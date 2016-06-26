from PIL import Image
from numpy import array

from src import MFM, Model, ModelInput, View
from src.fitter import GibbsSamplerFitter as Fitter
from data import get_datafile_path

MFM.init()
view = View((500, 500))
model = Model(view)
model_input = ModelInput(model)

model_filename = get_datafile_path('test.png')
image = Image.open(model_filename).convert('L')
fitter = Fitter(image=array((image.getdata()))[::-1].astype('f') / 255,
                model=model, steps=MFM.get_multipliers(3))
image.close()

model.start(fitter)
