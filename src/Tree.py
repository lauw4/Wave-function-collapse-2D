# Tree.py

from Prop import Prop
import os


class Tree(Prop):
    def __init__(self, name=None, position=(0, 0), can_overlap=False, sprite="", state=4):
        super().__init__(name, position, can_overlap, sprite)
        self.state = state

    def alter_state(self, dommage=1):
        self.state -= dommage
        if self.state == 0:
            self.sprite = "./data/imgs/props/trees_status/tree_cut.png"
