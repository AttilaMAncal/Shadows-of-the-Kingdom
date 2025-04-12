import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 60
        self.height = 70

        #animácie
        self.animations = {
            "idle": self.load_images("./player/Idle"),
            "walk": self.load_images("./player/Walk"),
            "jump": self.load_images("./player/Jump"),
            "attack": self.load_images("./player/Attack"),
            "death": self.load_images("./player/Death"),
            "hurt": self.load_images("./player/Hurt")
        }

        self.current_animation = "idle"
        self.current_frame = 0
        self.image = self.animations[self.current_animation][self.current_frame]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.frame_duration = 100  #ms
        self.last_update = pygame.time.get_ticks()

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.gravity = 1
        self.on_ground = False
        self.facing_right = True

        self.attack_executed = False

        self.sword_sound = pygame.mixer.Sound("./sounds/player_sword.wav")
        self.jump_sound = pygame.mixer.Sound("./sounds/player_jump.flac")
        self.hurt_sound = pygame.mixer.Sound("./sounds/player_hurt.wav")
        self.death_sound = pygame.mixer.Sound("./sounds/player_death.wav")

        self.health = 5
        self.coin_count = 0
        self.damage_cooldown = 500  # ms
        self.last_damage_time = 0
        self.dead = False

    def load_images(self, folder):
        images = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                path = os.path.join(folder, filename)
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                images.append(img)
        return images

    def update(self, obstacles=None):
        if obstacles is None:
            obstacles = []
        if self.dead:
            self.play_death_animation()
            return

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

        self.rect.x += self.vel_x

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel_x > 0:
                    self.rect.right = obstacle.rect.left
                elif self.vel_x < 0:
                    self.rect.left = obstacle.rect.right

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame += 1

            if self.current_animation == "attack":
                if self.current_frame >= len(self.animations["attack"]):
                    self.current_animation = "idle"
                    self.current_frame = 0

            elif self.current_animation == "hurt":
                if self.current_frame >= len(self.animations["hurt"]):
                    self.current_animation = "idle"
                    self.current_frame = 0

            elif self.current_animation == "death":
                if self.current_frame >= len(self.animations["death"]):
                    self.current_frame = len(self.animations["death"]) - 1

            else:
                self.current_frame %= len(self.animations[self.current_animation])

            base_image = self.animations[self.current_animation][self.current_frame]
            if not self.facing_right:
                base_image = pygame.transform.flip(base_image, True, False)
            self.image = base_image

            if self.current_animation != "attack":
                self.attack_executed = False

    def handle_keys(self, obstacles):
        if self.dead or self.current_animation == "death":
            return

        keys = pygame.key.get_pressed()

        if self.current_animation in ["attack", "hurt"]:
            return

        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.facing_right = False
            if self.on_ground and self.current_animation != "walk":
                self.current_animation = "walk"
                self.current_frame = 0
        elif keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.facing_right = True
            if self.on_ground and self.current_animation != "walk":
                self.current_animation = "walk"
                self.current_frame = 0
        else:
            self.vel_x = 0
            if self.on_ground and self.current_animation != "idle":
                self.current_animation = "idle"
                self.current_frame = 0

        #jump
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = -20
            self.current_animation = "jump"
            self.current_frame = 0
            self.jump_sound.play()

        #attack
        if keys[pygame.K_SPACE]:
            self.current_animation = "attack"
            self.sword_sound.play()
            self.current_frame = 0
            self.vel_x = 0
            self.attack_executed = False

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel_y > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.vel_y = 0
                    self.on_ground = True

    def take_damage(self, amount=1, attacker=None):
        now = pygame.time.get_ticks()
        if now - self.last_damage_time >= self.damage_cooldown and not self.dead:
            self.health -= amount
            self.last_damage_time = now
            if self.health > 0:
                self.current_animation = "hurt"
                self.current_frame = 0
                self.hurt_sound.play()
                if attacker:
                    if attacker.rect.centerx < self.rect.centerx:
                        self.rect.x += 10
                    else:
                        self.rect.x -= 10
            else:
                self.die()
                self.death_sound.play()

    def die(self):
        self.dead = True
        self.current_animation = "death"
        self.current_frame = 0
        self.vel_x = 0
        self.vel_y = 0


    def play_death_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.animations["death"]):
                self.current_frame = len(self.animations["death"]) - 1
            base_image = self.animations["death"][self.current_frame]
            if not self.facing_right:
                base_image = pygame.transform.flip(base_image, True, False)
            self.image = base_image

    def handle_attack(self, enemies):
        if self.current_animation == "attack" and not self.attack_executed:
            hits = pygame.sprite.spritecollide(self, enemies, False)
            for enemy in hits:
                enemy.take_damage(1, attacker=self)
            self.attack_executed = True