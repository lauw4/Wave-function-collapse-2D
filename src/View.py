import random
from Model import Model
from Play import Game
from Sql import Database
import pygame


class View:
    def __init__(self):
        """
        Initializes the View class, setting up the window for displaying the game and loading texture assets.

        This constructor loads various textures for different game elements (e.g., grass, roads, water, cliffs)
        and initializes the game environment, including the pygame window, the game's model, and the database.
        It sets the dimensions of the pygame display window and titles it 'WFC Test'.
        """
        self.grass_textures = ["LandsImg/grass2.png",
                               "LandsImg/grass2_1.png",
                               "LandsImg/grass2_2.png"]
        
        self.road_textures = ["LandsImg/vertical_path.png"]
        
        self.water_textures = ["LandsImg/water.png"]
        
        self.corner_cliff_ES_textures = ["LandsImg/corner_cliff_ES.png"]
        self.corner_cliff_NE_textures = ["LandsImg/corner_cliff_NE.png"]
        self.corner_cliff_SW_textures = ["LandsImg/corner_cliff_SW.png"]
        self.corner_cliff_WN_textures = ["LandsImg/corner_cliff_WN.png"]
        
        self.cliff_W_textures = ["LandsImg/cliff_W.png"]
        self.cliff_N_textures = ["LandsImg/cliff_N.png"]
        self.cliff_S_textures = ["LandsImg/cliff_S.png"]
        self.cliff_E_textures = ["LandsImg/cliff_E.png"]
        
        self.turn_cliff_ES_textures = ["LandsImg/turn_cliff_ES.png"]
        self.turn_cliff_NE_textures = ["LandsImg/turn_cliff_NE.png"]
        self.turn_cliff_SW_textures = ["LandsImg/turn_cliff_SW.png"]
        self.turn_cliff_WN_textures = ["LandsImg/turn_cliff_WN.png"]
        self.horizontal_path_textures = ["LandsImg/vertical_path.png"]
        self.vertical_path_textures = ["LandsImg/horizontal_path.png"]

        self.tree_textures = ["./data/imgs/props/trees_status/tree1.png",
                              "./data/imgs/props/trees_status/tree2.png",
                              "./data/imgs/props/trees_status/tree3.png",
                              "./data/imgs/props/trees_status/tree_cut.png"]
        
        self.house_textures = ["./data/imgs/props/houses_status/house1.png",
                               "./data/imgs/props/houses_status/house2.png",
                               "./data/imgs/props/houses_status/house3.png",
                               "./data/imgs/props/houses_status/house4.png",
                               "./data/imgs/props/houses_status/house5.png",
                               "./data/imgs/props/houses_status/house6.png"]
        self.window = None
        self.lands = None
        self.game = Game()
        self.model = Model()
        self.database = Database()

        pygame.init()
        self.window = pygame.display.set_mode((50 * 16, 50 * 16))
        pygame.display.set_caption('WFC Test')

    def changeLand(self, m):
        """
        Applies textures to the grid based on the cell values determined by the WFC algorithm.

        Parameters:
        - m: An object containing the WFC grid attribute that specifies the land type for each cell.

        The method iterates over the WFC grid, replacing numerical land types with corresponding textures.
        It applies different textures for various land types such as grass, roads, water, and cliffs, based
        on predefined conditions. The resulting grid of textures is stored in self.lands.
        """
        grass_weights = [10 if texture == self.grass_textures[0] else 1 for texture in self.grass_textures]

        terrain_grid = [[random.choices(self.grass_textures, weights=grass_weights, k=1)[0] if land == {12}
                         else random.choice(self.road_textures) if land == {42}
                         else random.choice(self.water_textures) if land == {13}
                         else random.choice(self.corner_cliff_ES_textures) if land == {0}
                         else random.choice(self.corner_cliff_NE_textures) if land == {1}
                         else random.choice(self.corner_cliff_SW_textures) if land == {2}
                         else random.choice(self.corner_cliff_WN_textures) if land == {3}
                         else random.choice(self.cliff_W_textures) if land == {4}
                         else random.choice(self.cliff_N_textures) if land == {5}
                         else random.choice(self.cliff_S_textures) if land == {6}
                         else random.choice(self.cliff_E_textures) if land == {7}
                         else random.choice(self.turn_cliff_ES_textures) if land == {8}
                         else random.choice(self.turn_cliff_NE_textures) if land == {9}
                         else random.choice(self.turn_cliff_SW_textures) if land == {10}
                         else random.choice(self.turn_cliff_WN_textures) if land == {11}
                         else random.choice(self.horizontal_path_textures) if land == {14}
                         else random.choice(self.vertical_path_textures) if land == {15}
                         else land for land in row] for row in m.wfc.grid]
        self.lands = [[pygame.image.load(path).convert() for path in row] for row in terrain_grid]

    def displayMap(self, model):
        """
        Displays the game map and all interactive elements, handling game events.

        Parameters:
        - model: The game model containing elements to be displayed, such as trees and houses.

        This method continuously updates the game window to display the map, interactive elements
        (trees and houses), and handle player and AI movement. It listens for the quit event to
        stop the game loop. The map display is updated at a rate of 30 frames per second.
        """
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            [self.window.blit(image, (col_index * 16, row_index * 16))
             for row_index, row in enumerate(self.lands)
             for col_index, image in enumerate(row)]

            for tree in model.trees:
                tree.draw(self.window)

            for house in model.houses:
                house.draw(self.window)

            # Moving the Player and the AI character
            if self.game.model.player.status:
                self.game.moveKeyboard(self.window, model.wfc.grid, model.houses)

            self.game.moveCharacter(self.window, model.wfc.grid)
            self.game.delete_player_in_contact()
            # Flip the Display of the game
            pygame.display.flip()
            # Smoothing the transactions
            pygame.time.Clock().tick(30)
