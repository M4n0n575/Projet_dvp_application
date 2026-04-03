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
    4: (155, 89, 182),   # Monstre (Violet)
    5: (241, 196, 15),   # Bonus (Jaune)
}

# --- 2. LES NIVEAUX ---
map1 = [
    [2, 0, 1, 0, 5, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 4, 0, 5, 1, 0],
    [0, 0, 5, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 5, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 0, 1, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 3]
]

map2 = [
    [2, 1, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [5, 1, 4, 1, 0, 5, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 3, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 5],
    [0, 0, 0, 1, 5, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 5, 0, 0, 0, 0, 0, 5, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
]

tous_les_niveaux = [map1, map2]
indice_niveau = 0 

# --- 3. INITIALISATION ---
pygame.init()
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Labyrinthe - P: Pause | ESPACE: Suivant | B: Révéler")

# Chronomètres
temps_restant_affichage = 5000  # 5 secondes au début
fin_affichage_map = pygame.time.get_ticks() + temps_restant_affichage
fin_ecran_rouge = 0
fin_ecran_bonus = 0

en_pause = False

def dessiner_bonus(x, y):
    centre = (x + TAILLE_CASE // 2, y + TAILLE_CASE // 2)
    pygame.draw.circle(screen, (211, 160, 0), centre, 15)
    pygame.draw.circle(screen, COULEURS[5], centre, 12)

def dessiner_tout(matrice_actuelle):
    for l in range(GRILLE_TAILLE):
        for c in range(GRILLE_TAILLE):
            valeur = matrice_actuelle[l][c]
            x, y = c * TAILLE_CASE, l * TAILLE_CASE
            rect = (x, y, TAILLE_CASE, TAILLE_CASE)
            
            couleur_fond = COULEURS[valeur] if valeur <= 3 else COULEURS[0]
            pygame.draw.rect(screen, couleur_fond, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)
            
            if valeur == 4: # Monstre
                pygame.draw.rect(screen, COULEURS[4], (x+10, y+10, 40, 40))
            elif valeur == 5: # Bonus
                dessiner_bonus(x, y)

def afficher_menu_pause():
    # Overlay semi-transparent
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0,0))
    
    # Texte
    font_titre = pygame.font.SysFont("Arial", 60, bold=True)
    font_sous_titre = pygame.font.SysFont("Arial", 25)
    
    surf_pause = font_titre.render("PAUSE", True, (255, 255, 255))
    surf_tuto = font_sous_titre.render("Appuyez sur P pour reprendre", True, (200, 200, 200))
    
    screen.blit(surf_pause, (LARGEUR // 2 - surf_pause.get_width() // 2, HAUTEUR // 2 - 50))
    screen.blit(surf_tuto, (LARGEUR // 2 - surf_tuto.get_width() // 2, HAUTEUR // 2 + 30))

# --- 4. BOUCLE PRINCIPALE ---
continuer = True
while continuer:
    temps_actuel = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                en_pause = not en_pause
                if en_pause:
                    # On calcule combien de temps il restait avant de cacher la map
                    temps_restant_affichage = max(0, fin_affichage_map - temps_actuel)
                else:
                    # On relance le chrono avec le temps qu'il restait
                    fin_affichage_map = pygame.time.get_ticks() + temps_restant_affichage

            # Les touches de jeu ne fonctionnent que si on n'est PAS en pause
            if not en_pause:
                if event.key == pygame.K_SPACE:
                    indice_niveau = (indice_niveau + 1) % len(tous_les_niveaux)
                    fin_affichage_map = temps_actuel + 5000
                    
                if event.key == pygame.K_b:
                    fin_affichage_map = temps_actuel + 2000 
                    
                if event.key == pygame.K_m:
                    fin_ecran_rouge = temps_actuel + 2000
                if event.key == pygame.K_l:
                    fin_ecran_bonus = temps_actuel + 500

    # --- 5. GESTION DE L'AFFICHAGE ---
    screen.fill((0, 0, 0)) # Fond noir
    
    if not en_pause:
        # Affichage du jeu normal
        if temps_actuel < fin_ecran_bonus:
            screen.fill((46, 204, 113)) 
        elif temps_actuel < fin_ecran_rouge:
            screen.fill((255, 0, 0))    
        elif temps_actuel < fin_affichage_map:
            dessiner_tout(tous_les_niveaux[indice_niveau])
    else:
        # Si on est en pause, on dessine quand même la map (si elle était visible)
        # Mais par dessus, on met le menu de pause
        if temps_restant_affichage > 0:
            dessiner_tout(tous_les_niveaux[indice_niveau])
        afficher_menu_pause()
    
    pygame.display.flip()

pygame.quit()