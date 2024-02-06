import random

import numpy as np

from WFC import WFC
import pygame
import Bezier
import Tools

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
grid_size = 20 * 3 * 16  # 16 cases de 16 pixels
window = pygame.display.set_mode((grid_size, grid_size))
pygame.display.set_caption('Courbe de Bézier Cubique avec Points de Contrôle Aléatoires')

wfc = WFC("../data/test2.csv", grid_size=(20, 20))
wfc.run_collapse()
img = wfc.get_final_grid_images()
print(img)
img = [pygame.image.load(path).convert() for path in img]
imgConvert = [pygame.transform.scale(x, (48, 48)) for x in img]
print(len(imgConvert))
print(imgConvert)

start_point = Tools.select_edge_point(grid_size)
end_point = Tools.select_edge_point(grid_size)

control_point1 = (random.randint(0, grid_size), random.randint(0, grid_size))
control_point2 = (random.randint(0, grid_size), random.randint(0, grid_size))
control_point3 = (random.randint(0, grid_size), random.randint(0, grid_size))
control_points = [start_point, control_point1, control_point2, control_point3, end_point]

water_texture = pygame.image.load('../LandsImg/water.png').convert()
water_texture = pygame.transform.scale(water_texture, (16, 16))

t_values = np.linspace(0, 1, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for idx, image in enumerate(imgConvert):
        row = idx // 20
        col = idx % 20
        x = col * 48
        y = row * 48
        # Blitter l'image à sa position
        window.blit(image, (x, y))

    bezier_points = Bezier.calculate_bezier_curve(control_points, t_values)
    Tools.fill_grid_with_texture(window, bezier_points, water_texture, True, grid_size)
    pygame.display.flip()

pygame.quit()
