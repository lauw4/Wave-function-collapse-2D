from PIL import Image


def decouper_image(source, taille_segment=(16, 16)):
    # Charger l'image source
    image = Image.open(source)
    largeur, hauteur = image.size

    # Calculer le nombre de segments horizontaux et verticaux
    segments_x = largeur // taille_segment[0]
    segments_y = hauteur // taille_segment[1]

    import os
    dossier_segments = 'segments'
    if not os.path.exists(dossier_segments):
        os.makedirs(dossier_segments)

    # Découper l'image en segments et les enregistrer
    for x in range(segments_x):
        for y in range(segments_y):
            # Définir les coordonnées du segment
            gauche = x * taille_segment[0]
            haut = y * taille_segment[1]
            droite = gauche + taille_segment[0]
            bas = haut + taille_segment[1]

            # Découper le segment
            segment = image.crop((gauche, haut, droite, bas))

            # Enregistrer le segment
            nom_fichier = f"{dossier_segments}/Icon_{x}_{y}.png"
            segment.save(nom_fichier)

    print(f"Image découpée en segments de {taille_segment[0]}x{taille_segment[1]} pixels.")


# Exemple d'utilisation
source = 'UiIcons.png'  # Remplacez par le chemin de votre image
decouper_image(source)
