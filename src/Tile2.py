class Tile2:
    def __init__(self, name_, img_path_, lands_):
        self.name = name_
        self.img_path = img_path_
        self.lands = lands_

    def get_land(self, side):
        sides = {'N': 0, 'W': 1, 'E': 2, 'S': 3, 'NW': 4, 'NE': 5, 'SW': 6, 'SE': 7}
        land_index = sides.get(side)
        if land_index is not None:
            return self.lands[land_index]
        raise ValueError("Invalid side")

    def can_place_next_to(self, other_tile, side):
        # Définir les côtés opposés
        opposite_sides = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E', 'NW': 'SE', 'NE': 'SW', 'SW': 'NE', 'SE': 'NW'}

        # Obtenir les attributs des côtés à comparer
        self_side_attr = self.get_land(side)
        other_side_attr = other_tile.get_land(opposite_sides[side])

        # Comparer les attributs
        return self_side_attr == other_side_attr
