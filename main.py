import pygame
import sys
from Menu import Menu
from Matrice import Jeu

def main():
    # Initialisation de Pygame et du mixer audio
    pygame.init()
    pygame.mixer.init()
    
    # Configuration de la fenêtre (600x600 pour une grille 10x10 de cases de 60px)
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Blind Maze - Le Labyrinthe")
    clock = pygame.time.Clock()
    
    menu = Menu(screen)
    jeu = None
    etat = "MENU" # États possibles : MENU, JEU
    
    # Tentative de chargement de la musique du menu
    try:
        pygame.mixer.music.load("Ambiance.mp3")
        pygame.mixer.music.set_volume(0.5) # Volume à 50%
    except:
        print("Note : menu_ambient.mp3 non trouvé.")

    while True:
        if etat == "MENU":
            # Lancer la musique si elle n'est pas déjà en cours
            if not pygame.mixer.music.get_busy():
                try:
                    pygame.mixer.music.play(-1) # -1 pour boucler à l'infini
                except:
                    pass

            # --- LOGIQUE DU MENU ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                resultat, difficulte = menu.handle_event(event)
                
                if resultat == "JEU":
                    # On arrête la musique du menu avant de lancer le jeu
                    pygame.mixer.music.stop()
                    # On initialise une nouvelle instance de jeu
                    jeu = Jeu(screen, difficulte)
                    etat = "JEU"
            
            menu.draw()
            
        elif etat == "JEU":
            # --- LOGIQUE DU JEU ---
            res_jeu = jeu.update()
            
            if res_jeu == "MENU":
                # On s'assure que tous les bruitages de Matrice.py sont coupés
                pygame.mixer.stop()
                etat = "MENU"
                
            elif res_jeu == "QUITTER":
                pygame.quit()
                sys.exit()
                
        pygame.display.flip()
        clock.tick(60) # Limite à 60 FPS

if __name__ == "__main__":
    main()