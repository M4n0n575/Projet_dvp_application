import pygame

class Personnage:
    def __init__(self, vie, vie_max, vitesse, x_depart, y_depart):
        """Fonction d'initialisation des statistiques basiques du personnage : sa vie, sa vitesse et ses coordonnées 2D (x et y)"""
        self.vie = vie
        self.vie_max = vie_max
        self.vitesse = vitesse
        self.x = x_depart
        self.y = y_depart
        self.ko = False
        self.temps_ko = 0

    def deplacement(self, dx, dy, labyrinthe):
        """Fonction qui permet de faire déplacer le personnage en modifiant ses variables x et y"""
        if self.ko:
            return False
        else :
        nouveau_x = self.x + dx
        nouveau_y = self.y + dy

        if 0 <= nouveau_x < len(labyrinthe[0]) and 0 <= nouveau_y < len(labyrinthe):
            if labyrinthe[nouveau_y][nouveau_x] != 1:
                self.x = nouveau_x
                self.y = nouveau_y
                return False
            
                self.vie -= 20
                if self.vie <= 0:
                    self.ko = True
                    self.temps_ko = pygame.time.get_ticks()
                return True
        return False

    def update_ko(self):
        """Fonction qui enlève l'état KO après 3 secondes."""
        if self.ko and pygame.time.get_ticks() - self.temps_ko >= 3000:
            self.ko = False
            self.vie = self.vie_max
