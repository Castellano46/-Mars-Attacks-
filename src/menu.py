import pygame
import sys
from src.utils import load_assets

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.assets = load_assets()
        self.options = ["Play", "Instructions", "Scores", "Exit"]
        self.selected = 0

    def draw(self):
        self.screen.blit(self.assets["background"], (0, 0))
        title = self.font.render("Mars Attacks! Main Menu", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200 + i * 60))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
        return None
