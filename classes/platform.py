# classes/platform.py
import pygame
import settings

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, height=20):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(settings.PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = settings.SCROLL_SPEED

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()