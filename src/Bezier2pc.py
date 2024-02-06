import pygame
import numpy as np
import random

# Initialisation de Pygame
# pygame.init()
#
# # Configuration de la fenêtre
# grid_size = 32 * 16  # 16 cases de 16 pixels
# window = pygame.display.set_mode((grid_size, grid_size))
# pygame.display.set_caption('Courbe de Bézier Cubique avec Points de Contrôle Aléatoires')


def calculate_bezier_point(t, P0, P1, P2, P3):
    """
    Calcule un point sur une courbe de Bézier cubique à un temps t donné.
    P0, P1, P2, P3 sont les points de départ, les points de contrôle et le point d'arrivée respectivement.
    """
    return (P0 * (1 - t) ** 3 + 3 * P1 * t * (1 - t) ** 2 + 3 * P2 * (1 - t) * t ** 2 + P3 * t ** 3)


def generate_bezier_curve(control_points, num_points=100):
    """
    Génère les points d'une courbe de Bézier cubique basée sur les points de contrôle donnés.
    """
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        x = calculate_bezier_point(t, control_points[0][0], control_points[1][0], control_points[2][0],
                                   control_points[3][0])
        y = calculate_bezier_point(t, control_points[0][1], control_points[1][1], control_points[2][1],
                                   control_points[3][1])
        points.append((int(x), int(y)))
    return points


def fill_grid_with_texture_and_adjacent(surface, points, texture, grid_size):
    """
    Remplit les cases de la grille et leurs voisins adjacents avec une texture basée sur les points donnés.
    """
    filled_cells = set()
    for x, y in points:
        cell_x, cell_y = x // 16 * 16, y // 16 * 16
        filled_cells.add((cell_x, cell_y))

    # Ajouter les cases adjacentes aux cases remplies
    adjacent_cells = set()
    for cell_x, cell_y in filled_cells:
        for dx in [-16, 0, 16]:
            for dy in [-16, 0, 16]:
                new_x, new_y = cell_x + dx, cell_y + dy
                # Vérifier si la nouvelle case est dans les limites de la grille
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                    adjacent_cells.add((new_x, new_y))

    # Combiner les cases initialement remplies avec leurs voisins adjacents
    all_cells_to_fill = filled_cells.union(adjacent_cells)

    # Remplir toutes les cases sélectionnées avec la texture
    for cell_x, cell_y in all_cells_to_fill:
        surface.blit(texture, (cell_x, cell_y))

def fill_grid_with_texture(surface, points, texture):
    """
    Remplit les cases de la grille avec une texture basée sur les points donnés.
    """
    filled_cells = set()
    for x, y in points:
        cell_x, cell_y = x // 16 * 16, y // 16 * 16
        if (cell_x, cell_y) not in filled_cells:
            surface.blit(texture, (cell_x, cell_y))
            filled_cells.add((cell_x, cell_y))


def select_edge_point(grid_size):
    """
    Sélectionne un point aléatoire sur le bord de la fenêtre.
    """
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        return random.randint(0, grid_size), 0
    elif edge == 'bottom':
        return random.randint(0, grid_size), grid_size
    elif edge == 'left':
        return 0, random.randint(0, grid_size)
    elif edge == 'right':
        return grid_size, random.randint(0, grid_size)


# # Définition du bouton
button_color = (200, 0, 0)  # Vert
# button_position = (0, 0)  # Position du bouton dans la fenêtre
# button_size = (64, 32)  # Taille du bouton
# button_text = 'Reset'

# Fonction pour dessiner le bouton
def draw_button(surface, position, size, text):
    font = pygame.font.Font(None, 24)  # Utilisez pygame.font.Font(None, taille) pour la police par défaut
    text_render = font.render(text, True, (255, 255, 255))
    rect = pygame.Rect(position, size)
    surface.fill(button_color, rect)
    text_rect = text_render.get_rect(center=rect.center)
    surface.blit(text_render, text_rect)
    return rect  # Retourne le rectangle du bouton pour la détection de clic


# Vérifie si un point est à l'intérieur d'un rectangle
def is_point_inside_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


# grass_texture = pygame.image.load('../LandsImg/grass1.png').convert()
# grass_texture = pygame.transform.scale(grass_texture, (16, 16))
# water_texture = pygame.image.load('../LandsImg/water.png').convert()
# water_texture = pygame.transform.scale(water_texture, (16, 16))
#
# start_point = select_edge_point(grid_size)
# end_point = select_edge_point(grid_size)
#
# control_point1 = (random.randint(0, grid_size), random.randint(0, grid_size))
# control_point2 = (random.randint(0, grid_size), random.randint(0, grid_size))
# control_points = [start_point, control_point1, control_point2, end_point]
#
# # Boucle principale
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             # Vérifie si le clic est sur le bouton
#             if is_point_inside_rect(event.pos, button_rect):
#                 start_point = select_edge_point(grid_size)
#                 end_point = select_edge_point(grid_size)
#
#                 control_point1 = (random.randint(0, grid_size), random.randint(0, grid_size))
#                 control_point2 = (random.randint(0, grid_size), random.randint(0, grid_size))
#                 control_points = [start_point, control_point1, control_point2, end_point]
#
#     for x in range(0, grid_size, 16):
#         for y in range(0, grid_size, 16):
#             window.blit(grass_texture, (x, y))
#
#     # Génère des points de contrôle aléatoires
#     # Génère et remplit les cases basées sur la courbe de Bézier
#     bezier_points = generate_bezier_curve(control_points)
#     fill_grid_with_texture_and_adjacent(window, bezier_points, water_texture, grid_size)
#     button_rect = draw_button(window, button_position, button_size, button_text)
#
#     pygame.display.flip()
#
# pygame.quit()
