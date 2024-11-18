import pygame
import os
from src.player import Player

def load_assets():
    screen_width, screen_height = 700, 720  
    background = pygame.image.load("assets/images/fondo.jpg")
    bg_width, bg_height = background.get_size()

    scale_factor = min(screen_width / bg_width, screen_height / bg_height)
    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)

    assets = {
        "background": pygame.transform.scale(background, (new_width, new_height)),
        "player": pygame.transform.scale(pygame.image.load("assets/images/tank.png"), (80, 80)),
        "bullet": pygame.transform.scale(pygame.image.load("assets/images/disparo.png"), (50, 50)),
        "enemy": pygame.transform.scale(pygame.image.load("assets/images/ovni.png"), (60, 60)),
        "heart": pygame.transform.scale(pygame.image.load("assets/images/corazon.png"), (30, 30)),
        "explosion": [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/explosion_frame_{i}.png"), (60, 60)
            ) for i in range(5)
        ],
        "sounds": {
            "shoot": pygame.mixer.Sound("assets/sounds/shoot.wav"),
            "explosion": pygame.mixer.Sound("assets/sounds/explosion.wav"),
            "game_over": pygame.mixer.Sound("assets/sounds/game_over.wav"),
        }
    }

    # Configuración de volumen para los sonidos
    assets["sounds"]["shoot"].set_volume(0.5)
    assets["sounds"]["explosion"].set_volume(0.7)
    assets["sounds"]["game_over"].set_volume(0.8)

    return assets


def reset_game_state(screen_width, screen_height, assets):
    player = Player(screen_width, screen_height, assets['player'])
    bullets = []
    enemies = []
    explosions = []
    lives = 3
    score = 0
    level = 1
    return player, bullets, enemies, explosions, lives, score, level
