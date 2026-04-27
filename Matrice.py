import pygame
from Personnage import Personnage

# --- CONFIGURATION ---
TAILLE_CASE = 60
GRILLE_TAILLE = 10
LARGEUR, HAUTEUR = GRILLE_TAILLE * TAILLE_CASE, GRILLE_TAILLE * TAILLE_CASE

COULEURS = {
    0: (255, 255, 255), # Sol
    1: (40, 44, 52),    # Mur
    2: (46, 204, 113),  # Départ
    3: (231, 76, 60),   # Arrivée
}

class Jeu:
    def __init__(self, screen, difficulte):
        self.screen = screen
        self.difficulte = difficulte
        
        # --- INITIALISATION AUDIO ---
        pygame.mixer.init()
        try:
            self.son_victoire = pygame.mixer.Sound("Win.mp3")
            self.son_joue = False 
        except:
            print("Note : victoire.wav introuvable, le jeu restera silencieux.")
            self.son_victoire = None
            self.son_joue = False

        # --- GESTION DU CHRONO ---
        # Ajustement du temps selon la difficulté choisie dans le menu
        temps_secondes = 60 if difficulte == "FACILE" else 45 if difficulte == "MOYEN" else 30
        self.temps_limite = temps_secondes * 1000 
        self.debut_jeu = pygame.time.get_ticks()
        
        # --- NIVEAUX ---
        self.map1 = [
            [2, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
            [1, 1, 1, 0, 1, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 3]
        ]
        self.map2 = [
            [2, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 3, 1]
        ]
        
        self.tous_les_niveaux = [self.map1, self.map2]
        self.indice_niveau = 0
        self.victoire = False
        
        # --- INITIALISATION JOUEUR ---
        x_d, y_d = self.trouver_depart(self.tous_les_niveaux[self.indice_niveau])
        self.joueur = Personnage(100, 100, 1, x_d, y_d)
        
        self.fin_affichage_map = pygame.time.get_ticks() + 5000
        self.fin_ecran_rouge = 0

    def trouver_depart(self, matrice):
        for l in range(GRILLE_TAILLE):
            for c in range(GRILLE_TAILLE):
                if matrice[l][c] == 2: return c, l
        return 0, 0

    def dessiner_interface(self, temps_restant_ms):
        # Barre de vie
        pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, 200, 20))
        largeur_vie = max(0, (self.joueur.vie / self.joueur.vie_max) * 200)
        pygame.draw.rect(self.screen, (46, 204, 113), (10, 10, largeur_vie, 20))
        
        # Chrono
        secondes = max(0, temps_restant_ms // 1000)
        font_timer = pygame.font.SysFont("Arial", 24, bold=True)
        couleur_timer = (255, 255, 255) if secondes > 10 else (231, 76, 60)
        txt_timer = font_timer.render(f"TEMPS : {secondes}s", True, couleur_timer)
        self.screen.blit(txt_timer, (LARGEUR - 150, 10))

    def dessiner_victoire(self):
        # Overlay sombre
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Texte de victoire
        font_v = pygame.font.SysFont("Arial", 60, bold=True)
        txt_v = font_v.render("VICTOIRE !", True, (46, 204, 113))
        rect_v = txt_v.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 30))
        self.screen.blit(txt_v, rect_v)
        
        font_s = pygame.font.SysFont("Arial", 25)
        txt_s = font_s.render("Appuyez sur ESPACE pour le menu", True, (255, 255, 255))
        rect_s = txt_s.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 40))
        self.screen.blit(txt_s, rect_s)

    def update(self):
        temps_actuel = pygame.time.get_ticks()
        
        # --- ÉCRAN DE VICTOIRE ---
        if self.victoire:
            if self.son_victoire and not self.son_joue:
                self.son_victoire.play()
                self.son_joue = True
            
            self.dessiner_victoire()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUITTER"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return "MENU"
            return "JEU"

        # --- GESTION DU TEMPS ---
        temps_ecoule = temps_actuel - self.debut_jeu
        temps_restant = self.temps_limite - temps_ecoule
        if temps_restant <= 0: return "MENU"

        matrice_actuelle = self.tous_les_niveaux[self.indice_niveau]
        map_visible = temps_actuel < self.fin_affichage_map

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUITTER"
            
            if event.type == pygame.KEYDOWN:
                # Retour menu avec P ou Echap
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE: 
                    return "MENU"
                
                # Le joueur ne peut bouger que si la map est cachée et qu'il n'est pas KO
                if not map_visible and not self.joueur.ko:
                    vie_avant = self.joueur.vie
                    if event.key == pygame.K_z: self.joueur.deplacement(0, -1, matrice_actuelle)
                    if event.key == pygame.K_s: self.joueur.deplacement(0, 1, matrice_actuelle)
                    if event.key == pygame.K_q: self.joueur.deplacement(-1, 0, matrice_actuelle)
                    if event.key == pygame.K_d: self.joueur.deplacement(1, 0, matrice_actuelle)
                    
                    # Flash rouge si collision mur
                    if self.joueur.vie < vie_avant:
                        self.fin_ecran_rouge = temps_actuel + 200
                    
                    # Vérification Arrivée
                    if matrice_actuelle[self.joueur.y][self.joueur.x] == 3:
                        if self.indice_niveau < len(self.tous_les_niveaux) - 1:
                            self.indice_niveau += 1
                            nx, ny = self.trouver_depart(self.tous_les_niveaux[self.indice_niveau])
                            self.joueur.x, self.joueur.y = nx, ny
                            self.fin_affichage_map = pygame.time.get_ticks() + 5000
                        else:
                            self.victoire = True

        # --- DESSIN ---
        self.joueur.update_ko()
        self.screen.fill((0, 0, 0))
        
        # Labyrinthe et Joueur
        for l in range(GRILLE_TAILLE):
            for c in range(GRILLE_TAILLE):
                val = matrice_actuelle[l][c]
                pygame.draw.rect(self.screen, COULEURS.get(val, (255,255,255)), (c*60, l*60, 60, 60))
        
        pygame.draw.circle(self.screen, (52, 152, 219), (self.joueur.x*60+30, self.joueur.y*60+30), 20)
        
        # Brouillard de guerre (si phase de jeu)
        if not map_visible:
            obs = pygame.Surface((LARGEUR, HAUTEUR))
            obs.fill((10,10,10))
            pygame.draw.circle(obs, (255,255,255), (self.joueur.x*60+30, self.joueur.y*60+30), 40)
            obs.set_colorkey((255,255,255))
            self.screen.blit(obs, (0,0))
        else:
            font = pygame.font.SysFont("Arial", 30, bold=True)
            txt = font.render("MÉMORISEZ !", True, (0, 0, 0))
            self.screen.blit(txt, (LARGEUR//2 - 80, 20))

        # Effet flash rouge
        if temps_actuel < self.fin_ecran_rouge:
            s = pygame.Surface((LARGEUR, HAUTEUR))
            s.fill((255,0,0))
            s.set_alpha(100)
            self.screen.blit(s, (0,0))
            
        self.dessiner_interface(temps_restant)
            
        return "JEU"