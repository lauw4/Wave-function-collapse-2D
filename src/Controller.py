from Model import Model
from View import View


class Controller:
    def __init__(self):
        self.model = Model(30)
        self.view = View()

    def run(self):
        self.model.add_water()
        self.model.addTrees()
        self.model.wfc.run_collapse()

        self.model.map.set_land_layer(self.model.wfc)
        self.view.changeLand(self.model)

        for i in range(30):
            for j in range(30):
                print(self.model.wfc.grid[i][j])
            print('\n')

        self.view.displayMap(self.model.wfc.grid)


c = Controller()
c.run()
