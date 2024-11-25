from src.game import MarsAttacksGame
from src.menu import MainMenu
from src.utils import load_assets
from src.scores import display_scores, display_instructions
import pygame
import sys

if __name__ == "__main__":
    pygame.init()
    width, height = 700, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("🛸👽 Mars Attacks! 👽🛸")

    menu = MainMenu(screen)

    while True:
        menu.draw()
        choice = menu.handle_events()

        if choice == "Play":
            game = MarsAttacksGame()
            game.run()
        elif choice == "Instructions":
            display_instructions(screen)
        elif choice == "Scores":
            display_scores(screen)
        elif choice == "Exit":
            pygame.quit()
            sys.exit()
