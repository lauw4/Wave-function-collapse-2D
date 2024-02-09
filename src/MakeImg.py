from PIL import Image


def creer_grille(images):
    # Taille de chaque image et de la grille
    taille_image = (256, 256)
    grille_taille = (3, 3)

    # Créer une nouvelle image pour la grille
    grille = Image.new('RGB', (taille_image[0] * grille_taille[0], taille_image[1] * grille_taille[1]))

    # Placer chaque image dans la grille
    for i, img in enumerate(images):
        # Ouvrir l'image
        image = Image.open(img)
        # Redimensionner si nécessaire
        if image.size != taille_image:
            image = image.resize(taille_image)
        # Calculer la position
        x = (i % grille_taille[0]) * taille_image[0]
        y = (i // grille_taille[0]) * taille_image[1]
        # Placer l'image
        grille.paste(image, (x, y))

    return grille


grass2_path = "../LandsImg/grass2.png"
horizontal_path = "../LandsImg/horizontal_path.png"
vertical_path = "../LandsImg/vertical_path.png"

# Liste des chemins d'accès aux images
images = [grass2_path,
          vertical_path,
          grass2_path,

          horizontal_path,
          horizontal_path,
          grass2_path,

          grass2_path,
          grass2_path,
          grass2_path,
          ]

# Créer la grille et enregistrer l'image
image_finale = creer_grille(images)
image_finale.save("imgs/turn_road_WN.png")
