import pygame

class Personnage:
    def __init__(self, vie, vie_max, vitesse):
        """Fonction d'initialisation des statistiques basiques du personnage : sa vie, sa vitesse et ses coordonnées 2D (x et y)."""
        self.vie = vie
        self.vie_max = vie
        self.vitesse = vitesse
        self.x = 0
        self.y = 0
        self.ko = False
        self.temps_ko = 0

    def deplacement(self, dx, dy, labyrinthe):
        """Fonction qui permet de faire déplacer le personnage en modifiant ses variables x et y."""
        if self.ko:   # Si le personnage est KO, il ne bouge pas
            return
        else:
            nouveau_x = self.x + dx
            nouveau_y = self.y + dy

            if labyrinthe[nouveau_y][nouveau_x] != 1:   # Si pas de mur, il se déplace
                self.x = nouveau_x
                self.y = nouveau_y
            else:
                self.vie -= 20   # Sinon il perd 20 PV
                # ajout tremblement cam
                if self.vie <= 0: # Si sa vie passe sous la barre des 0
                    self.ko = True
                    self.temps_ko = pygame.time.get_ticks() #Initialisation de la variable temps_ko qui enregistre le moment de la collisions

    def update_ko(self):
        """Fonction qui enlève l'état KO après 3 secondes."""
        if self.ko and pygame.time.get_ticks() - self.temps_ko >= 3000:
            self.ko = False
            self.vie = self.vie_max