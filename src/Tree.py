# Tree.py

import Prop
import os
import os

Tree_folder = "../data/imgs/props/trees_status"


class Tree(Prop):
    def __init__(self, name=None, position=(0, 0), can_overlap=False, sprite=None, sprite_trunk=None):
        Prop.__init__(name, position, can_overlap, sprite)
        self.state = False
        self.sprite_trunk = os.path.join(Tree_folder, sprite_trunk)
