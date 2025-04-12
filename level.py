import pygame
from icons import Coin, Heart, Door, Princess
from player import Player
from enemy import Enemy

TILE_SIZE = 48
screen_scroll = 0

def load_tile_images(level):
    img_list = []
    for x in range(34):  #0-32 tile, 33 obrázkov
        img = pygame.image.load(f"./Level{level}/tile/{x}.png")
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
    return img_list

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

class World():
    def __init__(self, level=1):

        self.img_list = load_tile_images(level)
        self.obstacle_group = pygame.sprite.Group()  #skupina prekážok
        self.coin_group = pygame.sprite.Group()        #skupina mincí
        self.heart_group = pygame.sprite.Group()        #skupina srdca
        self.enemy_group = pygame.sprite.Group()
        self.door = None
        self.player = None
        self.princess = None
        self.level = level
        self.start_time = 0

    def process_data(self, data, screen_height):
        rows = len(data)
        level_height = rows * TILE_SIZE
        offset_y = screen_height - level_height

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                pos_x = x * TILE_SIZE
                pos_y = offset_y + y * TILE_SIZE
                if 0 <= tile <= 28:  #prekážky
                    img = self.img_list[tile]
                    obstacle = Obstacle(img, pos_x, pos_y)
                    self.obstacle_group.add(obstacle)

                elif tile == 29:  #mince
                    coin = Coin(pos_x, pos_y)
                    self.coin_group.add(coin)

                elif tile == 30:  #srdce
                    heart = Heart(pos_x, pos_y)
                    self.heart_group.add(heart)

                elif tile == 31:  #hráč
                    self.player = Player(pos_x, pos_y)

                elif tile == 32:  #protihráči
                    enemy = Enemy(pos_x, pos_y)
                    self.enemy_group.add(enemy)

                elif tile == 33:  #dvere
                    self.door = Door(pos_x, pos_y, current_level=self.level)

                elif tile == 34:
                    self.princess = Princess(pos_x, pos_y)
        self.start_time = pygame.time.get_ticks()
        return self
