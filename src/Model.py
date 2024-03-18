import random
from character import Character, Player
from Tree import Tree
from WFC import WFC2
import Bezier as bz
from House import House


class Model:
    def __init__(self, n=20):

        self.tree_textures = ["./data/imgs/props/trees_status/tree1.png",
                              "./data/imgs/props/trees_status/tree2.png",
                              "./data/imgs/props/trees_status/tree3.png"]
        self.house_textures = ["./data/imgs/props/houses_status/house1.png",
                               "./data/imgs/props/houses_status/house2.png",
                               "./data/imgs/props/houses_status/house3.png",
                               "./data/imgs/props/houses_status/house4.png",
                               "./data/imgs/props/houses_status/house5.png",
                               "./data/imgs/props/houses_status/house6.png"]

        self.n_ = n
        self.grid_size = (n, n)
        self.wfc = WFC2("data/test3.csv", self.grid_size)

        self.num_points = None
        self.control_points = None
        self.curve = None
        self.control_points2 = None
        self.curve2 = None
        self.init_curve()
        self.curve3 = None
        self.control_points3 = None

        self.characters = [Character(position=(5, 5)),
                           Character(position=(15, 40)),
                           Character(position=(25, 25)),
                           Character(position=(30, 35))]
        self.player = Player(position=(random.randint(0, n), random.randint(0, n)))

        self.trees = []
        self.houses = []

    def init_curve(self):
        self.num_points = 100
        self.control_points = bz.generate_control_points(self.n_)
        self.curve = bz.bezier_curve(self.control_points, self.num_points)
        self.control_points2 = bz.generate_control_points(self.n_)
        index = random.randint(0, len(self.curve)-1)
        self.control_points2[0] = self.curve[index]
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

    def add_road(self, nb_road):
        for i in range(nb_road):
            A, B = (random.randint(0, self.n_ - 1), random.randint(0, self.n_ - 1)), \
                (random.randint(0, self.n_ - 1), random.randint(0, self.n_ - 1))
            # Générer un chemin aléatoire de A à B

            x, y = A
            chemin = [(x, y)]
            while (x, y) != B and len(chemin) < 15:
                choix = random.choice(['x', 'y'])
                if choix == 'x' and x != B[0]:
                    x += -1 if x > B[0] else 1
                elif y != B[1]:
                    y += -1 if y > B[1] else 1
                chemin.append((x, y))

            for (x, y) in chemin:
                if self.wfc.grid[y][x] == {12}:
                    self.wfc.grid[y][x] = random.choices(({12}, {14}, {15}), weights=[1, 5, 5], k=1)[0]

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
                                if map[new_y][new_x] in [{12}, {14}, {15}]:
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
    def player_movements(self, map, houses):
        player_directions = []

        if map is not None:
            x = self.player.x
            y = self.player.y

            if 0 <= x < len(map) and 0 <= y < len(map[0]):

                # Check each of the four neighboring cells: N, S, W, E
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    new_x = x + dx
                    new_y = y + dy

                    if 0 <= new_x < len(map) and 0 <= new_y < len(map[0]):
                        houses_array = [house.position for house in houses]
                        if (new_x, new_y) not in houses_array:
                            if map[new_y][new_x] in [{12}, {14}, {15}]:
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

    def addTrees(self):
        """
        Adds trees to the map based on certain conditions.

        tree_weights: Weights assigned to different tree textures.
        tree_sprite: Selected tree sprite based on weighted random choice.
        tree: Tree object with chosen sprite added to the list of trees.

        map: 2D map grid to add trees to.
        List of Tree objects added to the map.
        """
        tree_weights = [10 if texture == self.tree_textures[0] else 1 for texture in self.tree_textures]

        for row_index, row in enumerate(self.wfc.grid):
            for col_index, cell in enumerate(row):
                if cell == {12}:  # Assuming {12} is the code for an empty tile
                    if random.random() < 0.2:  # Adjust probability as needed
                        tree_sprite = random.choices(self.tree_textures, weights=tree_weights, k=1)[0]
                        tree = Tree(position=(col_index, row_index), sprite=tree_sprite)
                        self.trees.append(tree)
        return self.trees

    def addHouses(self):
        """
        Adds houses to the map based on certain conditions.

        house_weights: Weights assigned to different house textures.
        house_sprite: Selected house sprite based on weighted random choice.
        house: House object with chosen sprite added to the list of houses.

        2D map grid to add houses to.
        List of House objects added to the map.
        """
        house_weights = [10 if texture == self.house_textures[0] else 1 for texture in self.house_textures]

        for row_index, row in enumerate(self.wfc.grid):
            for col_index, cell in enumerate(row):
                if cell == {12} and cell not in self.trees:  # Assuming {12} is the code for an empty tile
                    if random.random() < 0.05:  # Adjust probability as needed
                        house_sprite = random.choices(self.house_textures, weights=house_weights, k=1)[0]
                        house = House(position=(col_index, row_index), sprite=house_sprite)
                        self.houses.append(house)
        return self.houses

    def reposition_character(self, char):
        for row_index, row in enumerate(self.wfc.grid):
            for col_index, cell in enumerate(row):
                if cell in {12}:
                    char.position = (row_index, col_index)
