import pygame as pg
from Model import Model
import random


class Game:
    def __init__(self):
        """
        Initializes the Game object.
        """
        # Model object
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
        """
        Moves the character/s on the map.
        
        Args:
            window: The game window.
            map: The map grid.
        """
        for character in self.model.characters:
            x, y = character.x, character.y
            # Test if it is displayed in water
            if map[y][x] == {13}:
                self.model.reposition_character(map) # change the position in the map

            else:
                # Get possible positions of the character
                positions = self.model.ai_characters_movements(map, character)

                if positions:
                    turn = random.choice(positions) # Random turn

                    if turn == "N":         # North
                        character.y -= 1
                        character.image = self.character_textures[2] # display the character with a corresponding image (visual movements)
                    elif turn == "S":       # South
                        character.y += 1
                        character.image = self.character_textures[3]
                    elif turn == "W":       # West
                        character.x -= 1
                        character.image = self.character_textures[1]
                    elif turn == "E":       # East
                        character.x += 1
                        character.image = self.character_textures[0]
                    elif turn == "NW":
                        character.x -= 1
                        character.y -= 1
                        character.image = self.character_textures[2]
                    elif turn == "NE":
                        character.x += 1
                        character.y -= 1
                        character.image = self.character_textures[2]
                    elif turn == "SW":
                        character.x -= 1
                        character.y += 1
                        character.image = self.character_textures[3]
                    elif turn == "SE":
                        character.x += 1
                        character.y += 1
                        character.image = self.character_textures[3]
                    # Draw the character after updating its position
                    character.draw(window, character.image, (character.x, character.y))
                

    # Function for moving the Player as the direction keys are pressed
    def moveKeyboard(self, window, map, houses):
        """
        Moves the player based on keyboard input.
        
        Args:
            window: The game window.
            map: The map grid.
            houses: List of house positions on the map.
        """
        # Current position of the Player
        x, y = self.model.player.x, self.model.player.y
        # Check if he's spawned on water
        if map[y][x] == {13}:
            new_y, new_x = random.choice(self.model.reposition_character(map)) # Redraw the Player off water
            self.model.player.x, self.model.player.y = new_y, new_x
        else:
            # Get possible movements direction the player can make
            player_positions = self.model.player_movements(map, houses)

            if player_positions:
                keys = pg.key.get_pressed()  # Key listener
                if keys[pg.K_LEFT]:
                    if "W" in player_positions:  # Check if the player can go left
                        self.model.player.x -= 1
                        self.model.player.image = self.player_textures[1] # display the Player with a corresponding image (visual movements) 
                    else:
                        print("Unreachable Zone") 

                elif keys[pg.K_RIGHT]:
                    if "E" in player_positions:
                        self.model.player.x += 1
                        self.model.player.image = self.player_textures[0]
                    else:
                        print("Unreachable Zone")

                elif keys[pg.K_UP]:
                    if "N" in player_positions:
                        self.model.player.y -= 1
                        self.model.player.image = self.player_textures[2]
                    else:
                        print("Unreachable Zone")

                elif keys[pg.K_DOWN]:
                    if "S" in player_positions:
                        self.model.player.y += 1
                        self.model.player.image = self.player_textures[3]

                    else:
                        print("Unreachable Zone")
                self.model.player.draw(window, self.model.player.image, self.model.player.position)
            else:
                # In case you haven't pressed on the arrow buttons
                print("Use the Direction keys / arrow keys")

    # Function to remove the player if meets a character
    def delete_player_in_contact(self):
        """
        Deletes the player if it meets a character.
        """
        for character in self.model.characters: # each character

            if self.model.player.x == character.x and self.model.player.y == character.y: # If player and caracter meets
                self.model.player.status = False  # the player dies
                print("You Lost")
