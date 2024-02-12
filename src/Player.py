import pygame as pg
from Map import Map
from character import *

class Player(Character):
    def __init__(self, name=None, image="player_back.png", position=..., field=..., status=True):
        super().__init__(name, image, position, field)
        self._status = status
        
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, stat):
        self._status = stat

    # Function for moving the Player as the direction keys are pressed 
    def moveKeyboard(self, image):
        
        self.draw_caracter(image)
        # Listen to Events with pygane
        for event in pg.event.get():
            # Listern for a Key press among the events
            if event.type == pg.KEYDOWN:
                
                if event.key == pg.K_LEFT:
                    # move the character in the direction of the key pressed
                    self.move_character_left(image)
                
                elif event.key == pg.K_RIGHT:
                    # move the character in the direction of the key pressed
                    self.move_character_right(image)

                elif event.key == pg.K_UP:
                    # move the character in the direction of the key pressed
                    self.move_character_up(image)

                elif event.key == pg.K_DOWN:
                    # move the character in the direction of the key pressed
                    self.move_character_down(image)
                else:
                    # In case you haven't pressed on the arrow buttons
                    print("Use the Direction keys / arrow keys") 

