from PIL import Image
from numpy import array

from src import MFM, Model, ModelInput, View, ModelFitter
from data import get_datafile_path

MFM.init()
view = View((500, 500))
model = Model(view)
model_input = ModelInput(model)

model_filename = get_datafile_path('test.png')
image = Image.open(model_filename).convert('L')
fitter = ModelFitter(image=array((image.getdata()))[::-1].astype('f') / 255,
                     model=model)
image.close()

model.start(fitter)
