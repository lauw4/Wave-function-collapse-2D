import random

from src.WFC import WFC2
import src.Bezier as bz


class Model:
    def __init__(self, n=20):
        self.n_ = n
        self.grid_size = (n, n)
        self.wfc = WFC2("data/test3.csv", self.grid_size)
        self.num_points = None
        self.control_points = None
        self.curve = None
        self.control_points2 = None
        self.curve2 = None
        self.init_curve()

    def init_curve(self):
        self.num_points = 100
        self.control_points = bz.generate_control_points(self.n_)
        self.curve = bz.bezier_curve(self.control_points, self.num_points)

        self.control_points2 = bz.generate_control_points(self.n_)
        self.control_points2[0] = random.choice(self.curve)
        self.curve2 = bz.bezier_curve(self.control_points2, self.num_points)

    def add_water(self):
        for y in range(self.n_):
            for x in range(self.n_):
                if bz.is_below_curve([x, y], self.curve, 2) or bz.is_below_curve([x, y], self.curve2, 2):
                    self.wfc.grid[y][x] = {13}
                    self.wfc.update_neighbors(y, x)
                elif not (bz.is_below_curve([x, y], self.curve, 4) or bz.is_below_curve([x, y], self.curve2, 4)):
                    self.wfc.grid[y][x] = {12}
                    self.wfc.update_neighbors(y, x)

    # Fonction pour chercher le nouveau motif
