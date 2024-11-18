import pygame


class Explosion:
    def __init__(self, enemy_rect, explosion_images):
        self.frames = explosion_images
        self.current_frame = 0
        self.rect = self.frames[0].get_rect(center=enemy_rect.center)
        self.frame_timer = 0
        self.finished = False

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 5:  # Cambia de frame cada 5 ticks
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            screen.blit(self.frames[self.current_frame], self.rect)
