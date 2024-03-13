# prop.py
import pygame as pg


class Prop:
    def __init__(self, name: str, position: tuple, can_overlap: bool, sprite: str):
        self.name = name
        self.position = position
        self.can_overlap = can_overlap
        self.sprite = sprite

    def draw(self, window):
        image = pg.image.load(self.sprite)
        image_rect = image.get_rect(topleft=(self.position[0] * 16, self.position[1] * 16))
        window.blit(image, image_rect)
