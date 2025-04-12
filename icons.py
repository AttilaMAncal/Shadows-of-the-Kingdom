import pygame
import os

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.width = 32
        self.height = 32

        #animácia rotate
        self.animations = {
            "rotate": self.load_images("./assets/Icons/coin")
        }
        self.current_animation = "rotate"
        self.current_frame = 0
        self.image = self.animations[self.current_animation][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


        self.frame_duration = 100
        self.last_update = pygame.time.get_ticks()

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
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_frame]


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 32
        self.height = 32

        #animácia pulse
        self.animations = {
            "pulse": self.load_images("./assets/Icons/heart")
        }
        self.current_animation = "pulse"
        self.current_frame = 0
        self.image = self.animations[self.current_animation][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.frame_duration = 100
        self.last_update = pygame.time.get_ticks()

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
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_frame]

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, current_level):
        super().__init__()
        self.width = 64
        self.height = 100
        self.current_level = current_level

        self.closed_image = pygame.image.load(os.path.join("./assets/Icons/door/closed_door.png")).convert_alpha()
        self.opened_image = pygame.image.load(os.path.join("./assets/Icons/door/opened_door.png")).convert_alpha()

        self.closed_image = pygame.transform.scale(self.closed_image, (self.width, self.height))
        self.opened_image = pygame.transform.scale(self.opened_image, (self.width, self.height))

        self.image = self.closed_image
        self.rect = self.image.get_rect(midleft=(x, y))

        self.state = "closed"
        self.distance_threshold = 150

        self.level_loaded = False

    def update(self, player, start_time):
        distance = abs(self.rect.centerx - player.rect.centerx)

        if distance <= self.distance_threshold:
            if self.state != "open":
                self.state = "open"
                self.image = self.opened_image

            if self.rect.colliderect(player.rect) and not self.level_loaded:
                elapsed_time_ms = pygame.time.get_ticks() - start_time
                elapsed_time_sec = elapsed_time_ms / 1000.0


                import database
                player_data = {
                    "health": player.health,
                    "coins": player.coin_count,
                    "level": self.current_level,
                    "time": elapsed_time_sec
                }
                database.save_game_data(player_data)
                next_level = self.current_level + 1
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "load_level", "level": next_level}))
                self.level_loaded = True

        else:
            if self.state != "closed":
                self.state = "closed"
                self.image = self.closed_image


class Princess(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 38
        self.height = 70

        self.animations = {
            "idle": self.load_images("./princess")
        }
        self.current_animation = "idle"
        self.current_frame = 0
        self.image = self.animations[self.current_animation][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y + 48)

        self.frame_duration = 150
        self.last_update = pygame.time.get_ticks()
        self.win_triggered = False

    def load_images(self, folder):
        images = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                path = os.path.join(folder, filename)
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                images.append(img)
        return images

    def update(self, player, start_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_frame]

        if self.rect.colliderect(player.rect) and not self.win_triggered:
            elapsed_time_sec = (now - start_time) / 1000.0
            import database
            player_data = {
                "health": player.health,
                "coins": player.coin_count,
                "level": 3,
                "time": elapsed_time_sec
            }
            database.save_game_data(player_data)
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "win"}))
            self.win_triggered = True

