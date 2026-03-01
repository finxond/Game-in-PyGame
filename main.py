import pygame
import random
import os

# ===== КОНФИГУРАЦИЯ =====
SCREEN_WIDTH, SCREEN_HEIGHT = 910, 512
TITLE = "Emma in danger: Escape from the Forest"
FPS = 60

# Цвета (все в одном месте)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
GOLD = (255, 215, 0)
DARK_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BLUE = (50, 100, 255)
GRAY = (128, 128, 128)

# Цвета для бонусов (чтобы не путать с основными)
HEALTH_COLOR = (255, 50, 50)    # ярко-красный
AMMO_COLOR = (50, 100, 255)     # синий

# Игровые константы
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_FORCE = -16
SCROLL_SPEED = 3
BULLET_SPEED = 12
ENEMY_SPEED_MIN = 2
ENEMY_SPEED_MAX = 5
WINNING_SCORE = 500

# Состояния игры
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"

# ===== ИНИЦИАЛИЗАЦИЯ =====
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Создаем папки если нет
os.makedirs('image', exist_ok=True)
os.makedirs('Hero/Emma/Right', exist_ok=True)
os.makedirs('Hero/Emma/Left', exist_ok=True)
os.makedirs('Enemy/Enemy_Left', exist_ok=True)
os.makedirs('Weapon', exist_ok=True)
os.makedirs('Songs', exist_ok=True)
os.makedirs('Fonts', exist_ok=True)

# Шрифты
try:
    font_large = pygame.font.Font('Fonts/Blackadder.ttf', 60)
    font_medium = pygame.font.Font('Fonts/Blackadder.ttf', 40)
    font_small = pygame.font.Font('Fonts/Blackadder.ttf', 24)
except:
    font_large = pygame.font.SysFont('arial', 60, bold=True)
    font_medium = pygame.font.SysFont('arial', 40, bold=True)
    font_small = pygame.font.SysFont('arial', 24)

