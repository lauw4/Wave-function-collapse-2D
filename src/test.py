import numpy as np

import Bezier
import Tools
import WFC
import pygame
import random

from Land import Land
from Map import Map

n = 27

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
grid_size = n * 3 * 16  # 16 cases de 16 pixels
window = pygame.display.set_mode((grid_size, grid_size))
pygame.display.set_caption('Courbe de Bézier Cubique avec Points de Contrôle Aléatoires')

num_control_points = 5
control_points = []

# Générer les points de contrôle aléatoires
for _ in range(num_control_points):
    control_point = (random.randint(0, grid_size), random.randint(0, grid_size))
    control_points.append(control_point)

# Ajouter les points de départ et de fin
start_point = Tools.select_edge_point(grid_size)
end_point = Tools.select_edge_point(grid_size)
control_points.insert(0, start_point)
control_points.append(end_point)

t_values = np.linspace(0, 1, 500)

wfc = WFC.WFC("../data/test2.csv", grid_size=(n, n))
wfc.run_collapse()

m = Map(n)
m.set_land_layer(wfc)
points = Bezier.calculate_bezier_curve(control_points, t_values)
m.add_water(points)

# Liste des textures possibles pour "Land.GRASS" et "Land.ROAD"
grass_textures = ["../LandsImg/grass2.png", "../LandsImg/grass2_1.png", "../LandsImg/grass2_2.png"]
road_textures = ["../LandsImg/horizontal_path.png", "../LandsImg/vertical_path.png"]
water_textures = ["../LandsImg/water.png"]

grass_weights = [10 if texture == grass_textures[0] else 1 for texture in grass_textures]

# Utilisation d'une liste en compréhension pour le remplacement aléatoire
terrain_grid = [[random.choices(grass_textures, weights=grass_weights, k=1)[0] if land == "Land.GRASS"
                 else random.choice(road_textures) if land == "Land.ROAD"
                 else random.choice(water_textures) if land == "Land.WATER"
                 else land
                 for land in row] for row in m.land_layer]

lands = [[pygame.image.load(path).convert() for path in row] for row in terrain_grid]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    blit_list = [window.blit(image, (col_index * 16, row_index * 16))
                 for row_index, row in enumerate(lands)
                 for col_index, image in enumerate(row)]

    pygame.display.flip()

pygame.quit()
