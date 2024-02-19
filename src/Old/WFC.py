import csv
from random import choices
from PIL import Image, ImageTk

from Tile import Tile


class WFC:
    def __init__(self, tiles_file, grid_size=(10, 10)):
        self.grid_size = grid_size
        self.tiles_ = []
        self.read_tiles_from_csv(tiles_file)
        self.grid = [[set(range(len(self.tiles_))) for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    def read_tiles_from_csv(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                lands = [row['NW'], row['N'], row['NE'],
                         row['W'], row['C'], row['E'],
                         row['SW'], row['S'], row['SE']]
                tile_ = Tile(row['Name'], "data/imgs/" + row['Path'], lands)
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

        weights = [40 if item == 0 else 1 for item in list(cell)]

        chosen_tile = choices(list(cell), weights=weights, k=1)[0]
        self.grid[row][col] = {chosen_tile}
        return chosen_tile

    def update_neighbors(self, row, col):
        rows, cols = len(self.grid), len(self.grid[0])
        neighbors = [(row - 1, col, 'S', 'N'),
                     (row + 1, col, 'N', 'S'),
                     (row, col - 1, 'E', 'W'),
                     (row, col + 1, 'W', 'E')]

        for r, c, side, opposite in neighbors:
            if 0 <= r < rows and 0 <= c < cols:
                neighbor_cell = self.grid[r][c]
                if len(neighbor_cell) > 1:
                    collapse_tile = next(iter(self.grid[row][col]))  # Prendre la tuile collapsée
                    valid_tiles = {tile for tile in neighbor_cell if self.tiles_[tile].can_place_next_to
                    (self.tiles_[collapse_tile], side)}

                    if len(valid_tiles) < len(neighbor_cell):
                        self.grid[r][c] = valid_tiles
                        # Propager uniquement si l'entropie est égale à 1
                        if len(valid_tiles) == 1:
                            self.update_neighbors(self.grid, r, c)

    def run_collapse(self, save_filepath="out/grille_finale.png", show=False):
        while True:
            cell = self.find_cell_with_lowest_entropy()

            if cell is None:
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
                tile_index = next(iter(cell))  # Récupérer l'indice de la tuile
                tile_image_path = self.tiles_[tile_index].img_path  # Récupérer le chemin de l'image de la tuile
                images.append(tile_image_path)
        return images

    def creer_grille(self, images):
        # Taille de chaque image et de la grille
        taille_image = (self.grid_size[0] * 16, self.grid_size[1] * 16)

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


# wfc = WFC("../data/test2.csv", grid_size=(5, 5))
# wfc.run_collapse(show=True)
