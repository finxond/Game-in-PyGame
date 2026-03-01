# main.py
import pygame
import random
import os
import settings
from utils import load_image, check_and_create_resources, draw_text, reset_game
from menu import GameMenu
from classes.player import Player
from classes.enemy import Enemy
from classes.powerup import PowerUp
from classes.platform import Platform

# Инициализация
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption(settings.TITLE)
clock = pygame.time.Clock()

# Создаём папку resources и подпапки (если их нет)
os.makedirs(settings.BASE_PATH + 'image', exist_ok=True)
os.makedirs(settings.BASE_PATH + 'Hero/Emma/Right', exist_ok=True)
os.makedirs(settings.BASE_PATH + 'Hero/Emma/Left', exist_ok=True)
os.makedirs(settings.BASE_PATH + 'Enemy/Enemy_Left', exist_ok=True)
os.makedirs(settings.BASE_PATH + 'Weapon', exist_ok=True)
os.makedirs(settings.BASE_PATH + 'Songs', exist_ok=True)
os.makedirs(settings.BASE_PATH + 'Fonts', exist_ok=True)

# Проверяем и создаём заглушки
check_and_create_resources()

# Шрифты (теперь с путём resources)
try:
    font_large = pygame.font.Font(settings.BASE_PATH + 'Fonts/Blackadder.ttf', 60)
    font_medium = pygame.font.Font(settings.BASE_PATH + 'Fonts/Blackadder.ttf', 40)
    font_small = pygame.font.Font(settings.BASE_PATH + 'Fonts/Blackadder.ttf', 24)
except:
    font_large = pygame.font.SysFont('arial', 60, bold=True)
    font_medium = pygame.font.SysFont('arial', 40, bold=True)
    font_small = pygame.font.SysFont('arial', 24)

# Загрузка изображений (пути уже используют BASE_PATH внутри load_image)
bg_image = load_image('image/background_forest.jpg')
walk_right = [load_image(f'Hero/Emma/Right/Emma_right{i}.png') for i in range(1,4)]
walk_left = [load_image(f'Hero/Emma/Left/Emma_Left{i}.png') for i in range(1,4)]
enemy_frames = [load_image(f'Enemy/Enemy_Left/Enemy_Left{i}.png') for i in range(1,4)]
bullet_img = load_image('Weapon/Bullet_Right.png')

# Звуки (с путём resources)
def load_sound(name):
    try:
        return pygame.mixer.Sound(settings.BASE_PATH + 'Songs/' + name)
    except:
        return None

shoot_sound = load_sound('shoot.wav')
jump_sound = load_sound('jump.wav')
hit_sound = load_sound('hit.wav')
try:
    pygame.mixer.music.load(settings.BASE_PATH + 'Songs/night.mp3')
    pygame.mixer.music.play(-1)
except:
    print("Музыка не загружена")

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Игрок (пока None)
player = None

# Меню
menu = GameMenu(font_large, font_medium, font_small, bg_image)

# Таймеры
enemy_spawn_timer = pygame.USEREVENT + 1
powerup_spawn_timer = pygame.USEREVENT + 2
platform_spawn_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy_spawn_timer, settings.difficulty_settings["normal"]["enemy_spawn_delay"])
pygame.time.set_timer(powerup_spawn_timer, 5000)
pygame.time.set_timer(platform_spawn_timer, 8000)

game_state = settings.MENU
bg_x = 0
running = True

def create_player():
    from classes.player import Player
    return Player(walk_right, walk_left, all_sprites, bullets, platforms,
                  jump_sound, shoot_sound, hit_sound, bullet_img)

