import csv
from random import choices
from PIL import Image, ImageTk

from Tile import Tile


class Tile2:
    def __init__(self, name_, img_path_, lands_):
        self.name = name_
        self.img_path = img_path_
        self.lands = lands_

    def get_land(self, side):
        sides = {'N': 0, 'W': 1, 'E': 2, 'S': 3, 'NW': 4, 'NE': 5, 'SW': 6, 'SE': 7}
        land_index = sides.get(side)
        if land_index is not None:
            return self.lands[land_index]
        raise ValueError("Invalid side")

    def can_place_next_to(self, other_tile, side):
        # Définir les côtés opposés
        opposite_sides = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E', 'NW': 'SE', 'NE': 'SW', 'SW': 'NE', 'SE': 'NW'}

        # Obtenir les attributs des côtés à comparer
        self_side_attr = self.get_land(side)
        other_side_attr = other_tile.get_land(opposite_sides[side])

        # Comparer les attributs
        return self_side_attr == other_side_attr


class WFC2:
    def __init__(self, tiles_file, grid_size=(10, 10)):
        self.grid_size = grid_size
        self.tiles_ = []
        self.read_tiles_from_csv(tiles_file)
        self.grid = [[set(range(len(self.tiles_))) for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    def read_tiles_from_csv(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                lands = [row['N'], row['W'], row['E'], row['S'],
                         row['NW'], row['NE'], row['SW'], row['SE']]
                tile_ = Tile2(row['Name'], "data/imgs2/" + row['Path'], lands)
                self.tiles_.append(tile_)

    def find_cell_with_lowest_entropy(self):
        min_entropy = float('inf')
        min_cell = None

        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                entropy = len(cell)
                if 1 < entropy < min_entropy:
                    min_entropy = entropy
                    min_cell = (row_index, col_index)
        return min_cell

    def collapse_cell(self, row, col):
        cell = self.grid[row][col]
        if len(cell) == 1:
            return  # La cellule est déjà collapsée

        weights = [(40 if item == 12 else 1)
                   for item in list(cell)]

        # weights = [1 for item in list(cell)]
        chosen_tile = choices(list(cell), weights=weights, k=1)[0]
        self.grid[row][col] = {chosen_tile}
        return chosen_tile

    def update_neighbors(self, row, col):
        rows, cols = len(self.grid), len(self.grid)
        neighbors = [(row - 1, col, 'S', 'N'),
                     (row + 1, col, 'N', 'S'),
                     (row, col - 1, 'E', 'W'),
                     (row, col + 1, 'W', 'E'),
                     (row - 1, col - 1, 'SE', 'NW'),
                     (row - 1, col + 1, 'SW', 'NE'),
                     (row + 1, col - 1, 'NE', 'SW'),
                     (row + 1, col + 1, 'NW', 'SE')]

        for r, c, side, opposite in neighbors:
            if 0 <= r < rows and 0 <= c < cols:
                neighbor_cell = self.grid[r][c]
                if len(neighbor_cell) > 1:
                    collapse_tile = next(iter(self.grid[row][col]))  # Prendre la tuile collapsée
                    valid_tiles = {tile for tile in neighbor_cell if
                                   self.tiles_[tile].can_place_next_to(self.tiles_[collapse_tile], side)}

                    if len(valid_tiles) < len(neighbor_cell):
                        self.grid[r][c] = valid_tiles
                        # Propager uniquement si l'entropie est égale à 1
                        if len(valid_tiles) == 1:
                            self.update_neighbors(r, c)

    def run_collapse(self, save_filepath="out/grille_finale.png", show=False):
        while True:
            cell = self.find_cell_with_lowest_entropy()
            if cell is None:
                # self.replace_square_tiles(13,12)
                final_images = self.get_final_grid_images()
                grille_finale = self.creer_grille(final_images)
                print("finished")
                grille_finale.save(save_filepath)
                if show:
                    grille_finale.show()
                return

            row, col = cell
            self.collapse_cell(row, col)
            self.update_neighbors(row, col)

    def get_final_grid_images(self):

        images = []
        for row in self.grid:
            for cell in row:
                if cell != set():
                    tile_index = next(iter(cell))  # Récupérer l'indice de la tuile
                    tile_image_path = self.tiles_[tile_index].img_path  # Récupérer le chemin de l'image de la tuile
                    images.append(tile_image_path)
                else:
                    images.append("data/imgs2/grass1.png")
        return images

    def creer_grille(self, images):
        # Taille de chaque image et de la grille
        taille_image = (self.grid_size[0] * 4, self.grid_size[1] * 4)

        # Créer une nouvelle image pour la grille
        grille = Image.new('RGB', (taille_image[0] * self.grid_size[0], taille_image[1] * self.grid_size[1]))

        # Placer chaque image dans la grille
        for i, img in enumerate(images):
            # Ouvrir l'image
            image = Image.open(img)
            # Redimensionner si nécessaire
            if image.size != taille_image:
                image = image.resize(taille_image)
            # Calculer la position
            x = (i % self.grid_size[0]) * taille_image[0]
            y = (i // self.grid_size[0]) * taille_image[1]
            # Placer l'image
            grille.paste(image, (x, y))
        return grille

    def replace_square_tiles(self, water_tile, grass_tile):
        rows = len(self.grid)
        cols = len(self.grid[0])

        for i in range(rows - 1):
            for j in range(cols - 1):
                if (self.grid[i][j] == {0} and
                        self.grid[i][j + 1] == {2} and
                        self.grid[i + 1][j] == {1} and
                        self.grid[i + 1][j + 1] == {3}):
                    print("Changed water")
                    # Remplacer les 4 tuiles par la tuile de remplacement
                    self.grid[i][j] = {water_tile}
                    self.grid[i][j + 1] = {water_tile}
                    self.grid[i + 1][j] = {water_tile}
                    self.grid[i + 1][j + 1] = {water_tile}
                if (self.grid[i][j] == {11} and
                        self.grid[i][j + 1] == {9} and
                        self.grid[i + 1][j] == {10} and
                        self.grid[i + 1][j + 1] == {8}):
                    print("Changed grass")
                    # Remplacer les 4 tuiles par la tuile de remplacement
                    self.grid[i][j] = {grass_tile}
                    self.grid[i][j + 1] = {grass_tile}
                    self.grid[i + 1][j] = {grass_tile}
                    self.grid[i + 1][j + 1] = {grass_tile}
#
# wfc = WFC2("data/test3.csv", grid_size=(10, 10))
#
# for tile in wfc.tiles_:
#     print(tile.lands)
#
# wfc.run_collapse()
#
# for i in wfc.grid:
#     print(i)

import numpy as np


def bezier_curve(control_points, num_points):
    n = len(control_points) - 1
    t = np.linspace(0, 1, num_points)
    curve_points = np.zeros((num_points, 2))

    for i in range(num_points):
        point = np.zeros(2)
        for j in range(n + 1):
            point += control_points[j] * binomial_coefficient(n, j) * ((1 - t[i]) ** (n - j)) * (t[i] ** j)
        curve_points[i] = point

    return curve_points


def binomial_coefficient(n, k):
    return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))


def is_below_curve(point, curve_points):
    x, y = point[0], point[1]
    return y < np.interp(x, curve_points[:, 0], curve_points[:, 1])


# Example grid dimensions
n = 10

# Example control points (you can adjust these)
start_point = np.array([0, np.random.randint(0, n)])  # Start point on left side
end_point = np.array([n - 1, np.random.randint(0, n)])  # End point on right side
control_point1 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 1
control_point2 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 2

control_points = np.array([start_point, control_point1, control_point2, end_point])
num_points = 100  # Number of points on the curve

# Calculate the Bézier curve
curve = bezier_curve(control_points, num_points)

# Example grid land_layer
land_layer = [[-1 for _ in range(n)] for _ in range(n)]

# Fill the grid with the Bézier curve
for i in range(len(curve) - 1):
    x0, y0 = int(round(curve[i][0])), int(round(curve[i][1]))
    x1, y1 = int(round(curve[i + 1][0])), int(round(curve[i + 1][1]))

    # Bresenham's line algorithm
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        if 0 <= x0 < n and 0 <= y0 < n:
            land_layer[y0][x0] = 1
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# Mark points below the curve as -2
for y in range(n):
    for x in range(n):
        if is_below_curve([x, y], curve):
            land_layer[y][x] = -2

# Print the grid
for row in land_layer:
    print(row)
import numpy as np


def bezier_curve(control_points, num_points):
    n = len(control_points) - 1
    t = np.linspace(0, 1, num_points)
    curve_points = np.zeros((num_points, 2))

    for i in range(num_points):
        point = np.zeros(2)
        for j in range(n + 1):
            point += control_points[j] * binomial_coefficient(n, j) * ((1 - t[i]) ** (n - j)) * (t[i] ** j)
        curve_points[i] = point

    return curve_points


def binomial_coefficient(n, k):
    return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))


