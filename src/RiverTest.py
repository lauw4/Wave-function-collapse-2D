import random

import numpy as np
import pygame

import Bezier
from Model import Model

m = Model()
points = Bezier.calculate_bezier_curve(m.control_points)
land_layer = [[{0} for _ in range(1000 // 16)] for _ in range(1000 // 16)]
for point in points:
    x, y = int(point[0]) // 16, int(point[1] // 16)
    print(x, y)
    land_layer[x][y] = {13}
    adjacent_offsets_water = [-1, 0, 1]



print(len(land_layer))

pygame.init()
window = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('WFC Test')

water_textures = ["LandsImg/water.png"]
grass_textures = ["LandsImg/grass2.png"]
terrain_grid = [["LandsImg/water.png" if land == {13}
                 else "LandsImg/grass2.png" for land in row] for row in land_layer]

lands = [[pygame.image.load(path).convert() for path in row] for row in terrain_grid]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        [window.blit(image, (col_index, row_index))
         for row_index, row in enumerate(lands)
         for col_index, image in enumerate(row)]

        pygame.display.flip()
