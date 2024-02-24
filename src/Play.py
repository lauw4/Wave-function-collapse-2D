import pygame as pg
from Model import Model
import random

class Game:
    def __init__(self):
        self.model = Model()
        
        self.player_textures = ["data/imgs/player_right.png", 
                                "data/imgs/player_left.png", 
                                "data/imgs/player_back.png", 
                                "data/imgs/player_front.png"]
        
        self.character_textures = ["data/imgs/"]

    def moveCharacter(self, window, map):
        
        positions = self.model.ai_characters_movements(map)
        print(f'Positions:{positions}')

        if positions is not None and positions:
            turn = random.choice(positions)
            print(f'chosen:{turn}')
            print(f'Positions:{positions}')

            if turn == "up":
                self.model.character.y += 1
                self.model.character.draw(window, self.player_textures[2], (self.model.character.x, self.model.character.y))
            elif turn == "down":
                self.model.character.y -= 1
                self.model.character.draw(window, self.player_textures[3], (self.model.character.x, self.model.character.y))
            elif turn == "left":
                self.model.character.x -= 1
                self.model.character.draw(window, self.player_textures[1], (self.model.character.x, self.model.character.y))
            elif turn == "right":
                self.model.character.x += 1
                self.model.character.draw(window, self.player_textures[0], (self.model.character.x, self.model.character.y))
            else:
                print("no direction")

        else:
            print("the position is None or empty")

    def movePlayer(self, turn):
        positions = self.model.player_movements()
        if positions is not None:
            if turn in positions:
                if turn == "up":
                    self.model.player.y += 1
                    return (self.model.player.x, self.model.player.y)
                elif turn == "down":
                    self.model.player.y -= 1
                    return (self.model.player.x, self.model.player.y)
                elif turn == "left":
                    self.model.player.x -= 1
                    return (self.model.player.x, self.model.player.y)
                elif turn == "right":
                    self.model.player.x += 1
                    return (self.model.player.x, self.model.player.y)
                else:
                    print("no direction")
            else:
                print("The chosen direction is not accessible")
        else:
            print("the position is None")

    # Function for moving the Player as the direction keys are pressed 
    def moveKeyboard(self, window):
        # Listen to Events with pygame
        for event in pg.event.get():
            # Listern for a Key press among the events
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    # move the character in the direction of the key pressed
                    position = self.movePlayer("left")
                    self.model.character.draw(window, self.player_textures[1], position)
                elif event.key == pg.K_RIGHT:
                    # move the character in the direction of the key pressed
                    position =self.movePlayer("right")
                    self.model.character.draw(window, self.player_textures[0], position)
                elif event.key == pg.K_UP:
                    # move the character in the direction of the key pressed
                    position =self.movePlayer("up")
                    self.model.character.draw(window, self.player_textures[2], position)
                elif event.key == pg.K_DOWN:
                    # move the character in the direction of the key pressed
                    position =self.movePlayer("down")
                    self.model.character.draw(window, self.player_textures[3], position)
                else:
                    # In case you haven't pressed on the arrow buttons
                    print("Use the Direction keys / arrow keys") 

