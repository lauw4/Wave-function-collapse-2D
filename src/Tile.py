class Tile:
    def __init__(self, name_, img_path_, lands_):
        self.name = name_
        self.img_path = img_path_
        self.lands = lands_
        self.lands_3x3 = [[lands_[i * 3 + j] for j in range(3)] for i in range(3)]

    def get_land(self, side):
        sides = {'NW': 0, 'N': 1, 'NE': 2,
                 'W': 3, 'C': 4, 'E': 5,
                 'SW': 6, 'S': 7, 'SE': 8,
                 }
        land_index = sides.get(side)
        if land_index is not None:
            return self.lands[land_index]
        raise ValueError("Invalid side")

    def can_place_next_to(self, other_tile, side):
        # Définir les côtés opposés
        opposite_sides = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}

        # Obtenir les attributs des côtés à comparer
        self_side_attr = self.get_land(side)
        other_side_attr = other_tile.get_land(opposite_sides[side])

        # Comparer les attributs
        return self_side_attr == other_side_attr
