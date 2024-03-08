# Tree.py

from Prop import Prop
import os


class Tree(Prop):
    def __init__(self, name=None, position=(0, 0), can_overlap=False, sprite="tree1.png", state= False):
        super().__init__(name, position, can_overlap, sprite)
        self.state = state
        self.sprite = sprite

