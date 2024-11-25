import pygame
import os
import sys

SCORES_FILE = "scores.txt"

def get_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as file:
        return [int(line.strip()) for line in file.readlines()]

def save_score(score):
    with open(SCORES_FILE, "a") as file:
        file.write(f"{score}\n")

def display_scores(screen):
    scores = sorted(get_scores(), reverse=True)  # Ordenar puntuaciones descendente
    font = pygame.font.Font(None, 50)
    screen.fill((0, 0, 0))

    title = font.render("High Scores", True, (255, 255, 255))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

    for i, score in enumerate(scores[:10]):  # Mostrar solo los 10 primeros
        score_text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
        screen.blit(score_text, (100, 150 + i * 50))

    pygame.display.flip()
    wait_for_key()

def display_instructions(screen):
    font = pygame.font.Font(None, 50)
    screen.fill((0, 0, 0))

    instructions = [
        "Use arrow keys to move.",
        "Press SPACE to shoot.",
        "Destroy enemies to gain points.",
        "Survive as long as possible!",
        "Press R to return to the menu.",
    ]

    for i, line in enumerate(instructions):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (50, 100 + i * 60))

    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
