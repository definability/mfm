from PIL import Image
from numpy import array

from src import MFM, Model, ModelInput, View
from src.fitter import BGDFitter as Fitter
from data import get_datafile_path

MFM.init()
view = View((500, 500))
model = Model(view)
model_input = ModelInput(model)

model_filename = get_datafile_path('test.png')
image = Image.open(model_filename).convert('L')
fitter = Fitter(image=array((image.getdata()))[::-1].astype('f') / 255,
                model=model, dimensions=100, max_loops=100,
                dx=.1, step=100.)
image.close()

model.start(fitter)
