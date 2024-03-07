#Tree.py

import Prop
import os
import os
Tree_folder = "../data/imgs/props/trees_status"


class Tree:
    def __init__(self, sprite_trunk):
        self.Type = "Tree"
        self.state = False
        self.sprite_trunk = os.path.join(Tree_folder, sprite_trunk)
        self.props = []
