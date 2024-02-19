import random
from copy import deepcopy

import WFC
import Map
from src.Old import Bezier


class Model:
    def __init__(self, n=20):
        self.n_ = n
        self.grid_size = self.n_ * 3 * 16
        self.wfc = None
        self.map = None
        self.control_points = None
        self.getControlPoints()
        pass

    def runWFC(self):
        self.wfc = WFC.WFC("data/test2.csv", grid_size=(self.n_, self.n_))
        self.wfc.run_collapse()

    def changeLand(self):
        self.map = Map.Map(self.n_)
        self.map.set_land_layer(deepcopy(self.wfc))
        points = Bezier.calculate_bezier_curve(self.control_points)
        self.map.add_water(points)

    # =================
    #   Bezier river
    # =================

    def select_edge_point(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            return random.randint(0, self.grid_size - 1), 0
        elif edge == 'bottom':
            return random.randint(0, self.grid_size - 1), self.grid_size - 1
        elif edge == 'left':
            return 0, random.randint(0, self.grid_size - 1)
        elif edge == 'right':
            return self.grid_size - 1, random.randint(0, self.grid_size - 1)

    def getControlPoints(self):
        num_control_points = 2
        self.control_points = []
        # Générer les points de contrôle aléatoires
        for _ in range(num_control_points):
            control_point = (random.randint(0, self.grid_size),
                             random.randint(0, self.grid_size))
            self.control_points.append(control_point)
        # Ajouter les points de départ et de fin
        start_point = self.select_edge_point()
        end_point = self.select_edge_point()
        self.control_points.insert(0, start_point)
        self.control_points.append(end_point)
