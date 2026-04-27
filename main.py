import pygame
import sys
from Menu import Menu
from Matrice import Jeu

def main():
    pygame.init()
    
    # Configuration de la fenêtre (doit correspondre à la taille de la grille)
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Blind Path - Le Labyrinthe")
    clock = pygame.time.Clock()
    
    menu = Menu(screen)
    jeu = None
    etat = "MENU" # États possibles : MENU, JEU
    
    while True:
        if etat == "MENU":
            # --- LOGIQUE DU MENU ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                resultat, difficulte = menu.handle_event(event)
                if resultat == "JEU":
                    # On initialise une nouvelle instance de jeu avec la difficulté
                    jeu = Jeu(screen, difficulte)
                    etat = "JEU"
            
            menu.draw()
            
        elif etat == "JEU":
            # --- LOGIQUE DU JEU ---
            res_jeu = jeu.update()
            
            if res_jeu == "MENU":
                etat = "MENU"
            elif res_jeu == "QUITTER":
                pygame.quit()
                sys.exit()
                
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()