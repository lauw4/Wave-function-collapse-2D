# Tree.py

from Prop import Prop
import os


class Tree(Prop):
    def __init__(self, name=None, position=(0, 0), can_overlap=False, sprite="", state=4):
        super().__init__(name, position, can_overlap, sprite)
        self.state = state
    """
    Class representing a tree on the map.
    Inherits from the Prop class.
    """
    def __init__(self, name=None, position=(0, 0), can_overlap=False, sprite="tree1.png", state=False):
        """
        Initializes a new tree with the specified attributes.

        name: Name of the tree
        position: Position of the tree on the map (default at (0, 0))
        can_overlap: Indicates if the tree can overlap with other objects
        sprite: Path to the tree's image
        state: State of the tree, if its here or not
        """


    def alter_state(self, dommage=1):
        self.state -= dommage
        if self.state == 0:
            self.sprite = "./data/imgs/props/trees_status/tree_cut.png"
