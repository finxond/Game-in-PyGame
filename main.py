import pygame
import random

# Constants
SCREEN_WIDTH = 910
SCREEN_HEIGHT = 512
HERO_X = 250
HERO_Y = 400
ANIMATION_SPEED = 8
GRAVITY = 1
JUMP_HEIGHT = 20
BULLET_SPEED = 10

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 'right'
        self.images = {}
        self.index = 0
        self.is_jumping = False
        self.jump_velocity = 0
        self.weapon = Weapon(self.x, self.y, self.direction)

    def move(self, dx):
        self.x += dx
        self.x = max(0, min(self.x, SCREEN_WIDTH - 50))

    def update_animation(self):
        self.index = (self.index + 1) % len(self.images[self.direction])

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = -JUMP_HEIGHT

    def update_jump(self):
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += GRAVITY
            if self.y >= HERO_Y:
                self.y = HERO_Y
                self.is_jumping = False
                self.jump_velocity = 0

    def attack(self):
        bullet = self.weapon.shoot(self.x, self.y, self.direction)
        return bullet

class Weapon:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.images = {
            'left': [
                pygame.image.load('Weapon/Gun/Left/Gun_Left1.png'),
                pygame.image.load('Weapon/Gun/Left/Gun_Left2.png'),
            ],
            'right': [
                pygame.image.load('Weapon/Gun/Right/Gun_Right1.png'),
                pygame.image.load('Weapon/Gun/Right/Gun_Right2.png'),
            ]
        }
        self.index = 0
        self.bullet_speed = BULLET_SPEED
        self.bullet = Bullet(self.x, self.y, self.direction, self.bullet_speed)

    def shoot(self, x, y, direction):
        self.bullet.x = x
        self.bullet.y = y
        self.bullet.direction = direction
        self.bullet.is_alive = True
        return self.bullet

    def update_animation(self):
        self.index = (self.index + 1) % len(self.images[self.direction])

class Bullet:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.images = {
            'left': pygame.image.load('Weapon/Bullet_Left.png'),
            'right': pygame.image.load('Weapon/Bullet_Right.png'),
        }
        self.image = self.images[direction]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_alive = False

    def update(self):
        if self.is_alive:
            if self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'right':
                self.x += self.speed

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.images = {
            'left': pygame.image.load('Enemy/Enemy_Left.png'),
            'right': pygame.image.load('Enemy/Enemy_Right.png'),
        }
        self.image = self.images['right']
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_alive = True

    #...

    def update(self):
        self.x += self.speed
        if self.x + self.width > SCREEN_WIDTH:
            self.x = random.randint(0, SCREEN_WIDTH - self.width)
            self.y = random.randint(0, SCREEN_HEIGHT - self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collide(self, player):
        if self.x < player.x + player.width and self.x + self.width > player.x and self.y < player.y + player.height and self.y + self.height > player.y:
            return True
        return False

    def shoot(self, player):
        # Implement enemy shooting logic here
        pass

class GameOver:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Game Over", True, (255, 0, 0))
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.button_width = 100
        self.button_height = 50
        self.close_button = pygame.Rect(SCREEN_WIDTH // 2 - self.button_width // 2, SCREEN_HEIGHT // 2 + 50, self.button_width, self.button_height)
        self.restart_button = pygame.Rect(SCREEN_WIDTH // 2 - self.button_width // 2, SCREEN_HEIGHT // 2 + 120, self.button_width, self.button_height)
        self.close_text = self.font.render("Close", True, (255, 255, 255))
        self.restart_text = self.font.render("Restart", True, (255, 255, 255))
        self.close_text_rect = self.close_text.get_rect(center=self.close_button.center)
        self.restart_text_rect = self.restart_text.get_rect(center=self.restart_button.center)
        self.running = True

    def draw(self):
        self.screen.blit(self.text, self.text_rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.close_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.restart_button)
        self.screen.blit(self.close_text, self.close_text_rect)
        self.screen.blit(self.restart_text, self.restart_text_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.close_button.collidepoint(event.pos):
                    self.running = False
                elif self.restart_button.collidepoint(event.pos):
                    # Restart the game
                    pass

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(HERO_X, HERO_Y, 5)
        self.enemy = Enemy(random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100), 1)
        self.game_over = None

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(-self.player.speed)
                    self.player.direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    self.player.move(self.player.speed)
                    self.player.direction = 'right'
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_z:
                    bullet = self.player.attack()
                    bullet.is_alive = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.move(0)

        return True

    def update_game_state(self):
        self.player.update_animation()
        self.player.weapon.update_animation()
        self.enemy.update()

    def move_player(self):
        self.player.weapon.bullet.update()

    def update_bullets(self):
        for bullet in self.player.weapon.bullet:
            if bullet.is_alive:
                if bullet.x < 0 or bullet.x > SCREEN_WIDTH:
                    bullet.is_alive = False
                elif bullet.collide(self.enemy):
                    self.enemy.is_alive = False
                    bullet.is_alive = False

    def render_screen(self):
        self.screen.fill((0, 0, 0))
        self.player.weapon.bullet.draw(self.screen)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        if self.game_over:
            self.game_over.draw()
        pygame.display.flip()

    def run(self):
        running = True
        game_over = None
        enemy = Enemy(random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100), 1)

        while running:
            events = pygame.event.get()
            if game_over:
                game_over.handle_events(events)
                if not game_over.running:
                    running = False
            else:
                running = self.handle_events()

            self.update_game_state()
            self.move_player()
            self.player.update_jump()
            self.update_bullets()
            enemy.update()

            if self.player.weapon.bullet.collide(enemy):
                enemy.is_alive = False

            if enemy.collide(self.player):
                if not self.player.weapon.bullet.is_alive:
                    game_over = GameOver(self.screen)

            self.render_screen()
            self.clock.tick(self.animation_speed)

            if not enemy.is_alive:
                enemy = Enemy(random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100), 1)

if __name__ == '__main__':
    game = Game()
    game.run()