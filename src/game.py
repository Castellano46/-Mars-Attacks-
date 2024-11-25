import pygame
import sys
import random
from src.player import Player
from src.bullet import Bullet
from src.enemy import Enemy
from src.explosion import Explosion
from src.utils import load_assets, reset_game_state
from src.scores import save_score, get_scores
from src.scores import display_scores, display_instructions

class MarsAttacksGame:
    def __init__(self):
        pygame.init()

        # Configuración de pantalla
        self.width, self.height = 700, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🛸👽 Mars Attacks! 👽🛸")

        # Reloj y estado del juego
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.paused = False
        self.in_menu = True
        self.menu_index = 0  # Índice para navegar por el menú

        # Cargar recursos
        try:
            self.assets = load_assets()
        except FileNotFoundError as e:
            print(f"Error al cargar recursos: {e}")
            sys.exit()

        self.font = pygame.font.Font(None, 36)

        # Inicializar elementos del juego
        self.reset_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.in_menu:  # Si estamos en el menú principal
                    if event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        if self.menu_index == 0:  # Iniciar juego
                            self.in_menu = False
                            self.reset_game()
                        elif self.menu_index == 1:  # Ver puntuaciones
                            self.show_scores()
                        elif self.menu_index == 2:  # Leer instrucciones
                            self.show_instructions()
                        elif self.menu_index == 3:  # Salir del juego
                            pygame.quit()
                            sys.exit()
                elif self.game_over:  # Si el juego terminó
                    if event.key == pygame.K_r:  # Volver al menú principal
                        self.in_menu = True
                else:  # Si estamos jugando
                    if event.key == pygame.K_LEFT and not self.paused:
                        self.player.move_left()
                    elif event.key == pygame.K_RIGHT and not self.paused:
                        self.player.move_right()
                    elif event.key == pygame.K_SPACE and not self.paused:
                        bullet = Bullet(self.player.rect, self.assets['bullet'])
                        self.bullets.append(bullet)
                        self.assets['sounds']['shoot'].play()
                    elif event.key == pygame.K_p:  # Pausar/Reanudar el juego
                        self.paused = not self.paused
            if event.type == pygame.KEYUP and not self.paused:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.stop()

    def update(self):
        if self.game_over or self.paused or self.in_menu:
            return

        self.player.update()
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.rect.colliderect(self.player.rect):
                self.enemies.remove(enemy)
                self.lives -= 1
                self.assets['sounds']['explosion'].play()
                if self.lives <= 0:
                    self.end_game()
            elif enemy.rect.top > self.height:
                self.enemies.remove(enemy)

        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.explosions.append(Explosion(enemy.rect, self.assets['explosion']))
                    self.assets['sounds']['explosion'].play()
                    self.score += 10
                    break

        if random.randint(0, 100) < 2 + self.level:
            self.enemies.append(Enemy(self.width, self.assets['enemy']))

        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.finished:
                self.explosions.remove(explosion)

        if self.score > self.level * 50:
            self.level += 1

    def draw(self):
        if self.in_menu:  # Dibuja el menú principal
            self.screen.fill((0, 0, 0))
            options = ["Start Game", "View Scores", "Instructions", "Exit"]
            for i, option in enumerate(options):
                color = (255, 255, 0) if i == self.menu_index else (255, 255, 255)
                text = self.font.render(option, True, color)
                self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 3 + i * 50))
        else:
            # Dibuja el fondo
            self.screen.blit(self.background, (0, 0))

            # Dibuja al jugador
            self.player.draw(self.screen)

            # Dibuja las balas
            for bullet in self.bullets:
                bullet.draw(self.screen)

            # Dibuja a los enemigos
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Dibuja las explosiones
            for explosion in self.explosions:
                explosion.draw(self.screen)

            # Dibuja la puntuación y el nivel
            score_text = self.font.render(f"Score: {self.score:04d}", True, (255, 255, 255))
            level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (10, 40))

            # Dibuja los corazones (vidas)
            for i in range(self.lives):
                self.screen.blit(self.assets['heart'], (self.width - (i + 1) * (self.assets['heart'].get_width() + 10), 10))

            # Si el juego ha terminado, muestra "GAME OVER"
            if self.game_over:
                game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
                menu_text = self.font.render("Press R to return to Menu", True, (255, 255, 255))
                self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 3))
                self.screen.blit(menu_text, (self.width // 2 - menu_text.get_width() // 2, self.height // 1.5))

            # Si el juego está pausado, muestra "Paused"
            if self.paused:
                paused_text = self.font.render("PAUSED", True, (255, 255, 0))
                self.screen.blit(paused_text, (self.width // 2 - paused_text.get_width() // 2, self.height // 2))

        # Actualiza la pantalla
        pygame.display.flip()

    def reset_game(self):
        self.player, self.bullets, self.enemies, self.explosions, self.lives, self.score, self.level = reset_game_state(
            self.width, self.height, self.assets
        )
        self.background = self.assets["background"]
        self.game_over = False
        self.paused = False

    def end_game(self):
        self.game_over = True
        self.assets['sounds']['game_over'].play()
        save_score(self.score)  # Guardar la puntuación al finalizar el juego

    def show_scores(self):
        scores = get_scores()
        font = pygame.font.Font(None, 50)
        self.screen.fill((0, 0, 0))

        title = font.render("High Scores", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

        for i, score in enumerate(scores[:10]):  # Mostrar solo los 10 primeros
            score_text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
            self.screen.blit(score_text, (100, 150 + i * 50))

        pygame.display.flip()
        self.wait_for_key()

    def show_instructions(self):
        display_instructions(self.screen)  # Llama a la función desde scores.py

    def run(self):
        while True:
            self.handle_events()
            if not self.in_menu:  # Solo actualizar y dibujar si estamos jugando
                self.update()
                self.draw()
            self.clock.tick(60)
