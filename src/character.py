import pygame as pg 

class Character:
    def __init__(self, name=None, position=(0, 0)):
        self.name = name
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

    # Function to redraw the Road as the player is moving 
    def draw(seff, window, image, position):
        image = pg.image.load(image)
        image_rect = image.get_rect(topleft = (position[0] * 16, position[1] * 16))
        # Blit the road on the window
        window.blit(image, image_rect)
        pg.display.flip()


class Player(Character):
    def __init__(self, name=None, position=..., status=True):
        super().__init__(name, position)
        self._status = status
        
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, stat):
        self._status = stat