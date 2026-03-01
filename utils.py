# utils.py
import pygame
import random
import os
import settings

def load_image(path):
    # Добавляем базовый путь
    full_path = settings.BASE_PATH + path
    try:
        return pygame.image.load(full_path).convert_alpha()
    except:
        print(f"Ошибка загрузки: {full_path}")
        surf = pygame.Surface((50, 50))
        surf.fill((255,0,255))  # ярко-розовый для отладки
        return surf

def create_placeholder_images():
    """Создаёт заглушки прямо в папке resources с сохранением подпапок"""
    base = settings.BASE_PATH
    os.makedirs(base + 'image', exist_ok=True)
    os.makedirs(base + 'Hero/Emma/Right', exist_ok=True)
    os.makedirs(base + 'Hero/Emma/Left', exist_ok=True)
    os.makedirs(base + 'Enemy/Enemy_Left', exist_ok=True)
    os.makedirs(base + 'Weapon', exist_ok=True)

    # Фон
    bg = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    for y in range(settings.SCREEN_HEIGHT):
        color = (34 + y//10, 139 + y//20, 34)
        pygame.draw.line(bg, color, (0, y), (settings.SCREEN_WIDTH, y))
    for _ in range(15):
        x = random.randint(0, settings.SCREEN_WIDTH)
        y = random.randint(200, settings.SCREEN_HEIGHT-50)
        pygame.draw.rect(bg, settings.BROWN, (x, y, 15, 100))
        pygame.draw.circle(bg, settings.DARK_GREEN, (x+7, y), 40)
    pygame.image.save(bg, base + 'image/background_forest.jpg')

    # Игрок
    for i in range(1,4):
        img = pygame.Surface((40,60), pygame.SRCALPHA)
        pygame.draw.rect(img, (255,200,150), (10,10,20,25))
        pygame.draw.rect(img, (100,50,150), (5,35,30,25))
        pygame.draw.rect(img, (50,50,200), (5,60,10,20))
        pygame.draw.rect(img, (50,50,200), (25,60,10,20))
        pygame.image.save(img, base + f'Hero/Emma/Right/Emma_right{i}.png')
        img_flipped = pygame.transform.flip(img, True, False)
        pygame.image.save(img_flipped, base + f'Hero/Emma/Left/Emma_Left{i}.png')

    # Враг
    for i in range(1,4):
        img = pygame.Surface((40,50), pygame.SRCALPHA)
        pygame.draw.circle(img, (150,150,150), (20,15), 15)
        pygame.draw.rect(img, (100,100,100), (10,25,20,25))
        pygame.draw.circle(img, (255,0,0), (15,12), 3)
        pygame.draw.circle(img, (255,0,0), (25,12), 3)
        pygame.image.save(img, base + f'Enemy/Enemy_Left/Enemy_Left{i}.png')

    # Пуля
    bullet = pygame.Surface((15,8), pygame.SRCALPHA)
    pygame.draw.ellipse(bullet, settings.GOLD, (0,0,15,8))
    pygame.image.save(bullet, base + 'Weapon/Bullet_Right.png')
    print("Созданы заглушки изображений в папке resources")

def check_and_create_resources():
    # Проверяем наличие ключевых файлов в папке resources
    base = settings.BASE_PATH
    files_needed = [
        base + 'image/background_forest.jpg',
        base + 'Hero/Emma/Right/Emma_right1.png',
        base + 'Enemy/Enemy_Left/Enemy_Left1.png',
        base + 'Weapon/Bullet_Right.png'
    ]
    missing = [f for f in files_needed if not os.path.exists(f)]
    if missing:
        print(f"Отсутствуют файлы: {missing}. Создаю заглушки...")
        create_placeholder_images()

def draw_text(surface, text, font, color, x, y, align="center"):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if align == "center":
        rect.center = (x, y)
    elif align == "topleft":
        rect.topleft = (x, y)
    elif align == "topright":
        rect.topright = (x, y)
    surface.blit(text_surface, rect)

def reset_game(all_sprites, enemies, bullets, powerups, platforms, player_class):
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    powerups.empty()
    platforms.empty()
    player = player_class()
    all_sprites.add(player)
    return player