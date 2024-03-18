from Prop import Prop
import os

class Tree(Prop):
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
        state: State of the tree, True or False
        """

        super().__init__(name, position, can_overlap, sprite)  # Initializes attributes from Prop
        self.state = state  # Specific state of the tree
