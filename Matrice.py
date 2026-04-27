import pygame
from Personnage import Personnage

# --- 1. CONFIGURATION ---
TAILLE_CASE = 60
GRILLE_TAILLE = 10
LARGEUR = GRILLE_TAILLE * TAILLE_CASE
HAUTEUR = GRILLE_TAILLE * TAILLE_CASE

COULEURS = {
    0: (255, 255, 255), 1: (40, 44, 52), 2: (46, 204, 113),
    3: (231, 76, 60), 4: (155, 89, 182), 5: (241, 196, 15),
}

# --- 2. LES NIVEAUX ---
map1 = [
    [2, 0, 1, 0, 5, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 4, 0, 5, 1, 0], [0, 0, 5, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0], [0, 5, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 5, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 0, 1, 4, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 3]
]
tous_les_niveaux = [map1]
indice_niveau = 0

# --- 3. INITIALISATION ---
pygame.init()
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Labyrinthe - Bloqué tant que la map est visible !")

def trouver_depart(matrice):
    for l in range(GRILLE_TAILLE):
        for c in range(GRILLE_TAILLE):
            if matrice[l][c] == 2: return c, l
    return 0, 0

x_d, y_d = trouver_depart(tous_les_niveaux[indice_niveau])
joueur = Personnage(100, 100, 1, x_d, y_d)

en_pause = False
fin_affichage_map = pygame.time.get_ticks() + 5000
fin_ecran_rouge = 0

def dessiner_interface():
    # Fond de la barre (gris foncé)
    pygame.draw.rect(screen, (50, 50, 50), (10, 10, 200, 20))
    # Calcul de la largeur selon la vie
    largeur_vie = (joueur.vie / joueur.vie_max) * 200
    # Couleur dynamique (Vert -> Orange -> Rouge)
    couleur = (46, 204, 113) if joueur.vie > 50 else (231, 76, 60)
    pygame.draw.rect(screen, couleur, (10, 10, largeur_vie, 20))
    # Bordure
    pygame.draw.rect(screen, (255, 255, 255), (10, 10, 200, 20), 2)

def dessiner_lumiere(x, y):
    obscurite = pygame.Surface((LARGEUR, HAUTEUR))
    obscurite.fill((10, 10, 10))
    cx, cy = x * TAILLE_CASE + 30, y * TAILLE_CASE + 30
    pygame.draw.circle(obscurite, (255, 255, 255), (cx, cy), 40)
    obscurite.set_colorkey((255, 255, 255))
    screen.blit(obscurite, (0, 0))

def dessiner_tout(matrice):
    for l in range(GRILLE_TAILLE):
        for c in range(GRILLE_TAILLE):
            val = matrice[l][c]
            rect = (c * TAILLE_CASE, l * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(screen, COULEURS[val] if val <= 3 else COULEURS[0], rect)
    # Joueur
    pygame.draw.circle(screen, (52, 152, 219), (joueur.x*60+30, joueur.y*60+30), 20)

# --- 4. BOUCLE PRINCIPALE ---
continuer = True
while continuer:
    temps_actuel = pygame.time.get_ticks()
    matrice_actuelle = tous_les_niveaux[indice_niveau]
    map_visible = temps_actuel < fin_affichage_map

    for event in pygame.event.get():
        if event.type == pygame.QUIT: continuer = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: en_pause = not en_pause
            
            # CONDITION : Pas en pause ET Map cachée
            if not en_pause and not map_visible:
                collision = False
                if event.key == pygame.K_z: collision = joueur.deplacement(0, -1, matrice_actuelle)
                if event.key == pygame.K_s: collision = joueur.deplacement(0, 1, matrice_actuelle)
                if event.key == pygame.K_q: collision = joueur.deplacement(-1, 0, matrice_actuelle)
                if event.key == pygame.K_d: collision = joueur.deplacement(1, 0, matrice_actuelle)
                
                if collision:
                    fin_ecran_rouge = temps_actuel + 200

    joueur.update_ko()
    screen.fill((0, 0, 0))
    
    if not en_pause:
        dessiner_tout(matrice_actuelle)
        if not map_visible:
            dessiner_lumiere(joueur.x, joueur.y)
        
        if temps_actuel < fin_ecran_rouge:
            flash = pygame.Surface((LARGEUR, HAUTEUR))
            flash.fill((255, 0, 0))
            flash.set_alpha(120)
            screen.blit(flash, (0,0))
            
        dessiner_interface()
    
    pygame.display.flip()
pygame.quit()