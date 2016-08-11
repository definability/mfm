from PIL import Image
from numpy import array

from src import MFM, Model, ModelInput, View
from src.fitter import BruteForceFitter as Fitter
from data import get_datafile_path

MFM.init()
view = View((500, 500))
model = Model(view)
model_input = ModelInput(model)

model_filename = get_datafile_path('test.png')
image = Image.open(model_filename).convert('L')
image_data = array((image.getdata()))[::-1].astype('f') / 255
image.close()

fitter = Fitter(
    image=image_data, model=model, dimensions=0,
    steps=[1, 10, 10, 5], max_level=4,
    offsets=[0, -0.5, -0.5, 0],
    scales=[0, -2, -2, 1])

model.start(fitter)
