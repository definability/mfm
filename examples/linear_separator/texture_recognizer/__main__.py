from os.path import join as pjoin, dirname
from sys import argv
from random import randint

from PIL import Image

from .Texture import Texture
from .neighbourhood import neighbourhoods

from cProfile import Profile
from pstats import Stats
try:
    range = xrange
except NameError:
    pass


def process_colors(pixel, colors, colors_dictionary=None):
    if type(pixel) is tuple or type(pixel) is list:
        d = tuple(colors * (d + 1) / 256 for d in pixel)
        p = reduce(lambda x, y: x*colors+y, d, 0)
    else:
        p = colors * (pixel + 1) / 256
    if colors_dictionary is None:
        return p
    elif p in colors_dictionary:
        return colors_dictionary[p]
    else:
        return None


if __name__ == '__main__':
    image_name = argv[1]
    mask_name = argv[2]
    test_name = argv[3]
    result_name = argv[4]
    colors = int(argv[5])
    textures = int(argv[6])
    neighbourhood_class = int(argv[7])

    RGB_MODE=False
    cur_neighbourhood = neighbourhoods[neighbourhood_class]

    image = Image.open(pjoin(dirname(__file__), image_name))
    if not RGB_MODE:
        image = Image.open(pjoin(dirname(__file__), image_name)).convert('L')
    mask = Image.open(pjoin(dirname(__file__), mask_name))
    width, height = image.size

    data = list(image.getdata())
    mask_data = list(mask.getdata())
    known_classes = []
    border = neighbourhood_class - 1 if neighbourhood_class > 1 else 0

    colors_dictionary = dict()
    count = 0
    for x in range(height):
        for y in range(width):
            cur = process_colors(data[x*width+y], colors)
            if cur not in colors_dictionary:
                colors_dictionary[cur] = count
                count += 1

    texture = Texture(len(cur_neighbourhood), len(colors_dictionary), textures)
    for x in range(border, height-border-1):
        for y in range(border, width-border-1):
            cur = process_colors(data[x*width+y], colors, colors_dictionary)

            params = {}

            for key, n in enumerate(cur_neighbourhood):
                i, j = n(x, y)
                neighbour_color = process_colors(data[i*width+j], colors,
                                                 colors_dictionary)
                params[key] = (cur, neighbour_color)

            cur_mask = mask_data[x*width+y]
            if sum(cur_mask) == 0:
                continue
            if cur_mask not in known_classes:
                known_classes.append(cur_mask)

            texture.pick_texture_sample(params, known_classes.index(cur_mask))
    #pring 'Setup'
    profile = Profile()
    profile.enable()
    texture.setup()
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()

    test_image = Image.open(pjoin(dirname(__file__), test_name))
    if not RGB_MODE:
        test_image = test_image.convert('L')
    test_width, test_height = test_image.size
    test_data = list(test_image.getdata())
    results = []

    profile = Profile()
    profile.enable()
    for x in range(test_height):
        row = []
        for y in range(test_width):
            cur = process_colors(test_data[x*test_width+y], colors,
                                 colors_dictionary)

            params = {}
            for key, n in enumerate(cur_neighbourhood):
                i, j = n(x, y)
                if i < test_height and j < test_width and i>0 and j>0:
                    neighbour_color = process_colors(test_data[i*test_width+j],
                                                     colors, colors_dictionary)
                    params[key] = (cur, neighbour_color)

            t = texture.recognize_texture(params)
            row.append(t)
        results += row
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()

    results = [known_classes[r] if r is not None else (0, 0, 0)
                                for r in results]
    result = Image.new('RGB', test_image.size)
    result.putdata(results)
    result.save(pjoin(dirname(__file__), result_name))

