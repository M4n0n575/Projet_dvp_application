import pygame
from Personnage import Personnage

# --- 1. CONFIGURATION ---
TAILLE_CASE = 60
GRILLE_TAILLE = 10
LARGEUR, HAUTEUR = GRILLE_TAILLE * TAILLE_CASE, GRILLE_TAILLE * TAILLE_CASE

COULEURS = {
    0: (255, 255, 255), # Sol
    1: (40, 44, 52),    # Mur
    2: (46, 204, 113),  # Départ
    3: (231, 76, 60),   # Arrivée
}

# --- 2. LES NIVEAUX ---
map1 = [
    [2, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 3]
]

map2 = [
    [2, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 3, 1]
]

tous_les_niveaux = [map1, map2]
indice_niveau = 0

# --- 3. INITIALISATION ---
pygame.init()
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Labyrinthe - Atteignez l'arrivée !")

def trouver_depart(matrice):
    for l in range(GRILLE_TAILLE):
        for c in range(GRILLE_TAILLE):
            if matrice[l][c] == 2: return c, l
    return 0, 0

# Création du joueur au départ du niveau 1
x_d, y_d = trouver_depart(tous_les_niveaux[indice_niveau])
joueur = Personnage(100, 100, 1, x_d, y_d)

fin_affichage_map = pygame.time.get_ticks() + 5000
fin_ecran_rouge = 0
en_pause = False

def dessiner_interface():
    # Barre de vie
    pygame.draw.rect(screen, (50, 50, 50), (10, 10, 200, 20))
    largeur_vie = max(0, (joueur.vie / joueur.vie_max) * 200)
    pygame.draw.rect(screen, (46, 204, 113), (10, 10, largeur_vie, 20))

def dessiner_tout(matrice):
    for l in range(GRILLE_TAILLE):
        for c in range(GRILLE_TAILLE):
            val = matrice[l][c]
            pygame.draw.rect(screen, COULEURS.get(val, (255,255,255)), (c*60, l*60, 60, 60))
    # Personnage
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
            
            # On ne bouge que si la map est cachée et qu'on n'est pas en pause
            if not map_visible and not en_pause:
                vie_avant = joueur.vie
                if event.key == pygame.K_z: joueur.deplacement(0, -1, matrice_actuelle)
                if event.key == pygame.K_s: joueur.deplacement(0, 1, matrice_actuelle)
                if event.key == pygame.K_q: joueur.deplacement(-1, 0, matrice_actuelle)
                if event.key == pygame.K_d: joueur.deplacement(1, 0, matrice_actuelle)
                
                # Effet flash rouge si on a touché un mur (vie a baissé)
                if joueur.vie < vie_avant:
                    fin_ecran_rouge = temps_actuel + 200
                
                # VÉRIFICATION ARRIVÉE (Case 3)
                if matrice_actuelle[joueur.y][joueur.x] == 3:
                    # 1. On passe au niveau suivant (boucle si fini)
                    indice_niveau = (indice_niveau + 1) % len(tous_les_niveaux)
                    # 2. On repositionne le joueur au nouveau départ
                    nx, ny = trouver_depart(tous_les_niveaux[indice_niveau])
                    joueur.x, joueur.y = nx, ny
                    # 3. On réaffiche la carte pour 5 secondes
                    fin_affichage_map = pygame.time.get_ticks() + 5000

    joueur.update_ko()
    screen.fill((0, 0, 0))
    
    if not en_pause:
        dessiner_tout(matrice_actuelle)
        
        # Si la map doit être cachée, on dessine le cercle de lumière
        if not map_visible:
            obs = pygame.Surface((LARGEUR, HAUTEUR))
            obs.fill((10,10,10))
            pygame.draw.circle(obs, (255,255,255), (joueur.x*60+30, joueur.y*60+30), 40)
            obs.set_colorkey((255,255,255))
            screen.blit(obs, (0,0))
        else:
            # Message d'attente
            font = pygame.font.SysFont("Arial", 30, bold=True)
            txt = font.render("MÉMORISEZ !", True, (0, 0, 0))
            screen.blit(txt, (LARGEUR//2 - 80, 20))

        if temps_actuel < fin_ecran_rouge:
            s = pygame.Surface((LARGEUR, HAUTEUR))
            s.fill((255,0,0)); s.set_alpha(100); screen.blit(s, (0,0))
            
        dessiner_interface()
    
    pygame.display.flip()

pygame.quit()