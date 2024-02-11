import pygame as pg 
from pathlib import Path
from Map import *

image_path = Path.cwd() / 'data'

class Character:
    def __init__(self, name=None, type="player", image="player_back.png", position=(0, 0)):
        self.name = name
        self._type = type
        self.image = image_path + image
        self.position = position

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos

    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, value):
        self._position = (value, self._position[1])

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, value):
        self._position = (self._position[0], value)

    # Function to draw the character and display them on the map
    def draw_caracter(self, map):
        image = pg.image.load(str(image_path /'imgs'/ self.image))
        image_rect = image.get_rect(center = (self.x, self.y))
        # Blit the character on the map from the center of the image
        map.blit(image, image_rect)
        pg.display.flip()

    # Function to redraw the Road as the player is moving 
    def redraw_road(self,map):
        image = pg.image.load(str(image_path /'landsImg'/'vertical_path.png'))
        image_rect = image.get_rect(center = (self.x, self.y))
        # Blit the road on the map
        map.blit(image, image_rect)
        pg.display.flip()

    # Functions to Move the CHARACTER
    def move_character_up(self, map):
        Character.redraw_road(map)
        self.y -= 16
        Character.draw_caracter(map)

    def move_character_down(self, map):
        Character.redraw_road(map)
        self.y += 16
        Character.draw_caracter(map)

    def move_character_left(self,map):
        Character.redraw_road(map)
        self.x -= 16
        Character.draw_caracter(map)

    def move_character_right(self,map):
        Character.redraw_road(map)
        self.x += 16
        Character.draw_caracter(map)