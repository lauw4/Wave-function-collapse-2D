from Prop import Prop
import os

class House(Prop):
    """
    Class representing a house on the map.
    Inherits from the Prop class.
    """

    def __init__(self, name=None, position=(0, 0), can_overlap=False, sprite="house1.png", state=False):
        """
        Initializes a new house with predefined attributes.

        name: Name of the house
        position: Position (x, y) of the house
        can_overlap: Boolean indicating if the house can overlap with other objects
        sprite: The path to the image of the house
        state: State of the house, True or False
        """
        super().__init__(name, position, can_overlap, sprite)  # Initializes the different attributes of Prop
        self.state = state  # State of the house
