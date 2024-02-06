import random


def select_edge_point(grid_size):
    """
    Sélectionne un point aléatoire sur le bord de la fenêtre.
    """
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        return random.randint(0, grid_size - 1), 0
    elif edge == 'bottom':
        return random.randint(0, grid_size - 1), grid_size - 1
    elif edge == 'left':
        return 0, random.randint(0, grid_size - 1)
    elif edge == 'right':
        return grid_size - 1, random.randint(0, grid_size - 1)
