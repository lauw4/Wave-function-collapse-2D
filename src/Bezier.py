import math
import random

import numpy as np


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


def is_below_curve(point, curve_points, offset):
    distances = np.sqrt((curve_points[:, 0] - point[0]) ** 2 + (curve_points[:, 1] - point[1]) ** 2)

    # Vérifier si la distance minimale est inférieure ou égale à l'offset
    return np.min(distances) <= offset


def select_edge_point(n):
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        return random.randint(0, n - 1), 0
    elif edge == 'bottom':
        return random.randint(0, n - 1), n - 1
    elif edge == 'left':
        return 0, random.randint(0, n - 1)
    elif edge == 'right':
        return n - 1, random.randint(0, n - 1)


def generate_control_points(n):
    num_internal_points = 2

    start_point = select_edge_point(n)
    end_point = select_edge_point(n)
    internal_points = [np.array([np.random.randint(0, n), np.random.randint(0, n)]) for _ in range(num_internal_points)]

    control_points_ = np.array([start_point] + internal_points + [end_point])
    return control_points_
