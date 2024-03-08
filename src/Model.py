import random
from copy import deepcopy

import pygame
from character import *
import WFC
import Map
from Map import Map
from Tree import Tree
from WFC import WFC2
import Bezier as bz
from House import House


class Model:
    def __init__(self, n=20):

        self.tree_textures = ["./data/imgs/props/trees_status/tree1.png",
                              "./data/imgs/props/trees_status/tree2.png",
                              "./data/imgs/props/trees_status/tree3.png",
                              "./data/imgs/props/trees_status/tree_cut.png"]
        self.house_textures = ["./data/imgs/props/houses_status/house1.png",
                               "./data/imgs/props/houses_status/house2.png",
                               "./data/imgs/props/houses_status/house3.png",
                               "./data/imgs/props/houses_status/house4.png",
                               "./data/imgs/props/houses_status/house5.png",
                               "./data/imgs/props/houses_status/house6.png"]

        self.n_ = n
        self.grid_size = (n, n)
        self.wfc = WFC2("data/test3.csv", self.grid_size)
        self.map = Map(self.n_)
        self.num_points = None
        self.control_points = None
        self.characters = [Character(), Character(position=(15, 40)), Character(position=(25, 25)),
                           Character(position=(50, 45))]
        self.player = Player()

        self.curve = None
        self.init_curve()

        self.trees = []
        self.houses = []

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

    def ai_characters_movements(self, map, character):
        directions = []
        if map is not None:
            x = character.x
            y = character.y
            if 0 <= x < len(map) and 0 <= y < len(map[0]):
                # Check each of the eight neighboring cells
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:  # Skip the current cell
                            new_x = x + dx
                            new_y = y + dy
                            if 0 <= new_x < len(map) and 0 <= new_y < len(map[0]):
                                if map[new_y][new_x] in [{12}, {42}]:
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
        if map is not None:

            for i in range(1):
                for j in range(1):
                    print(map[i][j])

            x = self.player.x
            y = self.player.y
            if 0 <= x < len(map) and 0 <= y < len(map[0]):
                # Check each of the four neighboring cells: N, S, W, E
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    new_x = x + dx
                    new_y = y + dy

                    print(f"""nx : {new_x}, ny : {new_y}""")

                    if 0 <= new_x < len(map) and 0 <= new_y < len(map[0]):
                        print(f"""test : {map[new_y][new_x]}""")
                        if map[new_y][new_x] in [{12}, {42}]:
                            print(2)
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

    def addTrees(self, map):

        tree_weights = [10 if texture == self.tree_textures[0] else 1 for texture in self.tree_textures]

        for row_index, row in enumerate(map):
            for col_index, cell in enumerate(row):
                if cell == {12}:
                    if random.random() < 0.2:
                        tree_sprite = random.choices(self.tree_textures, weights=tree_weights, k=1)[0]
                        # tree = Tree(position=(col_index, row_index),sprite=random.choice(self.tree_textures))
                        tree = Tree(position=(col_index, row_index), sprite=tree_sprite)
                        self.trees.append(tree)
        return self.trees

    def addHouses(self, map):

        house_weights = [10 if texture == self.house_textures[0] else 1 for texture in self.house_textures]

        for row_index, row in enumerate(map):
            for col_index, cell in enumerate(row):
                if cell == {12} and cell not in self.trees:
                    if random.random() < 0.05:
                        house_sprite = random.choices(self.house_textures, weights=house_weights, k=1)[0]
                        house = House(position=(col_index, row_index), sprite=house_sprite)
                        self.houses.append(house)
        return self.houses
