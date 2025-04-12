import pygame

class Camera:
    def __init__(self, screen_width, screen_height, vertical_shift):
        self.offset = pygame.Vector2(0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertical_shift = vertical_shift

    def update(self, target):
        margin_left = 150
        margin_right = self.screen_width - 150

        #súradnica obrazovky hráča
        player_screen_x = target.rect.centerx - self.offset.x

        if player_screen_x < margin_left:
            self.offset.x = target.rect.centerx - margin_left
        elif player_screen_x > margin_right:
            self.offset.x = target.rect.centerx - margin_right

        if self.offset.x < 0:
            self.offset.x = 0

        if target.rect.left < 0:
            target.rect.left = 0

        #vertikálny posun: fix hodnota, takže stopa sa vždy zobrazí nižšie
        self.offset.y = self.vertical_shift

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)