def is_below_curve(point, curve_points):
    x, y = point[0], point[1]
    return y > np.interp(x, curve_points[:, 0], curve_points[:, 1])


# Example grid dimensions
n = 10

# Example control points (you can adjust these)
start_point = np.array([0, np.random.randint(0, n)])  # Start point on left side
end_point = np.array([n - 1, np.random.randint(0, n)])  # End point on right side
control_point1 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 1
control_point2 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 2

control_points = np.array([start_point, control_point1, control_point2, end_point])
num_points = 100  # Number of points on the curve

# Calculate the Bézier curve
curve = bezier_curve(control_points, num_points)

# Example grid land_layer
land_layer = [[-1 for _ in range(n)] for _ in range(n)]

# Fill the grid with the Bézier curve
for i in range(len(curve) - 1):
    x0, y0 = int(round(curve[i][0])), int(round(curve[i][1]))
    x1, y1 = int(round(curve[i + 1][0])), int(round(curve[i + 1][1]))

    # Bresenham's line algorithm
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        if 0 <= x0 < n and 0 <= y0 < n:
            land_layer[y0][x0] = 8
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# Mark points below the curve as -2
# for y in range(n):
#     for x in range(n):
#         if is_below_curve([x, y], curve):
#             land_layer[y][x] = -2

# Print the grid
for row in land_layer:
    print(row)

