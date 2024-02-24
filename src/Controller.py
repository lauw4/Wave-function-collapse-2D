from Model import Model
from View import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        self.model.runWFC()
        self.model.changeLand()
        self.view.changeLand(self.model.map)
        self.view.displayMap(self.model.map)

c = Controller()
c.run()
