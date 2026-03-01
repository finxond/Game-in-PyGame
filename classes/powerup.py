# classes/powerup.py
import pygame
import random
import settings

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['health', 'ammo'])
        self.image = pygame.Surface((25,25), pygame.SRCALPHA)
        color = settings.HEALTH_COLOR if self.type == 'health' else settings.AMMO_COLOR
        pygame.draw.circle(self.image, color, (12,12), 12)
        pygame.draw.circle(self.image, settings.WHITE, (12,12), 8)
        self.rect = self.image.get_rect()
        self.rect.x = settings.SCREEN_WIDTH + random.randint(20,100)
        self.rect.bottom = settings.SCREEN_HEIGHT - 60
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()