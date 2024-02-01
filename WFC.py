import tkinter as tk
from PIL import Image, ImageTk
import random
from Tile import read_tiles_from_csv


# Fonctions de l'algorithme WFC
# ------------------------------

def collapse_random_cell(grid):
    non_collapsed_cells = [(row_index, col_index) for row_index, row in enumerate(grid)
                           for col_index, cell in enumerate(row) if len(cell) > 1]

    if not non_collapsed_cells:
        return None  # Aucune cellule à collapser

    # Choisir une cellule au hasard parmi les cellules non collapsées
    row, col = random.choice(non_collapsed_cells)

    # Choisir une tuile au hasard dans cette cellule
    chosen_tile = random.choice(list(grid[row][col]))
    grid[row][col] = {chosen_tile}

    return row, col


def find_cell_with_lowest_entropy(grid):
    min_entropy = float('inf')
    min_cell = None

    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            entropy = len(cell)
            if 1 < entropy < min_entropy:
                min_entropy = entropy
                min_cell = (row_index, col_index)

    return min_cell


def collapse_cell(grid, row, col):
    cell = grid[row][col]
    if len(cell) == 1:
        return  # La cellule est déjà collapsée

    chosen_tile = random.choice(list(cell))
    grid[row][col] = {chosen_tile}
    return chosen_tile


def update_neighbors(grid, row, col, tiles):
    rows, cols = len(grid), len(grid[0])
    neighbors = [(row - 1, col, 'S', 'N'), (row + 1, col, 'N', 'S'), (row, col - 1, 'E', 'W'), (row, col + 1, 'W', 'E')]

    for r, c, side, opposite in neighbors:
        if 0 <= r < rows and 0 <= c < cols:
            neighbor_cell = grid[r][c]
            if len(neighbor_cell) > 1:
                collapse_tile = next(iter(grid[row][col]))  # Prendre la tuile collapsée
                valid_tiles = {tile for tile in neighbor_cell if
                               tiles[tile].can_place_next_to(tiles[collapse_tile], side)}

                if len(valid_tiles) < len(neighbor_cell):
                    grid[r][c] = valid_tiles
                    # Propager uniquement si l'entropie est égale à 1
                    if len(valid_tiles) == 1:
                        update_neighbors(grid, r, c, tiles)  # Propagation récursive, mais uniquement pour entropie = 1


# Fonctions Tkinter pour l'affichage
# -----------------------------------

def create_tile_widgets(master, tiles, indices, row, col):
    frame = tk.Frame(master, width=200, height=200)
    frame.grid(row=row, column=col, padx=2, pady=2)
    frame.grid_propagate(False)

    if len(indices) == 1:
        # Si la cellule est collapsée, afficher l'image en plein écran dans la frame
        tile_index = next(iter(indices))
        try:
            img = Image.open(tiles[tile_index].img_path)
            img = img.resize(
                (190, 190))  # Redimensionner l'image pour remplir la frame
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=tk_img)
            label.image = tk_img  # Garder une référence
            label.pack(fill='both', expand=True)  # Remplir toute la frame
        except IOError:
            print(f"Unable to open the image {tiles[tile_index].img_path}")
    else:
        for i, tile_index in enumerate(indices):
            try:
                img = Image.open(tiles[tile_index].img_path)
                img = img.resize((50, 50))  # Redimensionner pour un affichage en miniature
                tk_img = ImageTk.PhotoImage(img)
                label = tk.Label(frame, image=tk_img)
                label.image = tk_img  # Garder une référence
                label.grid(row=i // 4, column=i % 4)  # Organiser en groupes de 4

            except IOError:
                print(f"Unable to open the image {tiles[tile_index].img_path}")


def update_display(root, tiles, grid):
    for widget in root.winfo_children():
        widget.destroy()
    for i, row in enumerate(grid):
        for j, cell_indices in enumerate(row):
            create_tile_widgets(root, tiles, cell_indices, i, j)


# Fonction pour exécuter l'algorithme
# ------------------------------------

def run_collapse(grid, tiles, update_display_callback, delay=500, silent=True):
    if silent: delay = 0

    def collapse_step():
        nonlocal grid, tiles
        cell = find_cell_with_lowest_entropy(grid)
        if cell is None:
            final_images = get_final_grid_images(grid, tiles)
            grille_finale = creer_grille(final_images, (5, 5))
            grille_finale.show()  # Afficher l'image finale
            grille_finale.save("grille_finale.png")
            return  # Fin de l'algorithme

        row, col = cell
        collapse_cell(grid, row, col)
        update_neighbors(grid, row, col, tiles)
        if not silent: update_display_callback()
        root.after(delay, collapse_step)  # Planifier la prochaine étape

    # Collapse initial d'une cellule au hasard
    initial_collapse = collapse_random_cell(grid)
    if initial_collapse is not None:
        row, col = initial_collapse
        update_neighbors(grid, row, col, tiles)
        if not silent: update_display_callback()

    root.after(delay, collapse_step)  # Commencer la boucle de collapse


def get_final_grid_images(grid, tiles):
    images = []
    for row in grid:
        for cell in row:
            tile_index = next(iter(cell))  # Récupérer l'indice de la tuile
            tile_image_path = tiles[tile_index].img_path  # Récupérer le chemin de l'image de la tuile
            images.append(tile_image_path)
    return images


def creer_grille(images, grille_taille):
    # Taille de chaque image et de la grille
    taille_image = (1280, 1280)

    # Créer une nouvelle image pour la grille
    grille = Image.new('RGB', (taille_image[0] * grille_taille[0], taille_image[1] * grille_taille[1]))

    # Placer chaque image dans la grille
    for i, img in enumerate(images):
        # Ouvrir l'image
        image = Image.open(img)
        # Redimensionner si nécessaire
        if image.size != taille_image:
            image = image.resize(taille_image)
        # Calculer la position
        x = (i % grille_taille[0]) * taille_image[0]
        y = (i // grille_taille[0]) * taille_image[1]
        # Placer l'image
        grille.paste(image, (x, y))

    return grille


# Exemple d'utilisation
tiles = read_tiles_from_csv('test.csv')
grid = [[set(range(len(tiles))) for _ in range(5)] for _ in range(5)]

root = tk.Tk()
root.title("Wave Function Collapse Simulation")

update_display_callback = lambda: update_display(root, tiles, grid)
run_collapse(grid, tiles, update_display_callback, silent=True)  # 500 ms de délai

root.mainloop()
