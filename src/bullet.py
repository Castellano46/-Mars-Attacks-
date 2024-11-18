import pygame


class Bullet:
    def __init__(self, player_rect, image):
        self.image = image
        self.rect = self.image.get_rect(midbottom=player_rect.midtop)
        self.speed = 12

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
