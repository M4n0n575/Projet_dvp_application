import pygame
import sys

# La classe Menu qui gère l'affichage et les clics
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        # --- POLICES ---
        self.font_title = pygame.font.SysFont("Arial", 70, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 22)
        
        # --- COULEURS DEMANDÉES ---
        self.bg_color = (48, 48, 48)       # Fond Gris
        self.btn_normal = (0, 0, 0)         # Bouton Noir
        self.btn_hover = (198, 8, 0)        # Rouge (Titre, Niveau, Survol)
        self.text_white = (255, 255, 255)   # Texte boutons
        
        # --- CONFIGURATION DES BOUTONS ---
        # Bouton JOUER
        self.play_rect = pygame.Rect(0, 0, 300, 70)
        self.play_rect.center = (screen.get_width() // 2, 250)
        
        # Bouton QUITTER
        self.quit_rect = pygame.Rect(0, 0, 300, 70)
        self.quit_rect.center = (screen.get_width() // 2, 340)
        
        # Zone de sélection de NIVEAU
        self.levels = ["FACILE", "MOYEN", "DIFFICILE"]
        self.level_idx = 0
        self.level_rect = pygame.Rect(0, 0, 220, 50)
        self.level_rect.center = (screen.get_width() // 2, 480)
        
        # États de couleur pour le survol
        self.current_play_col = self.btn_normal
        self.current_quit_col = self.btn_normal
        
    def handle_event(self, event):
        """Gère les interactions souris"""
        if event.type == pygame.MOUSEMOTION:
            # Survol JOUER
            if self.play_rect.collidepoint(event.pos):
                self.current_play_col = self.btn_hover
            else:
                self.current_play_col = self.btn_normal
                
            # Survol QUITTER
            if self.quit_rect.collidepoint(event.pos):
                self.current_quit_col = self.btn_hover
            else:
                self.current_quit_col = self.btn_normal

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Clic JOUER
            if self.play_rect.collidepoint(event.pos):
                return "JEU", self.levels[self.level_idx]
            
            # Clic QUITTER
            if self.quit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            
            # Clic NIVEAU
            if self.level_rect.collidepoint(event.pos):
                self.level_idx = (self.level_idx + 1) % len(self.levels)
                
        return "MENU", None

    def draw(self):
        """Affiche les éléments"""
        self.screen.fill(self.bg_color)
        
        # 1. Titre en ROUGE
        title_surf = self.font_title.render("BLIND MAZE", True, self.btn_hover)
        self.screen.blit(title_surf, (self.screen.get_width()//2 - title_surf.get_width()//2, 80))
        
        # 2. Bouton JOUER
        pygame.draw.rect(self.screen, self.current_play_col, self.play_rect, border_radius=10)
        txt_play = self.font_btn.render("JOUER", True, self.text_white)
        self.screen.blit(txt_play, txt_play.get_rect(center=self.play_rect.center))
        
        # 3. Bouton QUITTER
        pygame.draw.rect(self.screen, self.current_quit_col, self.quit_rect, border_radius=10)
        txt_quit = self.font_btn.render("QUITTER", True, self.text_white)
        self.screen.blit(txt_quit, txt_quit.get_rect(center=self.quit_rect.center))
        
        # 4. Sélecteur de NIVEAU
        lbl_lv = self.font_small.render("Difficulté (cliquez pour changer) :", True, (180, 180, 180))
        self.screen.blit(lbl_lv, (self.level_rect.centerx - lbl_lv.get_width()//2, 425))
        
        pygame.draw.rect(self.screen, self.btn_normal, self.level_rect, border_radius=5)
        # Niveau en ROUGE
        txt_lv = self.font_btn.render(self.levels[self.level_idx], True, self.btn_hover)
        self.screen.blit(txt_lv, txt_lv.get_rect(center=self.level_rect.center))

# ==========================================
# BLOC DE TEST (Lancé avec python menu.py)
# ==========================================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Menu - Blind Path")
    clock = pygame.time.Clock()
    
    mon_menu = Menu(screen)
    
    testant = True
    while testant:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                testant = False
            
            # On récupère les infos du menu
            resultat, niveau = mon_menu.handle_event(event)
            
            if resultat == "JEU":
                print(f"Bouton JOUER cliqué ! Niveau choisi : {niveau}")
                # Dans un vrai jeu, ici on lancerait la classe Game
        
        mon_menu.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()