import pygame
import os
import math
from icons import Coin

class Enemy(pygame.sprite.Sprite):
    coin_spawn_callback = None

    def __init__(self, x, y):
        super().__init__()
        self.width = 96
        self.height = 70

        self.animations = {
            "idle": self.load_images("enemy/Idle"),
            "run": self.load_images("enemy/Run"),
            "attack": self.load_images("enemy/Attack")
        }

        self.current_animation = "idle"
        self.current_frame = 0
        self.image = self.animations[self.current_animation][self.current_frame]

        TILE_SIZE = 64
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x + TILE_SIZE // 2, y + TILE_SIZE)

        self.frame_duration = 100  # ms
        self.last_update = pygame.time.get_ticks()

        self.speed = 2
        self.facing_right = True


        self.attack_range = 50

        self.health = 3
        self.damage_cooldown = 500  # ms
        self.last_damage_time = 0
        self.dead = False

        self.attack_executed = False
        self.hurt = False
        self.hurt_time = 0
        self.hurt_cooldown = 1000  # ms

        self.death_sound = pygame.mixer.Sound("./sounds/enemy_death.wav")
        self.hurt_sound = pygame.mixer.Sound("./sounds/enemy_hurt.wav")
        self.sword_sound = pygame.mixer.Sound("./sounds/enemy_sword.ogg")

        self.vel_y = 0
        self.gravity = 1
        self.on_ground = False

        self.heart_image = pygame.image.load("./assets/Icons/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (16, 16))

    def load_images(self, folder):
        images = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                path = os.path.join(folder, filename)
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                images.append(img)
        return images

    def take_damage(self, amount=1, attacker=None):
        now = pygame.time.get_ticks()
        if now - self.last_damage_time >= self.damage_cooldown and not self.dead:
            self.health -= amount
            self.last_damage_time = now
            if self.health > 0:
                self.hurt = True
                self.hurt_time = now
                self.hurt_sound.play()
                if attacker:
                    if attacker.rect.centerx < self.rect.centerx:
                        self.rect.x += 40
                    else:
                        self.rect.x -= 40
            else:
                self.death_sound.play()
                self.dead = True
                if Enemy.coin_spawn_callback:
                    Enemy.coin_spawn_callback(self.rect.center)
                self.kill()

    def ai(self, player, obstacles):
        now = pygame.time.get_ticks()
        if self.dead:
            self.set_state("idle")
            return
        if self.hurt and now - self.hurt_time < self.hurt_cooldown:
            self.set_state("idle")
            return
        else:
            self.hurt = False

        px, py = player.rect.center
        ex, ey = self.rect.center
        distance = math.hypot(px - ex, py - ey)

        if distance > 500:
            self.set_state("idle")
            return

        if distance < self.attack_range:
            self.set_state("attack")
        else:
            self.set_state("run")
            self.facing_right = (px > ex)

    def set_state(self, state):
        if state in self.animations and state != self.current_animation:
            self.current_animation = state
            self.current_frame = 0
            base_image = self.animations[state][0]
            self.image = base_image
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
            if state == "attack":
                self.attack_executed = False

    def handle_attack(self, enemies):
        hit_frame = len(self.animations["attack"]) // 2
        if (self.current_animation == "attack"
            and self.current_frame == hit_frame
            and not self.attack_executed):
            hits = pygame.sprite.spritecollide(self, enemies, False)
            for target in hits:
                target.take_damage(1, attacker=self)
            self.attack_executed = True
            self.sword_sound.play()

    def draw_health(self, surface, camera):
        draw_rect = camera.apply(self.rect)
        heart_count = self.health
        heart_width = self.heart_image.get_width()
        heart_height = self.heart_image.get_height()
        spacing = 2
        total_width = heart_count * (heart_width + spacing) - spacing
        start_x = draw_rect.centerx - total_width // 2
        start_y = draw_rect.top - heart_height - 5
        for i in range(heart_count):
            x = start_x + i * (heart_width + spacing)
            y = start_y
            surface.blit(self.heart_image, (x, y))

    def update(self, obstacles=None):
        if obstacles is None:
            obstacles = []

        #horizontálny pohyb
        old_x = self.rect.x
        if self.current_animation == "run":
            if self.facing_right:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

        #nárazová skúška v smere X
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.rect.x = old_x
                break

        #gravitačná a nárazová skúška v smere Y
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_ground = False
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel_y > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.vel_y = 0

        #aktualizácia animácie
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.animations[self.current_animation]):
                self.current_frame = 0

            base_image = self.animations[self.current_animation][self.current_frame]
            if not self.facing_right:
                base_image = pygame.transform.flip(base_image, True, False)
            self.image = base_image


            if self.current_animation == "attack" and self.current_frame == 0:
                self.attack_executed = False

    @staticmethod
    def spawn_coin(pos, coin_group, all_sprites):
        coin = Coin(pos[0], pos[1])
        coin_group.add(coin)
        all_sprites.add(coin)

Enemy.coin_spawn_callback = Enemy.spawn_coin