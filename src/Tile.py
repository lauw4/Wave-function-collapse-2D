class Tile2:
    def __init__(self, name_, img_path_, lands_):
        """
        Initializes a Tile2 object with a name, image path, and land types for each side.

        Parameters:
        - name_ (str): The name of the tile.
        - img_path_ (str): The path to the tile's image.
        - lands_ (list): A list of land types for each side of the tile, including diagonals. The list order
                         follows: [North, West, East, South, Northwest, Northeast, Southwest, Southeast].

        This constructor sets up the basic properties of a tile, including its visual representation
        and the types of lands it can connect to on each side.
        """
        self.name = name_
        self.img_path = img_path_
        self.lands = lands_

    def get_land(self, side):
        """
        Returns the land type of the specified side of the tile.

        Parameters:
        - side (str): The side for which to get the land type. Valid sides are 'N', 'W', 'E', 'S',
                      'NW', 'NE', 'SW', 'SE'.

        Returns:
        - The land type of the specified side.

        Raises:
        - ValueError: If an invalid side is specified.

        This method allows querying the type of land on a specific side of the tile, which is useful
        for determining compatibility with adjacent tiles.
        """
        sides = {'N': 0, 'W': 1, 'E': 2, 'S': 3, 'NW': 4, 'NE': 5, 'SW': 6, 'SE': 7}
        land_index = sides.get(side)
        if land_index is not None:
            return self.lands[land_index]
        raise ValueError("Invalid side")

    def can_place_next_to(self, other_tile, side):
        """
        Determines whether the tile can be placed next to another tile on the specified side.

        Parameters:
        - other_tile (Tile2): The other tile to compare against.
        - side (str): The side of this tile being compared. Valid sides are 'N', 'W', 'E', 'S',
                      'NW', 'NE', 'SW', 'SE'.

        Returns:
        - bool: True if the tiles are compatible on the specified sides; otherwise, False.

        This method checks if the current tile's specified side matches the opposite side of another tile,
        indicating whether the two tiles can be placed next to each other.
        """
        # Définir les côtés opposés
        opposite_sides = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E', 'NW': 'SE', 'NE': 'SW', 'SW': 'NE', 'SE': 'NW'}

        # Obtenir les attributs des côtés à comparer
        self_side_attr = self.get_land(side)
        other_side_attr = other_tile.get_land(opposite_sides[side])

        # Comparer les attributs
        return self_side_attr == other_side_attr