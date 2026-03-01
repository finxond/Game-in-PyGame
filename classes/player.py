# classes/player.py
import pygame
import settings
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, walk_right, walk_left, all_sprites, bullets, platforms,
                 jump_sound, shoot_sound, hit_sound, bullet_img):
        super().__init__()
        self.right_frames = walk_right
        self.left_frames = walk_left
        self.image = self.right_frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = settings.SCREEN_HEIGHT - 60
        self.rect.centerx = 100

        self.velocity_y = 0
        self.on_ground = True
        self.facing_right = True
        self.anim_index = 0
        self.last_anim_time = 0
        self.anim_delay = 120

        self.health = 3
        self.ammo = 8
        self.score = 0
        self.invulnerable = False
        self.invulnerable_end = 0
        self.is_moving = False

        self.all_sprites = all_sprites
        self.bullets = bullets
        self.platforms = platforms
        self.jump_sound = jump_sound
        self.shoot_sound = shoot_sound
        self.hit_sound = hit_sound
        self.bullet_img = bullet_img

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.animate()
        self.check_invulnerability()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= settings.PLAYER_SPEED
            self.facing_right = False
            self.is_moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += settings.PLAYER_SPEED
            self.facing_right = True
            self.is_moving = True
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def jump(self):
        if self.on_ground:
            self.velocity_y = settings.JUMP_FORCE
            self.on_ground = False
            if self.jump_sound:
                self.jump_sound.play()

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            direction = 1 if self.facing_right else -1
            x = self.rect.right if self.facing_right else self.rect.left
            bullet = Bullet(x, self.rect.centery, direction, self.bullet_img)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)
            if self.shoot_sound:
                self.shoot_sound.play()

    def apply_gravity(self):
        self.velocity_y += settings.GRAVITY
        self.rect.y += self.velocity_y

        self.on_ground = False
        for plat in self.platforms:
            if self.rect.colliderect(plat.rect) and self.velocity_y > 0:
                self.rect.bottom = plat.rect.top
                self.velocity_y = 0
                self.on_ground = True
                break

        ground = settings.SCREEN_HEIGHT - 60
        if self.rect.bottom >= ground:
            self.rect.bottom = ground
            self.velocity_y = 0
            self.on_ground = True

    def animate(self):
        now = pygame.time.get_ticks()
        frames = self.right_frames if self.facing_right else self.left_frames
        if self.is_moving or not self.on_ground:
            if now - self.last_anim_time >= self.anim_delay:
                self.anim_index = (self.anim_index + 1) % len(frames)
                self.image = frames[self.anim_index]
                self.last_anim_time = now
        else:
            self.image = frames[0]
            self.anim_index = 0

    def take_damage(self):
        if not self.invulnerable:
            self.health -= 1
            self.invulnerable = True
            self.invulnerable_end = pygame.time.get_ticks() + 2000
            if self.hit_sound:
                self.hit_sound.play()
            return True
        return False

    def check_invulnerability(self):
        if self.invulnerable and pygame.time.get_ticks() >= self.invulnerable_end:
            self.invulnerable = False

    def add_score(self, points):
        mult = settings.difficulty_settings[settings.difficulty]["score_multiplier"]
        self.score += int(points * mult)