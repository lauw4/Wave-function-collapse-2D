import random
from copy import deepcopy

import pygame
from character import *
import WFC
import Map
import Bezier
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
        self.getControlPoints()
        self.character = Character()
        self.player = Player()
        pass

    def runWFC(self):
        self.wfc = WFC.WFC("data/test2.csv", grid_size=(self.n, self.n))
        self.wfc.run_collapse()
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

    def ai_characters_movements(self, map):
        directions = []
        if map is not None and map.land_layer is not None:
            x = self.character.x
            y = self.character.y
            if 0 <= x < len(map.land_layer) and 0 <= y < len(map.land_layer[0]):
                # Check each of the eight neighboring cells
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:  # Skip the current cell
                            new_x = x + dx
                            new_y = y + dy
                            if 0 <= new_x < len(map.land_layer) and 0 <= new_y < len(map.land_layer[0]):
                                if map.land_layer[new_x][new_y] in ["Land.GRASS", "Land.ROAD"]:
                                    # Determine the direction based on the relative position
                                    direction = ""
                                    if dx == -1 and dy == 0:
                                        direction += "W"
                                    elif dx == -1 and dy == -1:
                                        direction += "NW"
                                    elif dx == 0 and dy == -1:
                                        direction += "N"
                                    elif dx == 1 and dy == -1:
                                        direction += "NE"
                                    elif dx == 1 and dy == 0:
                                        direction += "E"
                                    elif dx == 1 and dy == 1:
                                        direction += "SE"
                                    elif dx == 0 and dy == 1:
                                        direction += "S"
                                    elif dx == -1 and dy == 1:
                                        direction += "SW"
                                    directions.append(direction)

        return directions



    # Functions to give possible movements of the CHARACTER
    def player_movements(self, map):
        player_directions = []
        if map is not None and map.land_layer is not None:
            x = self.player.x
            y = self.player.y
            if 0 <= x < len(map.land_layer) and 0 <= y < len(map.land_layer[0]):
                # Check each of the four neighboring cells: N, S, W, E
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    new_x = x + dx
                    new_y = y + dy
                    if 0 <= new_x < len(map.land_layer) and 0 <= new_y < len(map.land_layer[0]):
                        if map.land_layer[new_x][new_y] in ["Land.GRASS", "Land.ROAD"]:
                            # Determine the direction based on the relative position
                            direction = ""
                            if dx == 0 and dy == -1:
                                direction += "N"
                            elif dx == 0 and dy == 1:
                                direction += "S"
                            elif dx == -1 and dy == 0:
                                direction += "W"
                            elif dx == 1 and dy == 0:
                                direction += "E"
                            player_directions.append(direction)

        return player_directions

