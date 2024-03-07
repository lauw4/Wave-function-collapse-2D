from Model import Model
from View import View


class Controller:
    def __init__(self):
        self.model = Model(50)
        self.view = View()

    def run(self):
        self.model.add_water()
        self.model.wfc.run_collapse()
        self.model.map.set_land_layer(self.model.wfc)
        self.view.changeLand(self.model)
        self.view.displayMap(self.model.wfc.grid)

c = Controller()
c.run()
