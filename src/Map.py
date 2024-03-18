from copy import deepcopy
from Tree import Tree
import numpy as np

import numpy as np
from copy import deepcopy

class Map:
    def __init__(self, n=10):
        """
        Initializes the map with a grid of size n x n, defaulting to a size of 10.
        """
        self.n = n
        self.land_layer = None
        self.trees = []

    def set_land_layer(self, wfc):
        """
        Initializes the land layer based on the grid provided by WFC.
        WFC: The WFC object containing the grid.
        """
        tile_grid = [[element.pop() for element in row] for row in deepcopy(wfc.grid)]
        self.land_layer = np.zeros((self.n, self.n), dtype=object)

        for i in range(self.n):
            for j in range(self.n):
                self.land_layer[i, j] = wfc.tiles_[tile_grid[i][j]]

    def add_tree(self, tree: Tree):
        """
        Adds a tree at the specified position on the map, if the tile is of type "Land.GRASS".
        tree: The Tree object to add.
        """
        x, y = tree.position
        if self.land_layer[x, y] == "Land.GRASS":
            self.land_layer[x, y] = tree
            self.trees.append(tree)
