from Model import Model
from View import View


class Controller:
    def __init__(self):
        self.model = Model(30)
        self.view = View()

    def run(self):
        self.model.add_water()
        self.model.wfc.run_collapse()
        self.model.map.set_land_layer(self.model.wfc)
        self.model.addTrees(self.model.wfc.grid)
        self.view.changeLand(self.model)
        self.view.displayMap(self.model)

c = Controller()
c.run()
