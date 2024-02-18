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

path = ["segments/segment_0_0.png", "segments/segment_0_1.png",
        "segments/segment_0_2.png", "segments/segment_1_0.png",
        "segments/segment_1_1.png", "segments/segment_1_2.png",
        ]

water = "../LandsImg/water.png"

# Liste des chemins d'accès aux images
images = [water,
          path[0],
          path[3],

          water,
          path[1],
          path[4],

          water,
          path[2],
          path[5],
          ]

# Créer la grille et enregistrer l'image
image_finale = creer_grille(images)
image_finale.save("test.png")
