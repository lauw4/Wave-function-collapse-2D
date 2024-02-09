import numpy as np
from math import comb


def calculate_bezier_curve(control_points, t):
    control_points = np.array(control_points)
    n = len(control_points) - 1
    bezier_curve = np.zeros((len(t), 2))
    for i in range(len(t)):
        ti = t[i]
        bezier_point = np.array([0.0, 0.0])
        for j in range(n + 1):
            bin_coeff = comb(n, j)
            bezier_point += bin_coeff * (1 - ti) ** (n - j) * ti ** j * control_points[j]
        bezier_curve[i, :] = bezier_point
    return bezier_curve
