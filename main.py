import pygame

# Constants
SCREEN_WIDTH = 910
SCREEN_HEIGHT = 512
HERO_X = 250
HERO_Y = 400
ANIMATION_SPEED = 8
GRAVITY = 3
JUMP_HEIGHT = 20

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

class Game:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.hero_x = HERO_X
        self.hero_y = HERO_Y
        self.animation_speed = ANIMATION_SPEED

        self.screen = None
        self.clock = None
        self.bg_x = 0
        self.player = Player(HERO_X, HERO_Y, 5)

        self.load_resources()

    def load_resources(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Путешествие героя")

        icon = pygame.image.load('image/icon.png')
        pygame.display.set_icon(icon)

        self.bg = pygame.image.load('image/background_forest.jpg')

        self.player.images = {
            'left': [
                pygame.image.load('Hero/Emma/Left/Emma_Left1.png'),
                pygame.image.load('Hero/Emma/Left/Emma_Left2.png'),
                pygame.image.load('Hero/Emma/Left/Emma_left3.png'),
            ],
            'right': [
                pygame.image.load('Hero/Emma/Right/Emma_right1.png'),
                pygame.image.load('Hero/Emma/Right/Emma_right2.png'),
                pygame.image.load('Hero/Emma/Right/Emma_right3.png'),
            ]
        }

        try:
            pygame.mixer.init()
            pygame.mixer.music.load('Hero/Songs/night.mp3')
            pygame.mixer.music.play(-1)  # Play the music in a loop
        except pygame.error as e:
            print(f"Error initializing mixer module: {e}")

        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
        return True

    def update_game_state(self):
        self.bg_x -= 2
        if self.bg_x == -self.screen_width:
            self.bg_x = 0

    def render_screen(self):
        self.screen.blit(self.bg, (self.bg_x, 0))
        self.screen.blit(self.bg, (self.bg_x + self.screen_width, 0))
        self.screen.blit(self.player.images[self.player.direction][self.player.index % len(self.player.images[self.player.direction])], (self.player.x, self.player.y))
        pygame.display.update()

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-self.player.speed)
            self.player.direction = 'left'
            self.player.update_animation()
        elif keys[pygame.K_RIGHT]:
            self.player.move(self.player.speed)
            self.player.direction = 'right'
            self.player.update_animation()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update_game_state()
            self.move_player()
            self.player.update_jump()
            self.render_screen()
            self.clock.tick(self.animation_speed)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()