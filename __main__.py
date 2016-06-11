from src import MFM, Model, ModelInput, View

MFM.init()
view = View((500, 500))
model = Model(view)
model_input = ModelInput(model)
model.start()
