import csv
import math

import numpy as np

from TEST import WFC2
from Tile2 import Tile2


def bezier_curve(control_points, num_points):
    n = len(control_points) - 1
    t = np.linspace(0, 1, num_points)
    curve_points = np.zeros((num_points, 2))

    for i in range(num_points):
        point = np.zeros(2)
        for j in range(n + 1):
            point += control_points[j] * binomial_coefficient(n, j) * ((1 - t[i]) ** (n - j)) * (t[i] ** j)
        curve_points[i] = point

    return curve_points


def binomial_coefficient(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def is_below_curve(point, curve_points):
    x, y = point[0], point[1]
    return y > np.interp(x, curve_points[:, 0], curve_points[:, 1])


def read_tiles_from_csv(filename):
    tiles_ = []
    with open(filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            lands = [row['N'], row['W'], row['E'], row['S'],
                     row['NW'], row['NE'], row['SW'], row['SE']]
            tile_ = Tile2(row['Name'], "data/imgs2/" + row['Path'], lands)
            tiles_.append(tile_)
    return tiles_


# Example grid dimensions
n = 10
grid_size = (n, n)

# Example control points (you can adjust these)
start_point = np.array([0, np.random.randint(0, n)])  # Start point on left side
end_point = np.array([n - 1, np.random.randint(0, n)])  # End point on right side
control_point1 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 1
control_point2 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 2
control_point3 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 2

control_points = np.array([start_point, control_point1, control_point2, control_point2, end_point])
num_points = 100  # Number of points on the curve

# Calculate the Bézier curve
curve = bezier_curve(control_points, num_points)

tiles = read_tiles_from_csv("data/test3.csv")
grid = [[set(range(len(tiles))) for _ in range(grid_size[1])] for _ in range(grid_size[0])]

# Fill the grid with the Bézier curve
for point in curve:
    x, y = int(round(point[0])), int(round(point[1]))
    if 0 <= x < n and 0 <= y < n:
        grid[y][x] = {-}

    adjacent_offsets_water = [-1, 0, 1]
    for dx in adjacent_offsets_water:
        for dy in adjacent_offsets_water:
            if dx == 0 and dy == 0:
                continue
            adjacent_x, adjacent_y = x + dx, y + dy
            if 0 <= adjacent_x < n * 3 and 0 <= adjacent_y < n * 3:
                grid[y][x] = {6}


# Mark points below the curve as -2
for y in range(n):
    for x in range(n):
        if is_below_curve([x, y], curve):
            grid[y][x] = {13}

# for row in grid:
#     print(row)

wfc = WFC2("data/test3.csv", grid_size)
wfc.grid = grid
wfc.tiles_ = tiles

for row in wfc.grid:
    print(row)

wfc.run_collapse()

for row in wfc.grid:
    print(row)