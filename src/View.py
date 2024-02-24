import random
from Model import Model
from Play import Game
import pygame
import time


class View:
    def __init__(self):
        self.model = Model()
        self.grass_textures = ["LandsImg/grass2.png",
                               "LandsImg/grass2_1.png",
                               "LandsImg/grass2_2.png"]
        
        self.road_textures = ["LandsImg/horizontal_path.png",
                              "LandsImg/vertical_path.png"]
        
        self.water_textures = ["LandsImg/water.png"]
        self.window = None
        self.lands = None
        self.game = Game()
        pygame.init()
        self.window = pygame.display.set_mode((self.model.grid_size, self.model.grid_size))
        pygame.display.set_caption('WFC Test')

    def changeLand(self, m):
        grass_weights = [10 if texture == self.grass_textures[0] else 1 for texture in self.grass_textures]

        terrain_grid = [[random.choices(self.grass_textures, weights=grass_weights, k=1)[0] if land == "Land.GRASS"
                         else random.choice(self.road_textures) if land == "Land.ROAD"
                         else random.choice(self.water_textures) if land == "Land.WATER"
                         else land for land in row] for row in m.land_layer]
        
        print(f"length: {len(terrain_grid)} data: {m.land_layer[0][2]}")
        self.lands = [[pygame.image.load(path).convert() for path in row] for row in terrain_grid]
            

    def displayMap(self,map):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            [self.window.blit(image, (col_index * 16, row_index * 16))
             for row_index, row in enumerate(self.lands)
             for col_index, image in enumerate(row)]
            
            print(f" map: {map.land_layer[5][5]}")
            self.game.model.character.draw(self.window, "data/imgs/player_front.png", (5, 5))
            self.game.moveCharacter(self.window,map)

            time.sleep(2)

            pygame.display.flip()
