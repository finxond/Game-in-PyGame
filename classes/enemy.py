# classes/enemy.py
import pygame
import random
import settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = settings.SCREEN_WIDTH + random.randint(20,100)
        self.rect.bottom = settings.SCREEN_HEIGHT - 60

        diff = settings.difficulty_settings[settings.difficulty]
        self.speed = random.uniform(diff["enemy_speed_min"], diff["enemy_speed_max"])
        self.anim_index = 0
        self.last_anim_time = 0
        self.anim_delay = 200

    def update(self):
        self.rect.x -= self.speed
        now = pygame.time.get_ticks()
        if now - self.last_anim_time >= self.anim_delay:
            self.anim_index = (self.anim_index + 1) % len(self.frames)
            self.image = self.frames[self.anim_index]
            self.last_anim_time = now
        if self.rect.right < 0:
            self.kill()