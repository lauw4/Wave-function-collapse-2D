import csv
from random import choices
from PIL import Image

from src.Tile import Tile2

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
                tile_ = Tile2(row['Name'], "LandsImg/" + row['Path'], lands)
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

        weights = [(1000 if item == 12
                    # else 100 if item in [4,5,6,7]
                    else 1)
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
                self.replace_square_tiles(13, 12)
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