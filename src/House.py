# House.py

from Prop import Prop
import os


class House(Prop):
    def __init__(self, name=None, position=(0, 0), can_overlap=False, sprite="house1.png", state= False):
        super().__init__(name, position, can_overlap, sprite)
        self.state = state

    def enter(self):
        pass

    def exit(self):
        pass