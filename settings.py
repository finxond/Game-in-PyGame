# settings.py
import pygame
import os

# Путь к папке с ресурсами
BASE_PATH = "resources/"

SCREEN_WIDTH, SCREEN_HEIGHT = 910, 512
TITLE = "Emma in danger: Escape from the Forest"
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
GOLD = (255, 215, 0)
DARK_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BLUE = (50, 100, 255)
GRAY = (128, 128, 128)
PLATFORM_COLOR = (101, 67, 33)
HEALTH_COLOR = (255, 50, 50)
AMMO_COLOR = (50, 100, 255)

GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_FORCE = -18
SCROLL_SPEED = 3
BULLET_SPEED = 12
WINNING_SCORE = 500

difficulty = "normal"
difficulty_settings = {
    "easy": {
        "enemy_speed_min": 1.5,
        "enemy_speed_max": 3.5,
        "enemy_spawn_delay": 2500,
        "max_enemies": 6,
        "score_multiplier": 1.0
    },
    "normal": {
        "enemy_speed_min": 2,
        "enemy_speed_max": 5,
        "enemy_spawn_delay": 2000,
        "max_enemies": 8,
        "score_multiplier": 1.0
    },
    "hard": {
        "enemy_speed_min": 3,
        "enemy_speed_max": 6,
        "enemy_spawn_delay": 1500,
        "max_enemies": 10,
        "score_multiplier": 1.5
    }
}

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"