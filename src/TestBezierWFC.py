import random

from WFC import WFC
import pygame
import Bezier2pc

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


# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
grid_size = 20*3 * 16  # 16 cases de 16 pixels
window = pygame.display.set_mode((grid_size, grid_size))
pygame.display.set_caption('Courbe de Bézier Cubique avec Points de Contrôle Aléatoires')

wfc = WFC("../data/test2.csv", grid_size=(20, 20))
wfc.run_collapse()
img = wfc.get_final_grid_images()
print(img)
img = [pygame.image.load(path).convert() for path in img]
imgConvert = [pygame.transform.scale(x, (48, 48)) for x in img]
print(len(imgConvert))
print(imgConvert)


start_point = Bezier2pc.select_edge_point(grid_size)
end_point = Bezier2pc.select_edge_point(grid_size)

control_point1 = (random.randint(0, grid_size), random.randint(0, grid_size))
control_point2 = (random.randint(0, grid_size), random.randint(0, grid_size))
control_points = [start_point, control_point1, control_point2, end_point]

water_texture = pygame.image.load('../LandsImg/water.png').convert()
water_texture = pygame.transform.scale(water_texture, (16, 16))

button_color = (200, 0, 0)  # Vert
button_position = (0, 0)  # Position du bouton dans la fenêtre
button_size = (64, 32)  # Taille du bouton
button_text = 'Reset'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifie si le clic est sur le bouton
                if Bezier2pc.is_point_inside_rect(event.pos, button_rect):
                    start_point = Bezier2pc.select_edge_point(grid_size)
                    end_point = Bezier2pc.select_edge_point(grid_size)

                    control_point1 = (random.randint(0, grid_size), random.randint(0, grid_size))
                    control_point2 = (random.randint(0, grid_size), random.randint(0, grid_size))
                    control_points = [start_point, control_point1, control_point2, end_point]

    for idx, image in enumerate(imgConvert):
        row = idx // 20
        col = idx % 20
        x = col * 48
        y = row * 48
        # Blitter l'image à sa position
        window.blit(image, (x, y))

    bezier_points = Bezier2pc.generate_bezier_curve(control_points)
    Bezier2pc.fill_grid_with_texture_and_adjacent(window, bezier_points, water_texture, grid_size)
    button_rect = Bezier2pc.draw_button(window, button_position, button_size, button_text)
    pygame.display.flip()

pygame.quit()
