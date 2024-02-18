import numpy as np
import math
import random

import pygame

from TEST import WFC2


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


# Example grid dimensions
n = 40

# Example control points (you can adjust these)
start_point = np.array([0, np.random.randint(0, n)])  # Start point on left side
end_point = np.array([n - 1, np.random.randint(0, n)])  # End point on right side
control_point1 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 1
control_point2 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 2
control_point3 = np.array([np.random.randint(1, n - 2), np.random.randint(0, n)])  # Control point 2

control_points = np.array([start_point, control_point1, control_point2, control_point2,  end_point])
num_points = 100  # Number of points on the curve

# Calculate the Bézier curve
curve = bezier_curve(control_points, num_points)

# Example grid land_layer
land_layer = [[{-1} for _ in range(n)] for _ in range(n)]

# Fill the grid with the Bézier curve
for point in curve:
    x, y = int(round(point[0])), int(round(point[1]))
    if 0 <= x < n and 0 <= y < n:
        land_layer[y][x] = {5}

# Mark points below the curve as -2
for y in range(n):
    for x in range(n):
        if is_below_curve([x, y], curve):
            land_layer[y][x] = {-2}

# Print the grid
for row in land_layer:
    print(row)

grass_textures = ["LandsImg/grass2.png",
                  "LandsImg/grass2_1.png",
                  "LandsImg/grass2_2.png"]
road_textures = [
    "LandsImg/vertical_path.png"]
water_textures = ["LandsImg/water.png"]

wfc = WFC2("data/test3.csv", grid_size=(48, 48))

wfc.run_collapse()

pygame.init()
window = pygame.display.set_mode((n*16,n*16))
pygame.display.set_caption('WFC Test')

terrain_grid = [[random.choice(grass_textures) if land == {-1}
                 else random.choice(road_textures) if land == {5}
else random.choice(water_textures) if land == {-2}
else land for land in row] for row in land_layer]

lands = [[pygame.image.load(path).convert() for path in row] for row in terrain_grid]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    [window.blit(image, (col_index * 16, row_index * 16))
     for row_index, row in enumerate(lands)
     for col_index, image in enumerate(row)]

    pygame.display.flip()
