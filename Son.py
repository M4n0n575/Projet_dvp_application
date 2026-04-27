import pygame

class Sons:
    def __init__(self):
        """Initialise l'utilisation des sons"""
        pygame.mixer.init()
        
        self.ambiance = "Sons/Ambiance.mp3" 
        
        try:
            self.son_degat = pygame.mixer.Sound("Degats.mp3")
            self.son_ko = pygame.mixer.Sound("KO.mp3")
            self.son_win = pygame.mixer.Sound("Win.mp3")
            self.son_lose = pygame.mixer.Sound("Lose.mp3")
            self.son_pas = pygame.mixer.Sound("Déplacements.mp3")
        except pygame.error:
            print("Erreur : Vérifiez que les fichiers sont dans le bon fichier")

    def jouer_ambiance(self):
        """Lance la musique de fond"""
        pygame.mixer.music.load(self.ambiance)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def jouer_pas(self):
        """Se dèclenche lorsque le personnage se déplace et si aucun autre son n'est joué"""
        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(self.son_pas)
            self.son_pas.set_volume(0.3)


    def jouer_degat(self):
        """Se déclenche lors d'une collision avec un mur"""
        self.son_degat.play()

    def jouer_ko(self):
        """Se déclenche quand le personnage tombe KO"""
        self.son_ko.play()

    def jouer_win(self):
        """Se déclenche quand l'utilisateur trouve la sortie et gagne"""
        self.son_win.play()

    def jouer_lose(self):
        """Se déclenche si le personnage ne trouve pas la sortie"""
        self.son_lose.play()