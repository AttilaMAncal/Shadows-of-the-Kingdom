import pygame, csv, sys
from camera import Camera
from level import World
from enemy import Enemy
from background import draw_background
from menus import pause_menu, game_over_menu, win_menu
from hud import HUD


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    #pozadie, ikony, načítanie písma
    background = pygame.image.load("./assets/Background/Background1.png").convert_alpha()
    heart_img = pygame.image.load("./assets/Icons/heart.png").convert_alpha()
    coin_img = pygame.image.load("./assets/Icons/coin/coin1.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (32, 32))
    coin_img = pygame.transform.scale(coin_img, (32, 32))
    font = pygame.font.Font(None, 36)

    hud = HUD(heart_img, coin_img, font)

    #vytvorenie kamery
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, vertical_shift=40)

    coin_sound = pygame.mixer.Sound("./sounds/coin_sound.flac")
    heal_sound = pygame.mixer.Sound("./sounds/heal.wav")

    #načítanie csv
    level = 1
    world_data = []
    with open(f"./Level1/level{level}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            world_data.append([int(tile) for tile in row])

    #vytváranie sveta
    world = World()
    world.process_data(world_data, SCREEN_HEIGHT+100)

    #skupina sprite
    all_sprites = pygame.sprite.Group()
    all_sprites.add(world.obstacle_group)
    all_sprites.add(world.coin_group, world.heart_group, world.enemy_group)
    if world.player:
        all_sprites.add(world.player)


    Enemy.coin_spawn_callback = lambda pos: Enemy.spawn_coin(pos, world.coin_group, all_sprites)

    death_time = None
    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.USEREVENT:
                action = event.dict.get("action")

                if action == "load_level":
                    new_level = event.dict.get("level", 1)
                    if new_level == 1:
                        background = pygame.image.load("./assets/Background/Background1.png").convert_alpha()
                    elif new_level == 2:
                        background = pygame.image.load("./assets/Background/Background2.png").convert_alpha()
                    elif new_level == 3:
                        background = pygame.image.load("./assets/Background/Background3.png").convert_alpha()
                    level_data = []
                    with open(f"./Level{new_level}/level{new_level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for row in reader:
                            level_data.append([int(tile) for tile in row])
                    world = World(level=new_level)
                    world.process_data(level_data, SCREEN_HEIGHT + 100)
                    all_sprites.empty()
                    all_sprites.add(world.obstacle_group)
                    all_sprites.add(world.coin_group, world.heart_group, world.enemy_group)
                    if world.player:
                        all_sprites.add(world.player)

                elif action == "win":
                    # Meghívjuk a win menüt
                    choice = win_menu(screen)
                    if choice == "restart":
                        return "restart"  # vagy írd be ide azt a logikát, amivel újraindítod a pályát
                    elif choice == "menu":
                        return "menu"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    choice = pause_menu(screen)
                    if choice == "restart":
                        return "restart"
                    elif choice == "menu":
                        return "menu"

        #vstupy a logika hráčov
        if world.player and world.player.health > 0:
            world.player.handle_keys(world.obstacle_group)
            for enemy in world.enemy_group:
                enemy.ai(world.player, world.obstacle_group)
            all_sprites.update(world.obstacle_group)
            coin_hits = pygame.sprite.spritecollide(world.player, world.coin_group, True)
            heart_hits = pygame.sprite.spritecollide(world.player, world.heart_group, True)
            if coin_hits:
                world.player.coin_count += len(coin_hits)
                coin_sound.play()
            if heart_hits and world.player.health <= 4:
                world.player.health += len(heart_hits)
                heal_sound.play()
            world.player.handle_attack(world.enemy_group)
            for enemy in world.enemy_group:
                enemy.handle_attack(pygame.sprite.Group(world.player))
            camera.update(world.player)
            if world.player.rect.top > camera.offset.y + SCREEN_HEIGHT:
                world.player.take_damage(world.player.health)
            if world.door:
                world.door.update(world.player, world.start_time)
            death_time = None
            if world.princess:
                world.princess.update(world.player, world.start_time)
        else:
            all_sprites.update(world.obstacle_group)
            if death_time is None:
                death_time = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - death_time >= 2000:
                    choice = game_over_menu(screen)
                    if choice == "restart":
                        return "restart"
                    elif choice == "exit":
                        pygame.quit()
                        sys.exit()

        #vykreslenie
        screen.fill((30, 30, 30))
        draw_background(screen, background, camera, parallax_factor=0.3)
        if world.door:
            screen.blit(world.door.image, camera.apply(world.door.rect))
        if world.princess:
            screen.blit(world.princess.image, camera.apply(world.princess.rect))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))
        for enemy in world.enemy_group:
            enemy.draw_health(screen, camera)
        elapsed_time = (pygame.time.get_ticks() - world.start_time) / 1000.0

        #HUD
        if world.player:
            hud.draw(screen, world.player.health, world.player.coin_count, elapsed_time)
        pygame.display.flip()
    pygame.quit()
