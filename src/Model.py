from src.Map import Map
from src.WFC import WFC2
import src.Bezier as bz


class Model:
    def __init__(self, n=20):
        self.n_ = n
        self.grid_size = (n, n)
        self.wfc = WFC2("data/test3.csv", self.grid_size)
        self.map = Map(self.n_)
        self.num_points = None
        self.control_points = None
        self.curve = None
        self.init_curve()

    def init_curve(self):
        self.num_points = 100
        self.control_points = bz.generate_control_points(self.n_)
        self.curve = bz.bezier_curve(self.control_points, self.num_points)

    def add_water(self):
        for y in range(self.n_):
            for x in range(self.n_):
                if bz.is_below_curve([x, y], self.curve, 2):
                    self.wfc.grid[y][x] = {13}
                    self.wfc.update_neighbors(y, x)
                elif not (bz.is_below_curve([x, y], self.curve, 4)):
                    self.wfc.grid[y][x] = {12}
                    self.wfc.update_neighbors(y, x)
