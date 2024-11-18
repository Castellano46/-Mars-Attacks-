import pygame
import random


class Enemy:
    def __init__(self, screen_width, image):
        self.image = image
        self.rect = self.image.get_rect(midtop=(random.randint(0, screen_width - image.get_width()), 0))
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
