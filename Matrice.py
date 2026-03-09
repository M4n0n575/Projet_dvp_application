import pygame

# --- 1. CONFIGURATION ---
TAILLE_CASE = 60
GRILLE_TAILLE = 10
LARGEUR = GRILLE_TAILLE * TAILLE_CASE
HAUTEUR = GRILLE_TAILLE * TAILLE_CASE

COULEURS = {
    0: (255, 255, 255),  # Sol
    1: (40, 44, 52),     # Mur
    2: (46, 204, 113),   # Départ
    3: (231, 76, 60),    # Arrivée
}

# --- 2. LES NIVEAUX ---
map1 = [
    [2, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 3]
]

map2 = [
    [2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 3, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]
#Liste contenant tous nos niveaux
tous_les_niveaux = [map1, map2]
indice_niveau = 0  # On commence au premier (index 0)

# --- 3. INITIALISATION ---
pygame.init()
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Labyrinthe - Appuyez sur ESPACE pour changer")

def dessiner_tout(matrice_actuelle):
    for l in range(GRILLE_TAILLE):
        for c in range(GRILLE_TAILLE):
            valeur = matrice_actuelle[l][c]
            rect = (c * TAILLE_CASE, l * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(screen, COULEURS[valeur], rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

# --- 4. BOUCLE PRINCIPALE ---
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
            
        # Détection de la touche ESPACE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # On passe au niveau suivant (et on revient au début si on dépasse)
                indice_niveau = (indice_niveau + 1) % len(tous_les_niveaux)
                print(f"Passage au niveau {indice_niveau + 1}")

    screen.fill((0, 0, 0))
    
    # On dessine le niveau correspondant à l'indice actuel
    dessiner_tout(tous_les_niveaux[indice_niveau])
    
    pygame.display.flip()

pygame.quit()  