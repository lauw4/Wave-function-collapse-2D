import pygame as pg 
from pathlib import Path
from Map import *

image_path = Path.cwd() / 'data'

class Character:
    def __init__(self, name=None, image="player_back.png", position=(0, 0), field=Map()):
        self.name = name
        self.field = field
        self.image = image_path + image
        self.position = position

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

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

    # Function to draw the character and display them on the background_image
    def draw_caracter(self, background_image):
        image = pg.image.load(str(image_path /'imgs'/ self.image))
        image_rect = image.get_rect(center = (self.x * 16, self.y * 16))
        # Blit the character on the background_image from the center of the image
        background_image.blit(image, image_rect)
        pg.display.flip()

    # Function to redraw the Road as the player is moving 
    def redraw_road(self,background_image):
        image = pg.image.load(str(image_path /'landsImg'/'vertical_path.png'))
        image_rect = image.get_rect(center = (self.x * 16, self.y * 16))
        # Blit the road on the background_image
        background_image.blit(image, image_rect)
        pg.display.flip()

    # Functions to Move the CHARACTER
    def move_character_up(self, background_image):

        if self.field.land_layer(self.x, self.y - 1) == "Land.HOUSE" or "Land.TREE" or "Land.WATER":
            self.y = self.y
        else:
            Character.redraw_road(background_image)
            self.y -= 1
            Character.draw_caracter(background_image)

    def move_character_down(self, background_image):

        if self.field.land_layer(self.x, self.y + 1) == "Land.HOUSE" or "Land.TREE" or "Land.WATER":
            self.y = self.y
        else:
            Character.redraw_road(background_image)
            self.y += 1
            Character.draw_caracter(background_image)

    def move_character_left(self,background_image):

        if self.field.land_layer(self.x - 1, self.y) == "Land.HOUSE" or "Land.TREE" or "Land.WATER":
            self.x = self.x
        else:
            Character.redraw_road(background_image)
            self.x -= 1
            Character.draw_caracter(background_image)

    def move_character_right(self,background_image):

        if self.field.land_layer(self.x + 1, self.y) == "Land.HOUSE" or "Land.TREE" or "Land.WATER":
            self.x = self.x
        else:
            Character.redraw_road(background_image)
            self.x += 1
            Character.draw_caracter(background_image)