while running:
    clock.tick(settings.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == settings.MENU:
            result = menu.handle_input(event)
            if result is not None:
                if result == 0:  # START
                    game_state = settings.PLAYING
                    player = reset_game(all_sprites, enemies, bullets, powerups, platforms, create_player)
                    pygame.time.set_timer(enemy_spawn_timer, settings.difficulty_settings[settings.difficulty]["enemy_spawn_delay"])
                elif result == 1:  # DIFFICULTY
                    menu.show_difficulty = True
                elif result == 2:  # CONTROLS
                    menu.show_controls = True
                elif result == 3:  # EXIT
                    running = False

        elif game_state == settings.PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = settings.MENU
                elif event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_z:
                    player.shoot()

            if event.type == enemy_spawn_timer:
                if len(enemies) < settings.difficulty_settings[settings.difficulty]["max_enemies"]:
                    from classes.enemy import Enemy
                    enemy = Enemy(enemy_frames)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            if event.type == powerup_spawn_timer:
                if random.random() < 0.8:
                    powerup = PowerUp()
                    all_sprites.add(powerup)
                    powerups.add(powerup)
            if event.type == platform_spawn_timer:
                if random.random() < 0.6:
                    width = random.randint(80, 150)
                    x = settings.SCREEN_WIDTH
                    y = random.randint(200, settings.SCREEN_HEIGHT - 150)
                    platform = Platform(x, y, width)
                    all_sprites.add(platform)
                    platforms.add(platform)

        elif game_state in [settings.GAME_OVER, settings.VICTORY]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = settings.PLAYING
                    player = reset_game(all_sprites, enemies, bullets, powerups, platforms, create_player)
                    pygame.time.set_timer(enemy_spawn_timer, settings.difficulty_settings[settings.difficulty]["enemy_spawn_delay"])
                elif event.key == pygame.K_ESCAPE:
                    game_state = settings.MENU

    # ОБНОВЛЕНИЕ
    if game_state == settings.PLAYING and player is not None:
        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            player.add_score(50)

        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for p in powerup_hits:
            if p.type == 'health' and player.health < 5:
                player.health = min(player.health + 1, 5)
            elif p.type == 'ammo':
                player.ammo += 3

        enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
        if enemy_hits:
            for e in enemy_hits:
                e.kill()
            player.take_damage()

        if player.health <= 0:
            game_state = settings.GAME_OVER
        elif player.score >= settings.WINNING_SCORE:
            game_state = settings.VICTORY

    # ОТРИСОВКА
    screen.fill(settings.BLACK)

    if game_state == settings.MENU:
        menu.draw(screen)

    elif game_state == settings.PLAYING:
        screen.blit(bg_image, (bg_x, 0))
        screen.blit(bg_image, (bg_x + settings.SCREEN_WIDTH, 0))
        bg_x -= settings.SCROLL_SPEED
        if bg_x <= -settings.SCREEN_WIDTH:
            bg_x = 0

        all_sprites.draw(screen)

        if player and player.invulnerable:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                s = pygame.Surface((player.rect.width, player.rect.height), pygame.SRCALPHA)
                s.fill((255,255,255,128))
                screen.blit(s, player.rect.topleft)

        if player:
            pygame.draw.rect(screen, settings.RED, (10,10,150,20))
            health_width = 150 * (player.health / 5)
            pygame.draw.rect(screen, settings.GREEN, (10,10,health_width,20))
            pygame.draw.rect(screen, settings.WHITE, (10,10,150,20), 2)
            draw_text(screen, f"{player.health}/5", font_small, settings.WHITE, 85, 20)

            draw_text(screen, f"Score: {player.score}/{settings.WINNING_SCORE}",
                      font_medium, settings.GOLD, settings.SCREEN_WIDTH-10, 20, align="topright")
            draw_text(screen, f"Ammo: {player.ammo}", font_medium, settings.BLUE, 10, 40, align="topleft")
            draw_text(screen, f"Difficulty: {settings.difficulty.upper()}",
                      font_small, settings.GRAY, settings.SCREEN_WIDTH-10, 60, align="topright")

    elif game_state == settings.GAME_OVER:
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.fill((20,0,0))
        screen.blit(overlay, (0,0))
        draw_text(screen, "GAME OVER", font_large, settings.RED, settings.SCREEN_WIDTH//2, 180)
        score = player.score if player else 0
        draw_text(screen, f"Final Score: {score}", font_medium, settings.WHITE, settings.SCREEN_WIDTH//2, 260)
        draw_text(screen, "Press R to Restart or ESC for Menu",
                  font_small, settings.GRAY, settings.SCREEN_WIDTH//2, 350)

    elif game_state == settings.VICTORY:
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.fill((0,20,0))
        screen.blit(overlay, (0,0))
        draw_text(screen, "VICTORY!", font_large, settings.GOLD, settings.SCREEN_WIDTH//2, 150)
        draw_text(screen, "Emma escaped the forest!", font_medium, settings.WHITE, settings.SCREEN_WIDTH//2, 230)
        score = player.score if player else settings.WINNING_SCORE
        draw_text(screen, f"Final Score: {score}", font_medium, settings.GREEN, settings.SCREEN_WIDTH//2, 290)
        draw_text(screen, "Press R to Play Again or ESC for Menu",
                  font_small, settings.GRAY, settings.SCREEN_WIDTH//2, 380)

    pygame.display.flip()

pygame.quit()