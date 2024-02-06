import WFC
import pygame
import random
import numpy as np

n = 27


def fill_grid_with_texture(surface, points, texture):
    """
    Remplit les cases de la grille avec une texture basée sur les points donnés.
    """
    filled_cells = set()
    for x, y in points:
        cell_x, cell_y = x // 16 * 16, y // 16 * 16
        if (cell_x, cell_y) not in filled_cells:
            surface.blit(texture, (cell_x, cell_y))
            filled_cells.add((cell_x, cell_y))


# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
grid_size = n * 3 * 16  # 16 cases de 16 pixels
window = pygame.display.set_mode((grid_size, grid_size))
pygame.display.set_caption('Courbe de Bézier Cubique avec Points de Contrôle Aléatoires')

wfc = WFC.WFC("../data/test2.csv", grid_size=(n, n))
wfc.run_collapse()
g = wfc.grid

g = [[element.pop() for element in row] for row in g]

# Liste de tableaux 3x3 à partir de votre code existant
tableaux_3x3 = []

for i in range(n):
    for j in range(n):
        tableau_3x3 = wfc.tiles[g[i][j]].lands_3x3  # Remplacez par votre source de tableaux 3x3
        tableaux_3x3.append(np.array(tableau_3x3))

# Créez le tableau final n x n
terrain_grid = np.zeros((3*n, 3*n), dtype=object)

# Remplissez le tableau final avec les tableaux 3x3
for i in range(n):
    for j in range(n):
        terrain_grid[i*3:(i+1)*3, j*3:(j+1)*3] = tableaux_3x3[i*n + j]

print(terrain_grid)

# Affichez le tableau 15x15 résultant
for ligne in terrain_grid:
    print(ligne)

# Liste des textures possibles pour "Land.GRASS" et "Land.ROAD"
grass_textures = ["../LandsImg/grass1.png"]
road_textures = ["../LandsImg/horizontal_path.png", "../LandsImg/vertical_path.png"]

# Utilisation d'une liste en compréhension pour le remplacement aléatoire
terrain_grid = [[random.choice(grass_textures) if land == "Land.GRASS"
                 else (random.choice(road_textures) if land == "Land.ROAD"
                       else land)
                 for land in row] for row in terrain_grid]
lands = [[pygame.image.load(path).convert() for path in row] for row in terrain_grid]

for row_index, row in enumerate(lands):
    print(row)

grass_texture = pygame.image.load('../LandsImg/grass1.png').convert()
grass_texture = pygame.transform.scale(grass_texture, (16, 16))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    blit_list = [window.blit(image,(col_index * 16, row_index * 16))
                 for row_index, row in enumerate(lands)
                 for col_index, image in enumerate(row)]

    pygame.display.flip()

pygame.quit()
