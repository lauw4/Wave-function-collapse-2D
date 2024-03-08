#prop.py
import pygame as pg

class Prop:
    def __init__(self, name: str, position: tuple, can_overlap: bool, sprite: str):
        self.name = name
        self.position = position
        self.can_overlap = can_overlap
        self.sprite = sprite

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position = (value, self.position[1])

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position = (self.position[0], value)

    # Function to redraw the Road as the player is moving 
    def draw(self, window, image, position):
        image = pg.image.load(image)
        image_rect = image.get_rect(topleft = (position[0] * 16, position[1] * 16))
        # Blit the road on the window
        window.blit(image, image_rect)