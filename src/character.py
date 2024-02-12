import pygame as pg 
from pathlib import Path
from Map import *

image_path = 'data/imgs/'

class Character:
    def __init__(self, name=None, image="player_back.png", position=(0, 0), field=Map()):
        self.name = name
        self.field = field
        self.image = str(image_path + image)
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
        image = pg.image.load(self.image)
        image_rect = image.get_rect(center = (self.x * 16, self.y * 16))
        # Blit the character on the background_image from the center of the image
        background_image.blit(image, image_rect)
        pg.display.flip()

    # Function to redraw the Road as the player is moving 
    def redraw_road(self,background_image):
        image = pg.image.load(self.image)
        image_rect = image.get_rect(center = (self.x * 16, self.y * 16))
        # Blit the road on the background_image
        background_image.blit(image, image_rect)
        pg.display.flip()

    # Functions to Move the CHARACTER
    def move_character_up(self, background_image):
        # Checking if Going UP the Character won't ecounter a house, water or a tree
        if self.field.land_layer(self.x, self.y - 1) in ["Land.HOUSE", "Land.TREE", "Land.WATER"]:
            self.y = self.y     # the Value doesn't change
        else:
            # Remove the character where it was to the new place
            Character.redraw_road(background_image)
            self.y -= 1     # change the y-coordinate hence the position to up
            Character.draw_caracter(background_image) 

    def move_character_down(self, background_image):
        # Checking if Going DOWN the Character won't ecounter a house, water or a tree
        if self.field.land_layer(self.x, self.y + 1) in ["Land.HOUSE", "Land.TREE", "Land.WATER"]:
            self.y = self.y     # the Value doesn't change
        else:
            # Remove the character where it was to the new place
            Character.redraw_road(background_image)
            self.y += 1     # change the y-coordinate hence the position to down
            Character.draw_caracter(background_image)

    def move_character_left(self,background_image):
        # Checking if Going LEFT the Character won't ecounter a house, water or a tree
        if self.field.land_layer(self.x - 1, self.y) in ["Land.HOUSE", "Land.TREE", "Land.WATER"]:
            self.x = self.x     # the Value doesn't change
        else:
            # Remove the character where it was to the new place
            Character.redraw_road(background_image)
            self.x -= 1     # change the y-coordinate hence the position to left
            Character.draw_caracter(background_image)

    def move_character_right(self,background_image):
        # Checking if Going RIGHT the Character won't ecounter a house, water or a tree
        if self.field.land_layer(self.x + 1, self.y) in ["Land.HOUSE", "Land.TREE", "Land.WATER"]:
            self.x = self.x     # the Value doesn't change
        else:
            # Remove the character where it was to the new place
            Character.redraw_road(background_image)
            self.x += 1     # change the y-coordinate hence the position to right
            Character.draw_caracter(background_image)
