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
fitter = Fitter(image=array((image.getdata()))[::-1].astype('f') / 255,
                model=model, dimensions=199, steps=MFM.get_multipliers(3),
                max_level=2)
image.close()

model.start(fitter)
