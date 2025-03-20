import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego con Bosque y Skin del Personaje")

#Fondo del bosque
background_path = "C:/Users/sala311/Downloads/bosque 2d.jpg"
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Cargar la "skin" del personaje
player_skin_path = "C:/Users/sala311/Downloads/personaje.png"  # Cambia esta ruta al archivo de tu personaje
player_skin = pygame.image.load(player_skin_path)
player_skin = pygame.transform.scale(player_skin, (40, 60))  # Escalar al tamaño del jugador

# Colores
GREEN = (0, 255, 0)

# Jugador
player_size = (40, 60)  # Tamaño del jugador, solo usado para colisiones
player_x = 100
player_y = HEIGHT - player_size[1] - 50
player_speed = 5
player_jump_speed = -10
gravity = 0.5
is_jumping = False
vertical_speed = 0

# Plataforma
platform = pygame.Rect(300, 250, 200, 20)
platform_active = False

# Suelo
ground = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Moverse a la izquierda con "A"
        player_x -= player_speed
    if keys[pygame.K_d]:  # Moverse a la derecha con "D"
        player_x += player_speed

    # Saltar con "W"
    if keys[pygame.K_w] and not is_jumping and (player_y >= HEIGHT - player_size[1] - 50 or platform_active):
        is_jumping = True
        vertical_speed = player_jump_speed

    # Gravedad y salto
    if is_jumping:
        player_y += vertical_speed
        vertical_speed += gravity

    # Detectar colisión con el suelo
    if player_y >= HEIGHT - player_size[1] - 50:
        player_y = HEIGHT - player_size[1] - 50
        is_jumping = False

    # Detectar colisión con la plataforma
    if platform.colliderect(pygame.Rect(player_x, player_y, *player_size)):
        if vertical_speed > 0:  # Solo aterriza si cae desde arriba
            player_y = platform.y - player_size[1]
            is_jumping = False
            platform_active = True
    else:
        platform_active = False

    # Restricción del movimiento horizontal
    player_x = max(0, min(WIDTH - player_size[0], player_x))

    # Dibujar elementos
    screen.blit(background, (0, 0))  # Dibujar el fondo
    screen.blit(player_skin, (player_x, player_y))  # Dibujar la "skin" del jugador
    pygame.draw.rect(screen, GREEN, ground)  # Suelo
    pygame.draw.rect(screen, (70, 80, 70), platform)  # Plataforma

    pygame.display.flip()
    clock.tick(60)
