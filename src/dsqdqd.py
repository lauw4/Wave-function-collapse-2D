import csv
import math
import random

import numpy as np

# Example grid dimensions
import src.River.Bezier2 as bz
from src.River.WFC2 import WFC2

n = 30
grid_size = (n, n)
num_points = 100
control_points = bz.generate_control_points(n)
curve = bz.bezier_curve(control_points, num_points)

control_points2 = bz.generate_control_points(n)
control_points2[0] = random.choice(curve)
curve2 = bz.bezier_curve(control_points2, num_points)

control_points3 = bz.generate_control_points(n)
curve3 = bz.bezier_curve(control_points3, num_points)

wfc = WFC2("data/test3.csv", grid_size)

for y in range(n):
    for x in range(n):
        if bz.is_below_curve([x, y], curve, 2) or bz.is_below_curve([x, y], curve2, 2):
            wfc.grid[y][x] = {13}
            wfc.update_neighbors(y, x)
        elif not (bz.is_below_curve([x, y], curve, 4) or bz.is_below_curve([x, y], curve2, 4)):
            wfc.grid[y][x] = {12}
            wfc.update_neighbors(y, x)

wfc.run_collapse()

