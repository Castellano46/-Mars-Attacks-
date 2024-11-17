import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 700, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("🛸👽 Mars Attacks! 👽🛸")

# Cargar imágenes y escalarlas
player_image = pygame.image.load("tank.png")
player_image = pygame.transform.scale(player_image, (80, 80))

bullet_image = pygame.image.load("disparo.png")
bullet_image = pygame.transform.scale(bullet_image, (50, 50))

enemy_image = pygame.image.load("ovni.png")
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

background_image = pygame.image.load("fondo.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

heart_image = pygame.image.load("corazon.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Jugador
player_rect = player_image.get_rect()
player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
player_speed = 15

# Bala
bullet_rect = bullet_image.get_rect()
bullet_speed = 10
bullets = []

# Enemigo
enemy_rect = enemy_image.get_rect()
enemy_speed = 5
enemies = []

# Vidas
lives = 3  # Número de vidas iniciales

# Reloj
clock = pygame.time.Clock()

# Mantener registro de teclas presionadas
keys_pressed = {'left': False, 'right': False}

# Bucle Principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Manejar movimientos del jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keys_pressed['left'] = True
            elif event.key == pygame.K_RIGHT:
                keys_pressed['right'] = True
            elif event.key == pygame.K_SPACE:
                bullet_rect = bullet_image.get_rect()
                bullet = {
                    'rect': pygame.Rect(
                        player_rect.x + player_rect.width // 2 - bullet_rect.width // 2,
                        player_rect.y,
                        bullet_rect.width,
                        bullet_rect.height
                    ),
                    'image': bullet_image
                }
                bullets.append(bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys_pressed['left'] = False
            elif event.key == pygame.K_RIGHT:
                keys_pressed['right'] = False

    # Actualizar posición del jugador
    if keys_pressed['left'] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys_pressed['right'] and player_rect.right < width:
        player_rect.x += player_speed

    # Actualizar posición de las balas
    for bullet in bullets:
        bullet['rect'].y -= bullet_speed

    # Generar enemigos aleatorios
    if random.randint(0, 100) < 5:
        enemy_rect = enemy_image.get_rect()
        enemy_rect.x = random.randint(0, width - enemy_rect.width)
        enemies.append(enemy_rect.copy())

    # Actualizar posición de los enemigos
    for enemy in enemies:
        enemy.y += enemy_speed

    # Colisiones entre balas y enemigos
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if enemy.colliderect(bullet['rect']):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Colisiones entre jugador y enemigos
    for enemy in enemies[:]:
        if player_rect.colliderect(enemy):
            enemies.remove(enemy)
            lives -= 1  # Reducir una vida
            if lives <= 0:
                pygame.quit()
                sys.exit()

    # Limpiar la pantalla con el fondo
    screen.blit(background_image, (0, 0))

    # Dibujar al jugador
    screen.blit(player_image, player_rect)

    # Dibujar las balas
    for bullet in bullets:
        screen.blit(bullet['image'], bullet['rect'].topleft)

    # Dibujar los enemigos
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Dibujar las vidas en la esquina superior derecha
    for i in range(lives):
        screen.blit(heart_image, (width - (i + 1) * (heart_image.get_width() + 10), 10))

    # Actualizar la pantalla
    pygame.display.flip()

    # Establecer límite de FPS
    clock.tick(30)
  