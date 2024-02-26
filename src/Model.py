import random
from copy import deepcopy

import pygame
from character import *
import WFC
import Map
import Bezier


class Model:
    def __init__(self):
        self.n = 17
        self.grid_size = self.n * 3 * 16
        self.wfc = None
        self.map = Map.Map(self.n)
        self.control_points = None
        self.getControlPoints()
        self.character = Character()
        self.player = Player()
        pass

    def runWFC(self):
        self.wfc = WFC.WFC("data/test2.csv", grid_size=(self.n, self.n))
        self.wfc.run_collapse()

    def changeLand(self):
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

