import random
from Model import Model

import pygame


class View:
    def __init__(self):
        self.model = Model()
        self.grass_textures = ["LandsImg/grass2.png",
                               "LandsImg/grass2_1.png",
                               "LandsImg/grass2_2.png"]
        self.road_textures = ["LandsImg/vertical_path.png"]
        self.water_textures = ["LandsImg/water.png"]
        self.window = None
        self.lands = None
        pygame.init()
        self.window = pygame.display.set_mode((self.model.grid_size, self.model.grid_size))
        pygame.display.set_caption('WFC Test')

    def changeLand(self, m):
        grass_weights = [10 if texture == self.grass_textures[0] else 1 for texture in self.grass_textures]

        terrain_grid = [[random.choices(self.grass_textures, weights=grass_weights, k=1)[0] if land == "Land.GRASS"
                         else random.choice(self.road_textures) if land == "Land.ROAD"
                         else random.choice(self.water_textures) if land == "Land.WATER"
                         else land for land in row] for row in m.land_layer]
        self.lands = [[pygame.image.load(path).convert() for path in row] for row in terrain_grid]

    def displayMap(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            [self.window.blit(image, (col_index * 16, row_index * 16))
             for row_index, row in enumerate(self.lands)
             for col_index, image in enumerate(row)]

            pygame.display.flip()
