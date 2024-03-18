# Tree.py

from Prop import Prop
import os


class Tree(Prop):

    """
    Class representing a tree on the map.
    Inherits from the Prop class.
    """
    def __init__(self, name=None, position=(0, 0), can_overlap=False, sprite="", state=4):

        """
        Initializes a new tree with the specified attributes.

        name: Name of the tree
        position: Position of the tree on the map (default at (0, 0))
        can_overlap: Indicates if the tree can overlap with other objects
        sprite: Path to the tree's image
        state: State of the tree, if its here or not
        """

        super().__init__(name, position, can_overlap, sprite)
        self.state = state
        self.sprite = sprite

    def alter_state(self, damage=1):
        """
        Alters the state of the tree by reducing its health.
        Amount of damage to reduce the tree's state (default is 1).
        """
        self.state -= damage
        if self.state == 0:
            self.sprite = "./data/imgs/props/trees_status/tree_cut.png"

