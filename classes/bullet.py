# classes/bullet.py
import pygame
from settings import BULLET_SPEED, SCREEN_WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()# classes/bullet.py
import pygame
import settings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = settings.BULLET_SPEED * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > settings.SCREEN_WIDTH or self.rect.right < 0:
            self.kill()