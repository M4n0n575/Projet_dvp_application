import pygame
from Personnage import Personnage

class Jeu:
    def __init__(self, screen, difficulte):
        self.screen = screen
        self.difficulte = difficulte # On pourra ajuster selon la difficulté plus tard
        self.TAILLE_CASE = 60
        self.GRILLE_TAILLE = 10
        self.LARGEUR = self.GRILLE_TAILLE * self.TAILLE_CASE
        self.HAUTEUR = self.GRILLE_TAILLE * self.TAILLE_CASE
        
        self.COULEURS = {
            0: (255, 255, 255), 1: (40, 44, 52), 2: (46, 204, 113),
            3: (231, 76, 60), 4: (155, 89, 182), 5: (241, 196, 15),
        }

        self.map1 = [
            [2, 0, 1, 0, 5, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 1, 4, 0, 5, 1, 0], [0, 0, 5, 0, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 0], [0, 5, 0, 0, 1, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 0, 5, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
            [1, 1, 1, 0, 1, 0, 1, 4, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 3]
        ]
        
        x_d, y_d = self.trouver_depart(self.map1)
        self.joueur = Personnage(100, 100, 1, x_d, y_d)
        
        self.en_pause = False
        self.fin_affichage_map = pygame.time.get_ticks() + 5000
        self.fin_ecran_rouge = 0
        self.running = True

    def trouver_depart(self, matrice):
        for l in range(self.GRILLE_TAILLE):
            for c in range(self.GRILLE_TAILLE):
                if matrice[l][c] == 2: return c, l
        return 0, 0

    def dessiner_interface(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, 200, 20))
        largeur_vie = (self.joueur.vie / self.joueur.vie_max) * 200
        couleur = (46, 204, 113) if self.joueur.vie > 50 else (231, 76, 60)
        pygame.draw.rect(self.screen, couleur, (10, 10, largeur_vie, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, 200, 20), 2)

    def dessiner_lumiere(self, x, y):
        obscurite = pygame.Surface((self.LARGEUR, self.HAUTEUR))
        obscurite.fill((10, 10, 10))
        cx, cy = x * self.TAILLE_CASE + 30, y * self.TAILLE_CASE + 30
        pygame.draw.circle(obscurite, (255, 255, 255), (cx, cy), 40)
        obscurite.set_colorkey((255, 255, 255))
        self.screen.blit(obscurite, (0, 0))

    def dessiner_tout(self, matrice):
        for l in range(self.GRILLE_TAILLE):
            for c in range(self.GRILLE_TAILLE):
                val = matrice[l][c]
                rect = (c * self.TAILLE_CASE, l * self.TAILLE_CASE, self.TAILLE_CASE, self.TAILLE_CASE)
                pygame.draw.rect(self.screen, self.COULEURS[val] if val <= 3 else self.COULEURS[0], rect)
        pygame.draw.circle(self.screen, (52, 152, 219), (self.joueur.x*60+30, self.joueur.y*60+30), 20)

    def update(self):
        temps_actuel = pygame.time.get_ticks()
        map_visible = temps_actuel < self.fin_affichage_map

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUITTER"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return "MENU"
                if event.key == pygame.K_p: self.en_pause = not self.en_pause
                
                if not self.en_pause and not map_visible:
                    collision = False
                    if event.key == pygame.K_z: collision = self.joueur.deplacement(0, -1, self.map1)
                    if event.key == pygame.K_s: collision = self.joueur.deplacement(0, 1, self.map1)
                    if event.key == pygame.K_q: collision = self.joueur.deplacement(-1, 0, self.map1)
                    if event.key == pygame.K_d: collision = self.joueur.deplacement(1, 0, self.map1)
                    
                    if collision:
                        self.fin_ecran_rouge = temps_actuel + 200

        self.joueur.update_ko()
        self.screen.fill((0, 0, 0))
        
        if not self.en_pause:
            self.dessiner_tout(self.map1)
            if not map_visible:
                self.dessiner_lumiere(self.joueur.x, self.joueur.y)
            
            if temps_actuel < self.fin_ecran_rouge:
                flash = pygame.Surface((self.LARGEUR, self.HAUTEUR))
                flash.fill((255, 0, 0))
                flash.set_alpha(120)
                self.screen.blit(flash, (0,0))
                
            self.dessiner_interface()
        
        return "JEU"