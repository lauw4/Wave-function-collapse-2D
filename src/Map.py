from copy import deepcopy

import numpy as np


class Map:
    def __init__(self, n=10):
        self.n = n
        self.grid_size = (n, n)
        self.land_layer = None

    def set_land_layer(self, wfc):
        tile_grid = [[element.pop() for element in row] for row in deepcopy(wfc.grid)]
        self.land_layer = np.zeros(self.grid_size, dtype=object)

        for i in range(self.n):
            for j in range(self.n):
                self.land_layer[i, j] = wfc.tiles_[tile_grid[i][j]]

