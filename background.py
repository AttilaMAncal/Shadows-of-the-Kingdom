import pygame


def draw_background(screen, background, camera, parallax_factor=0.3):
    screen_w, screen_h = screen.get_size()
    bg_w, bg_h = background.get_size()

    #výška pozadia sa nastavím tak, aby vyplnila celú výšku obrazovky
    scale_factor = screen_h / bg_h
    scaled_w = int(bg_w * scale_factor)
    scaled_h = screen_h

    scaled_bg = pygame.transform.scale(background, (scaled_w, scaled_h))

    #horizontálny posun pozadia na základe pohybu kamery
    offset_x = -camera.offset.x * parallax_factor

    start_x = (offset_x // scaled_w) * scaled_w
    end_x = start_x + screen_w + scaled_w

    x = start_x
    while x < end_x:
        draw_x = x - offset_x
        screen.blit(scaled_bg, (draw_x, 0))
        x += scaled_w
