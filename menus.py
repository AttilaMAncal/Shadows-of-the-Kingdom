import pygame
import sys

def main_menu(screen):
    clock = pygame.time.Clock()
    black = (0, 0, 0)
    font_large = pygame.font.Font(None, 60)

    #hudba
    pygame.mixer.music.stop()
    pygame.mixer.music.load("./sounds/menu_music.ogg")
    pygame.mixer.music.play(-1)

    #pozadie, tlačidlo
    background_img = pygame.image.load("./assets/Menu/Background.png").convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))
    button_img = pygame.image.load("./assets/Menu/button.png").convert_alpha()
    title_img = pygame.image.load("./assets/Menu/title.png").convert_alpha()

    button_img = pygame.transform.scale(button_img, (300, 80))
    title_img = pygame.transform.scale(title_img, (720, 150))

    #texty
    start_text = font_large.render("Start Game", True, black)
    controls_text = font_large.render("Controls", True, black)
    exit_text = font_large.render("Quit Game", True, black)
    title_text = font_large.render("Shadows of the Kingdom", True, black)

    #nastavenie tlačidiel a texty
    title_rect = title_img.get_rect(center=(400, 100))
    start_button_rect = button_img.get_rect(center=(400, 250))
    controls_button_rect = button_img.get_rect(center=(400, 350))
    exit_button_rect = button_img.get_rect(center=(400, 450))

    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    controls_text_rect = controls_text.get_rect(center=controls_button_rect.center)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
    title_text_rect = title_text.get_rect(center=(title_rect.centerx, title_rect.centery - 20))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "start"
                elif controls_button_rect.collidepoint(event.pos):

                    from menus import controls_menu
                    controls_menu(screen)
                elif exit_button_rect.collidepoint(event.pos):
                    return "exit"

        screen.blit(background_img, (0, 0))
        screen.blit(title_img, title_rect)
        screen.blit(title_text, title_text_rect)

        screen.blit(button_img, start_button_rect)
        screen.blit(start_text, start_text_rect)
        screen.blit(button_img, controls_button_rect)
        screen.blit(controls_text, controls_text_rect)
        screen.blit(button_img, exit_button_rect)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()
        clock.tick(60)


def game_over_menu(screen):
    clock = pygame.time.Clock()
    black = (0, 0, 0)
    font_large = pygame.font.Font(None, 74)

    background_img = pygame.image.load("./assets/Background/game_over.png").convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))

    pygame.mixer.music.load("./sounds/game_over.ogg")
    pygame.mixer.music.play(-1)

    button_img = pygame.image.load("./assets/Menu/button.png").convert_alpha()
    button_img = pygame.transform.scale(button_img, (300, 80))

    restart_text = font_large.render("Restart", True, black)
    exit_text = font_large.render("Quit", True, black)

    restart_button_rect = button_img.get_rect(center=(400, 300))
    exit_button_rect = button_img.get_rect(center=(400, 400))

    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return "restart"
                elif exit_button_rect.collidepoint(event.pos):
                    return "exit"


        screen.blit(background_img, (0, 0))

        screen.blit(button_img, restart_button_rect)
        screen.blit(button_img, exit_button_rect)

        screen.blit(restart_text, restart_text_rect)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()
        clock.tick(60)



