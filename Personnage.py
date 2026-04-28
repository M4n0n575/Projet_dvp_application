import pygame

class Personnage:
    def __init__(self, vie, vie_max, vitesse, x_depart, y_depart):
        self.vie = vie
        self.vie_max = vie_max
        self.vitesse = vitesse
        self.x = x_depart
        self.y = y_depart
        self.ko = False
        self.temps_ko = 0
        
        #INITIALISATION AUDIO
        pygame.mixer.init()
        try:
            self.son_ko = pygame.mixer.Sound("KO.mp3")
        except:
            self.son_ko = None

    def deplacement(self, dx, dy, labyrinthe):
        if self.ko:
            return False
        
        nouveau_x = self.x + dx
        nouveau_y = self.y + dy

        if 0 <= nouveau_x < len(labyrinthe[0]) and 0 <= nouveau_y < len(labyrinthe):
            if labyrinthe[nouveau_y][nouveau_x] != 1:
                self.x = nouveau_x
                self.y = nouveau_y
                return False
            else:
                self.vie -= 45
                if self.vie <= 0:
                    self.ko = True
                    self.son_ko.play()
                    self.temps_ko = pygame.time.get_ticks()
                return True # Signal de collision pour l'effet rouge
        return False

    def update_ko(self):
        if self.ko and pygame.time.get_ticks() - self.temps_ko >= 3000:
            self.ko = False
            self.vie = self.vie_max