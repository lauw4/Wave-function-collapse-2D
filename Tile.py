import csv

from PIL import Image


class Tile:
    def __init__(self, name_, img_path_, lands_):
        self.name = name_
        self.img_path = img_path_
        self.lands = lands_

    def getLand(self, side):
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
        self_side_attr = self.getLand(side)
        other_side_attr = other_tile.getLand(opposite_sides[side])

        # Comparer les attributs
        return self_side_attr == other_side_attr

    def show(self):
        try:
            with Image.open(self.img_path) as img:
                img.show()
        except IOError:
            print(f"Unable to open the image {self.img_path}")


def read_tiles_from_csv(file_path_):
    tiles_ = []
    with open(file_path_, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            lands = [row['NW'], row['N'], row['NE'],
                     row['W'], row['C'], row['E'],
                     row['SW'], row['S'], row['SE']]
            tile_ = Tile(row['Name'], "img/" + row['Path'], lands)
            tiles_.append(tile_)
    return tiles_
