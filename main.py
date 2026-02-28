import pygame
import random

# ===== НАСТРОЙКИ =====
WIDTH, HEIGHT = 910, 512
FPS = 8

# Состояния игры
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

# ===== ИНИЦИАЛИЗАЦИЯ =====
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emma in danger")
clock = pygame.time.Clock()

# ===== ЗАГРУЗКА РЕСУРСОВ =====
# Иконка
icon = pygame.image.load('image/icon.png').convert_alpha()
pygame.display.set_icon(icon)

# Фон
bg = pygame.image.load('image/background_forest.jpg').convert_alpha()

# Игрок (анимация)
walk_right = [
    pygame.image.load('Hero/Emma/Right/Emma_right1.png').convert_alpha(),
    pygame.image.load('Hero/Emma/Right/Emma_right2.png').convert_alpha(),
    pygame.image.load('Hero/Emma/Right/Emma_right3.png').convert_alpha()
]
walk_left = [
    pygame.image.load('Hero/Emma/Left/Emma_Left1.png').convert_alpha(),
    pygame.image.load('Hero/Emma/Left/Emma_Left2.png').convert_alpha(),
    pygame.image.load('Hero/Emma/Left/Emma_Left3.png').convert_alpha()
]

# Враг (анимация)
enemy_frames = [
    pygame.image.load('Enemy/Enemy_Left/Enemy_Left1.png').convert_alpha(),
    pygame.image.load('Enemy/Enemy_Left/Enemy_Left2.png').convert_alpha(),
    pygame.image.load('Enemy/Enemy_Left/Enemy_Left3.png').convert_alpha()
]

# Пуля
bullet_img = pygame.image.load('Weapon/Bullet_Right.png').convert_alpha()

# Музыка
pygame.mixer.music.load('Songs/night.mp3')
pygame.mixer.music.play(-1)

# Шрифты
font_large = pygame.font.Font('Fonts/Blackadder.ttf', 60)
font_medium = pygame.font.Font('Fonts/Blackadder.ttf', 40)

# ===== КЛАСС МЕНЮ =====
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.selected = 0
        self.options = ["Start", "Control", "Exit"]
        
    def draw(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title = font_large.render("Emma in danger", True, (255, 215, 0))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        for i, opt in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (128, 128, 128)
            text = font_medium.render(opt, True, color)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 180 + i * 50))
    
    def handle_input(self, key):
        if key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)

# ===== СОЗДАЁМ МЕНЮ =====
menu = Menu(screen)

# ===== ИГРОВЫЕ ПЕРЕМЕННЫЕ =====
game_state = MENU

player_x = 100
player_y = 400
player_speed = 5
player_anim_count = 0
is_jump = False
jump_count = 10

bg_x = 0
scroll_speed = 5

enemy_anim_count = 0
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, random.randint(2500, 3500))
ghost_list = []

bullets = []
bullets_left = 5

# Здоровье и неуязвимость
player_health = 3
invulnerable = False
invulnerable_timer = 0

# Управление (подсказка)
controls = {
    "LEFT/RIGHT": "move",
    "SPACE": "jump",
    "Z": "shooting",
    "ESC": "menu"
}

# ===== СБРОС ИГРЫ =====
def reset_game():
    global player_x, player_y, ghost_list, bullets, bullets_left, bg_x, is_jump, jump_count, player_health, invulnerable
    player_x = 100
    player_y = 400
    ghost_list.clear()
    bullets.clear()
    bullets_left = 5
    bg_x = 0
    is_jump = False
    jump_count = 10
    player_health = 3
    invulnerable = False

