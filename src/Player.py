import pygame as pg
from character import *

class Player (Character):
    def __init__(self):
        super().__init__()


# get tile where the player is standing (Class mapp.getland) 
# get the sides of the tile if they are road or not (y-1.map.getland)
# if there is a road in there move to the road tile
# check if the road in on the edge of the map (have less than 4 neighbours)

