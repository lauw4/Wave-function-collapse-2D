from Land import Land


class Tile:
    def __init__(self,img_path,lands_):
        self.imgPath = img_path
        self.lands = lands_

    def getLand(self,side):
        land = None
        if side == 'N':
            land = 0
        elif side == 'E':
            land = 1
        elif side == 'S':
            land = 2
        elif side == 'W':
            land = 3

        if land is not None:
            return self.lands[land]

        raise TypeError

#N E S W
Tile('', [Land.GRASS, Land.GRASS, Land.GRASS, Land.GRASS])

