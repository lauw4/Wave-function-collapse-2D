import pygame
import math
import random

def calculate_bezier_point(t, control_points):
    n = len(control_points) - 1
    x = y = 0.0
    for i, point in enumerate(control_points):
        binomial_coefficient = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
        x += binomial_coefficient * ((1 - t) ** (n - i)) * (t ** i) * point[0]
        y += binomial_coefficient * ((1 - t) ** (n - i)) * (t ** i) * point[1]
    return (int(x), int(y))

def generate_bezier_points(control_points, num_points=100):
    return [calculate_bezier_point(t / num_points, control_points) for t in range(num_points + 1)]

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
grid_size = 16 * 16
window = pygame.display.set_mode((grid_size, grid_size))
pygame.display.set_caption('Courbe de Bézier avec remplissage d\'image - Point de Contrôle Aléatoire')

# Chargement et redimensionnement de l'image water.png
water_texture = pygame.image.load('img/water.png').convert()
water_texture = pygame.transform.scale(water_texture, (16, 16))

def fill_grid_with_texture(surface, points, texture):
    filled_cells = set()
    for x, y in points:
        cell_x, cell_y = x // 16 * 16, y // 16 * 16
        if (cell_x, cell_y) not in filled_cells:
            surface.blit(texture, (cell_x, cell_y))
            filled_cells.add((cell_x, cell_y))

# Boucle principale

pc = (random.randint(0, grid_size), random.randint(0, grid_size))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Définition aléatoire des points de contrôle de la courbe de Bézier
    control_points = [(0, 0), pc, (256, 256)]
    bezier_points = generate_bezier_points(control_points)

    window.fill((0, 0, 0))  # Nettoie l'écran
    fill_grid_with_texture(window, bezier_points, water_texture)  # Remplir les cases affectées sans afficher la courbe

    pygame.display.flip()

pygame.quit()
