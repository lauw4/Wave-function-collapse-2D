#prop.py

class Prop:
    def __init__(self, name: str, position: tuple, can_overlap: bool, sprite: str):
        self.name = name
        self.position = position
        self.can_overlap = can_overlap
        self.sprite = sprite