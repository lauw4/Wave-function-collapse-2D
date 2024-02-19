import numpy as np

from Land import Land


class Map:
    def __init__(self, n=10):
        self.n = n
        self.grid_size = (n * 3, n * 3)
        self.land_layer = None

    def set_land_layer(self, wfc):
        tile_grid = [[element.pop() for element in row] for row in wfc.grid]
        lands_tiles_3x3 = []

        for i in range(self.n):
            for j in range(self.n):
                lands_tile_3x3 = wfc.tiles_[tile_grid[i][j]].lands_3x3
                lands_tiles_3x3.append(np.array(lands_tile_3x3))

        self.land_layer = np.zeros(self.grid_size, dtype=object)

        for i in range(self.n):
            for j in range(self.n):
                self.land_layer[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = lands_tiles_3x3[i * self.n + j]

    def add_water(self, bezier_points):
        for point in bezier_points:
            x, y = int(point[0] // 16), int(point[1] // 16)
            if self.land_layer[x, y] != 'Land.ROAD':
                self.land_layer[x, y] = 'Land.WATER'

            adjacent_offsets_water = [-1, 0, 1]
            for dx in adjacent_offsets_water:
                for dy in adjacent_offsets_water:
                    if dx == 0 and dy == 0:
                        continue
                    adjacent_x, adjacent_y = x + dx, y + dy
                    if 0 <= adjacent_x < self.n*3 and 0 <= adjacent_y < self.n*3:
                        if self.land_layer[adjacent_x, adjacent_y] != 'Land.ROAD':
                            self.land_layer[adjacent_x, adjacent_y] = 'Land.WATER'
