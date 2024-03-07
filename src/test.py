from copy import deepcopy
from Play import *

import numpy as np

import Bezier
import Tools
import WFC
import pygame
import random

from Land import Land
from Map import Map

button_color = (200, 0, 0)  # Vert


def getControlPoints():
    global control_points
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


def draw_button(surface, position, size, text):
    font = pygame.font.Font(None, 24)  # Utilisez pygame.font.Font(None, taille) pour la police par défaut
    text_render = font.render(text, True, (255, 255, 255))
    rect = pygame.Rect(position, size)
    surface.fill(button_color, rect)
    text_rect = text_render.get_rect(center=rect.center)
    surface.blit(text_render, text_rect)
    return rect  # Retourne le rectangle du bouton pour la détection de clic


# Vérifie si un point est à l'intérieur d'un rectangle
def is_point_inside_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


n = 15

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
grid_size = n * 3 * 16  # 16 cases de 16 pixels
window = pygame.display.set_mode((grid_size, grid_size))
pygame.display.set_caption('Courbe de Bézier Cubique avec Points de Contrôle Aléatoires')

getControlPoints()

t_values = np.linspace(0, 1, 500)


def changeWFC():
    global wfc
    wfc = WFC.WFC("data/test2.csv", grid_size=(n, n))
    wfc.run_collapse()


changeWFC()

grass_textures = ["LandsImg/grass2.png", "LandsImg/grass2_1.png", "LandsImg/grass2_2.png"]
road_textures = ["LandsImg/horizontal_path.png", "LandsImg/vertical_path.png"]
water_textures = ["LandsImg/water.png"]

def changeLand(g):
    global m, lands
    m = Map(n)
    m.set_land_layer(g)
    points = Bezier.calculate_bezier_curve(control_points, t_values)
    m.add_water(points)
    # Liste des textures possibles pour "Land.GRASS" et "Land.ROAD"

    grass_weights = [10 if texture == grass_textures[0] else 1 for texture in grass_textures]
    # Utilisation d'une liste en compréhension pour le remplacement aléatoire
    terrain_grid = [[random.choices(grass_textures, weights=grass_weights, k=1)[0] if land == "Land.GRASS"
                     else random.choice(road_textures) if land == "Land.ROAD"
    else random.choice(water_textures) if land == "Land.WATER"
    else land
                     for land in row] for row in m.land_layer]
    lands = [[pygame.image.load(path).convert() for path in row] for row in terrain_grid]

changeLand(deepcopy(wfc))

button_position = (0, 0)  # Position du bouton dans la fenêtre
button_size = (64, 32)  # Taille du bouton
button_text = 'Reset'

button_position2 = (0 + 128, 0)  # Position du bouton dans la fenêtre
button_size2 = (64, 32)  # Taille du bouton
button_text2 = 'Reset'

# Create the player
wael = Player("Wael",field=m, position=(0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifie si le clic est sur le bouton
            if is_point_inside_rect(event.pos, button_rect):
                getControlPoints()
                changeLand(deepcopy(wfc))
            if is_point_inside_rect(event.pos, button_rect2):
                changeWFC()
                changeLand(deepcopy(wfc))

    blit_list = [window.blit(image, (col_index * 16, row_index * 16))
                 for row_index, row in enumerate(lands)
                 for col_index, image in enumerate(row)]
    button_rect = draw_button(window, button_position, button_size, button_text)
    button_rect2 = draw_button(window, button_position2, button_size2, button_text2)
    wael.moveKeyboard(window)
    pygame.display.flip()

pygame.quit()
