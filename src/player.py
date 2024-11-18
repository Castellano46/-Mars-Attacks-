import pygame


class Player:
    def __init__(self, screen_width, screen_height, image):
        self.image = image
        self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height - 20))
        self.speed = 10
        self.direction = 0

    def move_left(self):
        self.direction = -1

    def move_right(self):
        self.direction = 1

    def stop(self):
        self.direction = 0

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > pygame.display.get_surface().get_width():
            self.rect.right = pygame.display.get_surface().get_width()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
