import pygame as pg

class Prop:
    """
    Base class for Prop objects on the map.
    """

    def __init__(self, name: str, position: tuple, can_overlap: bool, sprite: str):
        """
        Initializes a new Prop object with the specified attributes.

        name: Name of the Prop object
        position: The x and y position of the object
        can_overlap: Boolean indicating if the object can overlap with others
        sprite: Path to the object's image
        """
        self.name = name
        self.position = position
        self.can_overlap = can_overlap
        self.sprite = sprite

    @property
    def x(self):
        """ X coordinate of the Prop."""
        return self.position[0]

    @x.setter
    def x(self, value):
        """ Sets the x coordinate of the Prop."""
        self.position = (value, self.position[1])

    @property
    def y(self):
        """ Y coordinate of the Prop."""
        return self.position[1]

    @y.setter
    def y(self, value):
        """ Sets the y coordinate of the Prop."""
        self.position = (self.position[0], value)

    def draw(self, window, image, position):
        """
        Draws the Prop object on the Pygame window.

        window: The Pygame window where everything is displayed
        image: Path to the object's image
        position: The x and y position where the object is drawn
        """

        image = pg.image.load(image)
        image_rect = image.get_rect(topleft=(position[0] * 16, position[1] * 16))
        window.blit(image, image_rect)
