import csv
from random import choices
from PIL import Image

from Tile import Tile2

class WFC2:
    """
    A Wave Function Collapse algorithm implementation for procedurally generating tile-based grids.

    Attributes:
        grid_size (tuple): The size of the grid as (width, height).
        tiles_ (list): A list of Tile2 objects representing available tiles.
        grid (list): A 2D list representing the grid, where each cell contains a set of possible tile indices.

    Args:
        tiles_file (str): The path to the CSV file containing tile definitions.
        grid_size (tuple, optional): The size of the grid to generate. Defaults to (10, 10).

    Methods:
        read_tiles_from_csv(filename): Reads tile data from a CSV file and populates the tiles_ list.
        find_cell_with_lowest_entropy(): Finds the grid cell with the lowest entropy (fewest possible tiles) that is not collapsed.
        collapse_cell(row, col): Collapses a cell to a single tile based on weighted randomness.
        update_neighbors(row, col): Updates the neighbors of a collapsed cell to remove invalid tile options.
        run_collapse(save_filepath="out/grille_finale.png", show=False): Runs the collapse process until all cells are collapsed and saves/optionally shows the final grid image.
        get_final_grid_images(): Creates a list of image paths representing the final grid layout.
        creer_grille(images): Creates a single image from a list of tile image paths representing the final grid.
        replace_square_tiles(water_tile, grass_tile): Replaces specific square patterns with a single tile for water or grass.
    """
    def __init__(self, tiles_file, grid_size=(10, 10)):
        """
        Initialize the WFC2 class with a tiles file and a specified grid size.

        Parameters:
        - tiles_file (str): The path to the CSV file containing tile definitions.
        - grid_size (tuple): A tuple (width, height) specifying the size of the grid.

        The method reads the tiles from the CSV file and initializes a grid with
        possible tile indices for each cell based on the provided grid size.
        """
        self.grid_size = grid_size
        self.tiles_ = []
        self.read_tiles_from_csv(tiles_file)
        self.grid = [[set(range(len(self.tiles_))) for _ in range(grid_size[1])] for _ in range(grid_size[0])]
        # print(self.grid)

    def read_tiles_from_csv(self, filename):
        """
        Read tile definitions from a CSV file and store them in the tiles_ list.

        Parameters:
        - filename (str): The path to the CSV file containing tile definitions.

        Each row in the CSV file should define a tile, including its name, image path,
        and connectivity information for all directions (N, W, E, S, NW, NE, SW, SE).
        """
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                lands = [row['N'], row['W'], row['E'], row['S'],
                         row['NW'], row['NE'], row['SW'], row['SE']]
                tile_ = Tile2(row['Name'], "LandsImg/" + row['Path'], lands)
                self.tiles_.append(tile_)

    def find_cell_with_lowest_entropy(self):
        """
        Find the cell in the grid with the lowest entropy (i.e., the fewest possible tiles),
        excluding cells that have only one possible tile or are already determined.

        Returns:
        - tuple: The (row, column) indices of the cell with the lowest entropy, or None
                 if all cells are determined or have equal entropy.
        """
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
        """
        Collapse the cell at the specified row and column to a single tile choice
        based on their weights. If the cell is already collapsed, does nothing.

        Parameters:
        - row (int): The row index of the cell to collapse.
        - col (int): The column index of the cell to collapse.

        Returns:
        - int: The index of the chosen tile for the cell, or None if the cell was already collapsed.
        """
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
        """
        Update the neighbors of the collapsed cell at (row, col) to eliminate impossible
        tile choices based on the newly collapsed cell's tile.

        Parameters:
        - row (int): The row index of the collapsed cell.
        - col (int): The column index of the collapsed cell.

        This method updates the possible tiles for neighboring cells based on the constraints
        defined by the adjacency rules of the tiles.
        """
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
        """
        Run the tile collapse process on the entire grid until all cells are collapsed,
        then save and optionally display the final grid image.

        Parameters:
        - save_filepath (str): The path where the final grid image will be saved.
        - show (bool): If True, display the final grid image using the default image viewer.

        The method iteratively collapses cells with the lowest entropy and updates neighbors
        until all cells are determined, then generates and saves the final grid image.
        """
        while True:
            cell = self.find_cell_with_lowest_entropy()
            if cell is None:
                self.replace_square_tiles(13, 12)
                final_images = self.get_final_grid_images()
                grille_finale = self.creer_grille(final_images)
                print("Ready")
                grille_finale.save(save_filepath)
                if show:
                    grille_finale.show()
                return

            row, col = cell
            self.collapse_cell(row, col)
            self.update_neighbors(row, col)

    def get_final_grid_images(self):
        """
               Generate a list of paths to the image files for each tile in the final grid.
                Returns:
        - list[str]: A list containing the paths to the image files for each tile in the grid.
                     If a cell in the grid is empty, it defaults to a specific grass tile image.

        This method maps the final tile indices in the grid to their corresponding image paths,
        preparing for the assembly of the final grid image.
        """
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
        """
            Create the final grid image from a list of tile image paths.

            Parameters:
            - images (list[str]): A list of paths to the image files for each tile in the final grid.

            Returns:
            - Image: The assembled final grid image as a single composite image.

            This method assembles the final grid by placing each tile's image according to its position
            in the grid, resulting in a single, large image representing the completed puzzle.
            """
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
        """
            Replace specific square patterns in the grid with either a water or grass tile.

            Parameters:
            - water_tile (int): The index of the tile to use for replacing water square patterns.
            - grass_tile (int): The index of the tile to use for replacing grass square patterns.

            This method scans the grid for predefined square patterns that represent larger areas of
            water or grass and replaces them with the corresponding single tile, effectively reducing
            the pattern's entropy and refining the final image.
            """
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