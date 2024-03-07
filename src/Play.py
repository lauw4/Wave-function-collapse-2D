import pygame as pg
from Model import Model
import random

class Game:
    def __init__(self):
        self.model = Model()
        # Images for the Player
        self.player_textures = ["data/imgs/player_right.png", 
                                "data/imgs/player_left.png", 
                                "data/imgs/player_back.png", 
                                "data/imgs/player_front.png"]
        # Images for the character
        self.character_textures = ["data/imgs/character_right.png",
                                   "data/imgs/character_left.png",
                                   "data/imgs/character_back.png",
                                   "data/imgs/character_front.png"]

    def moveCharacter(self, window, map):
        positions = self.model.ai_characters_movements(map)
        print(f'Positions:{positions}')

        if positions:
            turn = random.choice(positions)
            print(f'chosen:{turn}')

            if turn == "N":
                self.model.character.y -= 1
                self.model.character.image = self.character_textures[2]
            elif turn == "S":
                self.model.character.y += 1
                self.model.character.image = self.character_textures[3]
            elif turn == "W":
                self.model.character.x -= 1
                self.model.character.image = self.character_textures[1]
            elif turn == "E":
                self.model.character.x += 1
                self.model.character.image = self.character_textures[0]
            elif turn == "NW":
                self.model.character.x -= 1
                self.model.character.y -= 1
                self.model.character.image = self.character_textures[2]
            elif turn == "NE":
                self.model.character.x += 1
                self.model.character.y -= 1
                self.model.character.image = self.character_textures[2]
            elif turn == "SW":
                self.model.character.x -= 1
                self.model.character.y += 1
                self.model.character.image = self.character_textures[3]
            elif turn == "SE":
                self.model.character.x += 1
                self.model.character.y += 1
                self.model.character.image = self.character_textures[3]

            # Draw the character after updating its position
            self.model.character.draw(window, self.model.character.image, (self.model.character.x, self.model.character.y))
        else:
            print("the position is None or empty")


   # Function for moving the Player as the direction keys are pressed 
    def moveKeyboard(self, window, map):
        # get possible movements direction the player can make
        player_positions = self.model.player_movements(map)
        print(f'Player possible Positions:{player_positions}')
        self.model.player.draw(window, self.model.player.image, (self.model.player.x, self.model.player.y))
        if player_positions:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                if "W" in player_positions:
                    print("left pressed")
                    self.model.player.x -= 1
                    self.model.player.image = self.player_textures[1]
                    self.model.player.draw(window, self.model.player.image, (self.model.player.x, self.model.player.y))
                else:
                    print("Zone inaccessible")

            elif keys[pg.K_RIGHT]:
                if "E" in player_positions:
                    print("right pressed")
                    self.model.player.x += 1
                    self.model.player.image = self.player_textures[0]
                    self.model.player.draw(window, self.model.player.image, (self.model.player.x, self.model.player.y))
                else:
                    print("Zone inaccessible")

            elif keys[pg.K_UP]:
                if "N" in player_positions:
                    print("up pressed")
                    self.model.player.y -= 1
                    self.model.player.image = self.player_textures[2]
                    self.model.player.draw(window, self.model.player.image, (self.model.player.x, self.model.player.y))
                else:
                    print("Zone inaccessible")

            elif keys[pg.K_DOWN]:
                if "S" in player_positions:
                    print("down pressed")
                    self.model.player.y += 1
                    self.model.player.image = self.player_textures[3]
                    self.model.player.draw(window, self.model.player.image, (self.model.player.x, self.model.player.y))
                else:
                    print("Zone inaccessible")
        else:
            # In case you haven't pressed on the arrow buttons
            print("Use the Direction keys / arrow keys")

    # function to remove the player if meets a character
    def delete_player_in_contact(self):
        if self.model.player.x == self.model.character.x and self.model.player.y == self.model.character.y:
            self.model.player.status = False
            print("You Lost")