# ===== ГЕНЕРАЦИЯ ЗАГЛУШЕК ДЛЯ РЕСУРСОВ =====
def create_placeholder_images():
    """Создает цветные заглушки если изображения не найдены"""
    # Фон
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT):
        color = (34 + y // 10, 139 + y // 20, 34)  # Градиент леса
        pygame.draw.line(bg, color, (0, y), (SCREEN_WIDTH, y))
    # Деревья
    for _ in range(15):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(200, SCREEN_HEIGHT - 50)
        pygame.draw.rect(bg, BROWN, (x, y, 15, 100))
        pygame.draw.circle(bg, DARK_GREEN, (x + 7, y), 40)
    pygame.image.save(bg, 'image/background_forest.jpg')
    
    # Игрок (Эмма)
    for i in range(1, 4):
        # Вправо
        img = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.rect(img, (255, 200, 150), (10, 10, 20, 25))  # Лицо
        pygame.draw.rect(img, (100, 50, 150), (5, 35, 30, 25))    # Тело
        pygame.draw.rect(img, (50, 50, 200), (5, 60, 10, 20))     # Нога
        pygame.draw.rect(img, (50, 50, 200), (25, 60, 10, 20))    # Нога
        pygame.image.save(img, f'Hero/Emma/Right/Emma_right{i}.png')
        
        # Влево (зеркально)
        img_flipped = pygame.transform.flip(img, True, False)
        pygame.image.save(img_flipped, f'Hero/Emma/Left/Emma_Left{i}.png')
    
    # Враг (Призрак)
    for i in range(1, 4):
        img = pygame.Surface((40, 50), pygame.SRCALPHA)
        pygame.draw.circle(img, (150, 150, 150), (20, 15), 15)  # Голова
        pygame.draw.rect(img, (100, 100, 100), (10, 25, 20, 25))  # Тело
        pygame.draw.circle(img, (255, 0, 0), (15, 12), 3)  # Красный глаз
        pygame.draw.circle(img, (255, 0, 0), (25, 12), 3)  # Красный глаз
        pygame.image.save(img, f'Enemy/Enemy_Left/Enemy_Left{i}.png')
    
    # Пуля
    bullet = pygame.Surface((15, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(bullet, GOLD, (0, 0, 15, 8))
    pygame.image.save(bullet, 'Weapon/Bullet_Right.png')
    
    print("Созданы заглушки изображений")

def check_and_create_resources():
    files_needed = [
        'image/background_forest.jpg',
        'Hero/Emma/Right/Emma_right1.png',
        'Enemy/Enemy_Left/Enemy_Left1.png',
        'Weapon/Bullet_Right.png'
    ]
    missing = [f for f in files_needed if not os.path.exists(f)]
    if missing:
        print(f"Создание ресурсов: {len(missing)} файлов отсутствует...")
        create_placeholder_images()

check_and_create_resources()

# ===== ЗАГРУЗКА РЕСУРСОВ =====
def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        print(f"Ошибка загрузки: {path}")
        return pygame.Surface((50, 50))

bg_image = load_image('image/background_forest.jpg')
walk_right = [load_image(f'Hero/Emma/Right/Emma_right{i}.png') for i in range(1, 4)]
walk_left = [load_image(f'Hero/Emma/Left/Emma_Left{i}.png') for i in range(1, 4)]
enemy_frames = [load_image(f'Enemy/Enemy_Left/Enemy_Left{i}.png') for i in range(1, 4)]
bullet_img = load_image('Weapon/Bullet_Right.png')

# Звуки (заглушки)
try:
    shoot_sound = pygame.mixer.Sound('Songs/shoot.wav')
except:
    shoot_sound = None
try:
    jump_sound = pygame.mixer.Sound('Songs/jump.wav')
except:
    jump_sound = None
try:
    hit_sound = pygame.mixer.Sound('Songs/hit.wav')
except:
    hit_sound = None
try:
    pygame.mixer.music.load('Songs/night.mp3')
    pygame.mixer.music.play(-1)
except:
    print("Музыка не загружена (файл не найден)")

# ===== КЛАССЫ =====
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.right_frames = walk_right
        self.left_frames = walk_left
        self.image = self.right_frames[0]
        self.rect = self.image.get_rect()
        # Ставим игрока на землю сразу
        self.rect.bottom = SCREEN_HEIGHT - 60
        self.rect.centerx = 100
        
        self.velocity_y = 0
        self.on_ground = True
        self.facing_right = True
        self.animation_index = 0
        self.last_animation_time = 0
        self.animation_delay = 120
        
        self.health = 3
        self.ammo = 5
        self.score = 0
        self.invulnerable = False
        self.invulnerable_end_time = 0
        self.is_moving = False

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.animate()
        self.check_invulnerability()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False
            self.is_moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True
            self.is_moving = True
            
        # Границы экрана
        self.rect.clamp_ip(screen.get_rect())

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False
            if jump_sound:
                jump_sound.play()

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            direction = 1 if self.facing_right else -1
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
            all_sprites.add(bullet)
            bullets.add(bullet)
            if shoot_sound:
                shoot_sound.play()

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        ground_y = SCREEN_HEIGHT - 60
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True

    def animate(self):
        current_time = pygame.time.get_ticks()
        frames = self.right_frames if self.facing_right else self.left_frames
        
        if self.is_moving or not self.on_ground:
            if current_time - self.last_animation_time >= self.animation_delay:
                self.animation_index = (self.animation_index + 1) % len(frames)
                self.image = frames[self.animation_index]
                self.last_animation_time = current_time
        else:
            self.image = frames[0]
            self.animation_index = 0

    def take_damage(self):
        if not self.invulnerable:
            self.health -= 1
            self.invulnerable = True
            self.invulnerable_end_time = pygame.time.get_ticks() + 2000
            if hit_sound:
                hit_sound.play()
            return True
        return False

    def check_invulnerability(self):
        if self.invulnerable and pygame.time.get_ticks() >= self.invulnerable_end_time:
            self.invulnerable = False

    def add_score(self, points):
        self.score += points

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = enemy_frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
        self.rect.x = SCREEN_WIDTH + random.randint(20, 100)
        ground_y = SCREEN_HEIGHT - 60
        self.rect.bottom = ground_y - random.choice([0, 30, 60])
        
        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        self.animation_index = 0
        self.last_animation_time = 0
        self.animation_delay = 200

    def update(self):
        self.rect.x -= self.speed
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time >= self.animation_delay:
            self.animation_index = (self.animation_index + 1) % len(self.frames)
            self.image = self.frames[self.animation_index]
            self.last_animation_time = current_time
        
        if self.rect.right < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['health', 'ammo'])
        
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        if self.type == 'health':
            color = HEALTH_COLOR
        else:
            color = AMMO_COLOR
        pygame.draw.circle(self.image, color, (12, 12), 12)
        pygame.draw.circle(self.image, WHITE, (12, 12), 8)
        
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(20, 100)
        self.rect.bottom = SCREEN_HEIGHT - 60
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# ===== ГРУППЫ СПРАЙТОВ =====
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# ===== КЛАСС МЕНЮ =====
class GameMenu:
    def __init__(self):
        self.options = ["START GAME", "CONTROLS", "EXIT"]
        self.selected = 0
        self.show_controls = False

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected
            elif event.key == pygame.K_ESCAPE:
                self.show_controls = False
        return None

    def draw(self, surface):
        surface.blit(bg_image, (0, 0))
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        title = font_large.render("EMMA IN DANGER", True, GOLD)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        subtitle = font_small.render("Escape from the Haunted Forest", True, WHITE)
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 140))
        
        if not self.show_controls:
            for i, option in enumerate(self.options):
                color = WHITE if i == self.selected else GRAY
                text = font_medium.render(option, True, color)
                surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))
                
                if i == self.selected:
                    pygame.draw.polygon(surface, WHITE, [
                        (SCREEN_WIDTH // 2 - 80, 270 + i * 60),
                        (SCREEN_WIDTH // 2 - 100, 275 + i * 60),
                        (SCREEN_WIDTH // 2 - 80, 280 + i * 60)
                    ])
            
            goal_text = font_small.render(f"Goal: Collect {WINNING_SCORE} points to win!", True, GREEN)
            surface.blit(goal_text, (SCREEN_WIDTH // 2 - goal_text.get_width() // 2, 450))
        else:
            self.draw_controls(surface)

    def draw_controls(self, surface):
        panel = pygame.Rect(SCREEN_WIDTH // 2 - 200, 150, 400, 300)
        pygame.draw.rect(surface, (30, 30, 30), panel)
        pygame.draw.rect(surface, GOLD, panel, 3)
        
        title = font_medium.render("CONTROLS", True, GOLD)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 170))
        
        controls = [
            ("← →", "Move"),
            ("SPACE", "Jump"),
            ("Z", "Shoot"),
            ("ESC", "Menu")
        ]
        
        for i, (key, action) in enumerate(controls):
            key_text = font_small.render(key, True, GREEN)
            action_text = font_small.render(action, True, WHITE)
            surface.blit(key_text, (SCREEN_WIDTH // 2 - 120, 220 + i * 40))
            surface.blit(action_text, (SCREEN_WIDTH // 2 + 20, 220 + i * 40))
        
        back_text = font_small.render("Press ESC to return", True, GRAY)
        surface.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 420))

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
def draw_text(surface, text, font, color, x, y, align="center"):
    """Универсальная функция для отрисовки текста с выравниванием."""
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if align == "center":
        rect.center = (x, y)
    elif align == "topleft":
        rect.topleft = (x, y)
    elif align == "topright":
        rect.topright = (x, y)
    elif align == "bottomleft":
        rect.bottomleft = (x, y)
    elif align == "bottomright":
        rect.bottomright = (x, y)
    surface.blit(text_surface, rect)

def reset_game():
    """Сброс игры для нового раунда"""
    global player, all_sprites, enemies, bullets, powerups
    
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    powerups.empty()
    
    player = Player()
    all_sprites.add(player)

# ===== ГЛАВНЫЙ ЦИКЛ =====
game_state = MENU
menu = GameMenu()

# Таймеры
enemy_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_spawn_timer, 2000)  # Новый враг каждые 2 секунды

powerup_spawn_timer = pygame.USEREVENT + 2
pygame.time.set_timer(powerup_spawn_timer, 8000)  # Бонус каждые 8 секунд

bg_x = 0
running = True

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # МЕНЮ
        if game_state == MENU:
            result = menu.handle_input(event)
            if result == 0:  # START
                game_state = PLAYING
                reset_game()
            elif result == 1:  # CONTROLS
                menu.show_controls = not menu.show_controls
            elif result == 2:  # EXIT
                running = False
        
        # ИГРА
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU
                elif event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_z:
                    player.shoot()
            
            if event.type == enemy_spawn_timer:
                if len(enemies) < 8:  # Максимум врагов
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            
            if event.type == powerup_spawn_timer:
                if random.random() < 0.5:  # 50% шанс
                    powerup = PowerUp()
                    all_sprites.add(powerup)
                    powerups.add(powerup)
        
        # КОНЕЦ ИГРЫ
        elif game_state in [GAME_OVER, VICTORY]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = PLAYING
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    game_state = MENU

    # ОБНОВЛЕНИЕ
    if game_state == PLAYING:
        all_sprites.update()
        
        # Пули попадают во врагов
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            player.add_score(50)
        
        # Игрок подбирает бонусы
        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in powerup_hits:
            if powerup.type == 'health' and player.health < 5:
                player.health = min(player.health + 1, 5)
            elif powerup.type == 'ammo':
                player.ammo += 3
        
        # Враги бьют игрока
        enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
        if enemy_hits:
            # Если урон нанесен, удаляем всех коснувшихся врагов
            if player.take_damage():
                for enemy in enemy_hits:
                    enemy.kill()
            else:
                # Если игрок неуязвим, враги всё равно исчезают? По желанию можно оставить
                # В текущей реализации оставим как есть: враги исчезают в любом случае
                for enemy in enemy_hits:
                    enemy.kill()
        
        # Проверка условий победы/поражения
        if player.health <= 0:
            game_state = GAME_OVER
        elif player.score >= WINNING_SCORE:
            game_state = VICTORY

    # ОТРИСОВКА
    screen.fill(BLACK)
    
    if game_state == MENU:
        menu.draw(screen)
    
    elif game_state == PLAYING:
        # Параллакс фон
        screen.blit(bg_image, (bg_x, 0))
        screen.blit(bg_image, (bg_x + SCREEN_WIDTH, 0))
        bg_x -= SCROLL_SPEED
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0
        
        all_sprites.draw(screen)
        
        # Эффект неуязвимости
        if player.invulnerable:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                s = pygame.Surface((player.rect.width, player.rect.height), pygame.SRCALPHA)
                s.fill((255, 255, 255, 128))
                screen.blit(s, player.rect.topleft)
        
        # Интерфейс
        pygame.draw.rect(screen, RED, (10, 10, 150, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, 150 * (player.health / 5), 20))
        pygame.draw.rect(screen, WHITE, (10, 10, 150, 20), 2)
        draw_text(screen, f"{player.health}/5", font_small, WHITE, 85, 20)
        
        draw_text(screen, f"Score: {player.score}/{WINNING_SCORE}", font_medium, GOLD, SCREEN_WIDTH - 10, 20, align="topright")
        draw_text(screen, f"Ammo: {player.ammo}", font_medium, BLUE, 10, 40, align="topleft")
    
    elif game_state == GAME_OVER:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((20, 0, 0))
        screen.blit(overlay, (0, 0))
        
        draw_text(screen, "GAME OVER", font_large, RED, SCREEN_WIDTH // 2, 180)
        draw_text(screen, f"Final Score: {player.score}", font_medium, WHITE, SCREEN_WIDTH // 2, 260)
        draw_text(screen, "Press R to Restart or ESC for Menu", font_small, GRAY, SCREEN_WIDTH // 2, 350)
    
    elif game_state == VICTORY:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 20, 0))
        screen.blit(overlay, (0, 0))
        
        draw_text(screen, "VICTORY!", font_large, GOLD, SCREEN_WIDTH // 2, 150)
        draw_text(screen, "Emma escaped the forest!", font_medium, WHITE, SCREEN_WIDTH // 2, 230)
        draw_text(screen, f"Final Score: {player.score}", font_medium, GREEN, SCREEN_WIDTH // 2, 290)
        draw_text(screen, "Press R to Play Again or ESC for Menu", font_small, GRAY, SCREEN_WIDTH // 2, 380)

    pygame.display.flip()

pygame.quit()