def pause_menu(screen):
    clock = pygame.time.Clock()

    paused_background = screen.copy()

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # fekete, 150-es alfa érték

    button_img = pygame.image.load("./assets/Menu/button.png").convert_alpha()
    button_img = pygame.transform.scale(button_img, (300, 80))

    font_large = pygame.font.Font(None, 60)
    black = (0, 0, 0)

    continue_text = font_large.render("Continue", True, black)
    restart_text = font_large.render("Restart", True, black)
    menu_text = font_large.render("Main Menu", True, black)

    continue_button_rect = button_img.get_rect(center=(400, 200))
    restart_button_rect = button_img.get_rect(center=(400, 300))
    menu_button_rect = button_img.get_rect(center=(400, 400))

    continue_text_rect = continue_text.get_rect(center=continue_button_rect.center)
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "continue"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(event.pos):
                    return "continue"
                elif restart_button_rect.collidepoint(event.pos):
                    return "restart"
                elif menu_button_rect.collidepoint(event.pos):
                    return "menu"

        screen.blit(paused_background, (0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(button_img, continue_button_rect)
        screen.blit(button_img, restart_button_rect)
        screen.blit(button_img, menu_button_rect)

        screen.blit(continue_text, continue_text_rect)
        screen.blit(restart_text, restart_text_rect)
        screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()
        clock.tick(60)


def controls_menu(screen):
    clock = pygame.time.Clock()
    black = (0, 0, 0)
    white = (255, 255, 255)

    background_img = pygame.image.load("./assets/Menu/Background.png").convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))

    button_img = pygame.image.load("./assets/Menu/button.png").convert_alpha()
    button_img = pygame.transform.scale(button_img, (300, 80))
    font_large = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    back_text = font_large.render("Back", True, black)
    back_button_rect = button_img.get_rect(center=(400, 500))
    back_text_rect = back_text.get_rect(center=back_button_rect.center)

    up_icon = pygame.image.load("./assets/Controls/up.png").convert_alpha()
    up_icon = pygame.transform.scale(up_icon, (32, 32))

    left_icon = pygame.image.load("./assets/Controls/left.png").convert_alpha()
    left_icon = pygame.transform.scale(left_icon, (32, 32))

    right_icon = pygame.image.load("./assets/Controls/right.png").convert_alpha()
    right_icon = pygame.transform.scale(right_icon, (32, 32))

    space_icon = pygame.image.load("./assets/Controls/space.png").convert_alpha()
    space_icon = pygame.transform.scale(space_icon, (64, 32))

    p_icon = pygame.image.load("./assets/Controls/p.png").convert_alpha()
    p_icon = pygame.transform.scale(p_icon, (32, 32))

    esc_icon = pygame.image.load("./assets/Controls/esc.png").convert_alpha()
    esc_icon = pygame.transform.scale(esc_icon, (64, 32))

    controls_info = [
        (up_icon,    "Jump"),
        (left_icon,  "Left"),
        (right_icon, "Right"),
        (space_icon, "Attack"),
        (p_icon,     "Pause"),
        (esc_icon,   "Quit Game")
    ]

    start_y = 120
    spacing = 60

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return

        screen.blit(background_img, (0, 0))

        for i, (icon, text) in enumerate(controls_info):
            icon_rect = icon.get_rect()
            icon_rect.midright = (350, start_y + i * spacing)
            screen.blit(icon, icon_rect)

            label = font_small.render(text, True, white)
            label_rect = label.get_rect(midleft=(icon_rect.right + 10, icon_rect.centery))
            screen.blit(label, label_rect)

        screen.blit(button_img, back_button_rect)
        screen.blit(back_text, back_text_rect)

        pygame.display.flip()
        clock.tick(60)

def win_menu(screen):
    import database

    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 74)
    info_font = pygame.font.Font(None, 36)

    pygame.mixer.music.load("./sounds/win_music.mp3")
    pygame.mixer.music.play(-1)  # végtelen ciklusban

    background_img = pygame.image.load("./assets/Background/win_background.png").convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))


    button_img = pygame.image.load("./assets/Menu/button.png").convert_alpha()
    button_img = pygame.transform.scale(button_img, (300, 80))

    win_text = font_large.render("You Win!", True, (255, 255, 0))
    win_text_rect = win_text.get_rect(center=(400, 100))


    restart_text = font_large.render("Restart", True, (0, 0, 0))
    menu_text = font_large.render("Main Menu", True, (0, 0, 0))


    restart_button_rect = button_img.get_rect(center=(400, 400))
    menu_button_rect = button_img.get_rect(center=(400, 500))

    last_three = database.get_last_three_saves()

    save_texts = []
    start_y = 180
    spacing = 50
    for i, record in enumerate(last_three):
        text_str = f"Level {record['level']} - {record['time']:.2f} sec, {record['coins']} coins, {record['health']} health"
        text_surface = info_font.render(text_str, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, start_y + i * spacing))
        save_texts.append((text_surface, text_rect))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return "restart"
                elif menu_button_rect.collidepoint(event.pos):
                    return "menu"

        screen.blit(background_img, (0, 0))
        screen.blit(win_text, win_text_rect)

        for text_surface, text_rect in save_texts:
            screen.blit(text_surface, text_rect)

        screen.blit(button_img, restart_button_rect)
        screen.blit(button_img, menu_button_rect)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(restart_text, restart_text_rect)
        screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()
        clock.tick(60)
