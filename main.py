import pygame, sys
from menus import main_menu
from game_loop import game_loop

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Shadows of the Kingdom")

    while True:
        #Main menu hudba
        pygame.mixer.music.stop()
        pygame.time.delay(100)
        pygame.mixer.music.load("./sounds/menu_music.ogg")
        pygame.mixer.music.play(-1)

        choice = main_menu(screen)
        #ak klikneme na štart
        if choice == "start":
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./sounds/level_music.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

            result = game_loop()
            #ak kliknete na reštart, reštartujeme levelu
            while result == "restart":
                pygame.mixer.music.stop()
                pygame.mixer.music.load("./sounds/level_music.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                result = game_loop()

            if result == "menu" or result == "exit":
                continue
        elif choice == "exit":
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
