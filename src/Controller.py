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
        self.view.displayMap()

c = Controller()
c.run()