# ===== ГЛАВНЫЙ ЦИКЛ =====
running = True
while running:
    # ===== ОБРАБОТКА СОБЫТИЙ =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        
        # ===== МЕНЮ =====
        if game_state == MENU:
            if event.type == pygame.KEYDOWN:
                menu.handle_input(event.key)
                if event.key == pygame.K_RETURN:
                    if menu.selected == 0:
                        game_state = PLAYING
                        reset_game()
                    elif menu.selected == 2:
                        running = False
        
        # ===== ИГРА =====
        elif game_state == PLAYING:
            if event.type == enemy_timer:
                y_pos = random.choice([350, 400, 450])
                ghost_list.append(enemy_frames[0].get_rect(topleft=(WIDTH, y_pos)))
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU
                if event.key == pygame.K_z and bullets_left > 0:
                    bullets.append(bullet_img.get_rect(topleft=(player_x + 30, player_y + 10)))
                    bullets_left -= 1
    
    # ===== ОТРИСОВКА =====
    if game_state == MENU:
        screen.blit(bg, (0, 0))
        menu.draw()
        
        # Рисуем управление
        y_offset = 400
        for key, desc in controls.items():
            text = font_medium.render(f"{key}: {desc}", True, (200, 200, 200))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))
            y_offset += 30
    
    elif game_state == PLAYING:
        # ===== ФОН =====
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + WIDTH, 0))
        bg_x -= scroll_speed
        if bg_x <= -WIDTH:
            bg_x = 0
        
        # ===== ВРАГИ =====
        for i, enemy_rect in enumerate(ghost_list[:]):  # копия списка
            screen.blit(enemy_frames[enemy_anim_count], (enemy_rect.x, enemy_rect.y))
            enemy_rect.x -= scroll_speed * 1.2
            
            if enemy_rect.x < -50:
                ghost_list.remove(enemy_rect)
        
        # Анимация врагов
        enemy_anim_count += 1
        if enemy_anim_count >= len(enemy_frames):
            enemy_anim_count = 0
        
        # ===== ИГРОК =====
        keys = pygame.key.get_pressed()
        
        # Движение
        if keys[pygame.K_LEFT] and player_x > 5:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed
        
        # Анимация и отрисовка игрока
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        
        player_anim_count += 1
        if player_anim_count >= len(walk_right):
            player_anim_count = 0
        
        # ===== ПРЫЖОК =====
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10
        
        # ===== ПУЛИ =====
        for i, bullet_rect in enumerate(bullets[:]):  # копия списка
            screen.blit(bullet_img, (bullet_rect.x, bullet_rect.y))
            bullet_rect.x += 15
            
            if bullet_rect.x > WIDTH:
                bullets.remove(bullet_rect)
            
            # Попадание во врага
            for j, enemy_rect in enumerate(ghost_list[:]):
                if bullet_rect.colliderect(enemy_rect):
                    if bullet_rect in bullets:
                        bullets.remove(bullet_rect)
                    if enemy_rect in ghost_list:
                        ghost_list.remove(enemy_rect)
                    break
        
        # ===== КОЛЛИЗИЯ С ВРАГАМИ =====
        player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))
        
        if not invulnerable:
            for enemy_rect in ghost_list[:]:
                if player_rect.colliderect(enemy_rect):
                    player_health -= 1
                    if enemy_rect in ghost_list:
                        ghost_list.remove(enemy_rect)
                    invulnerable = True
                    invulnerable_timer = 30  # ~4 секунды при 8 FPS
                    if player_health <= 0:
                        game_state = GAME_OVER
                    break
        
        if invulnerable:
            invulnerable_timer -= 1
            if invulnerable_timer <= 0:
                invulnerable = False
        
        # ===== ИНТЕРФЕЙС =====
        bullets_text = font_medium.render(f"Mana: {bullets_left}", True, (255, 255, 255))
        screen.blit(bullets_text, (10, 10))
        
        health_text = font_medium.render(f"Life {player_health}", True, (255, 50, 50))
        screen.blit(health_text, (10, 50))
    
    elif game_state == GAME_OVER:
        screen.fill((87, 88, 89))
        lose_text = font_large.render("Emma dead!", True, (193, 196, 199))
        restart_text = font_medium.render("R - restart, ESC - exit", True, (115, 132, 148))
        
        screen.blit(lose_text, (WIDTH//2 - lose_text.get_width()//2, 200))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 300))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_state = PLAYING
            reset_game()
        if keys[pygame.K_ESCAPE]:
            game_state = MENU
    
    pygame.display.update()
    clock.tick(FPS)