import pygame
import os
import sys

# Constantes globales
WIDTH, HEIGHT = 800, 600
FRAME_WIDTH = 60 #Tamaño del jugador
FRAME_HEIGHT = 80  # Tamaño del jugador
FPS = 60
GRAVITY = 0.5
FALL_SPEED = 10  # Velocidad de caída
JUMP_STRENGTH = -22

# Inicializar Pygame
def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("La tierra que llueve")
    return screen

icono = pygame.image.load("assets/campesino_2d.png")
pygame.display.set_icon(icono)

# Función para cargar imágenes
def load_image(path, scale=None):
    image = pygame.image.load(path)
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

# Crear datos de las escenas
def create_scene_data():
    scenes = [
        {
            "background": "assets/Bosque 2d.jpg",
            "platforms": [
                pygame.Rect(100, 400, 200, 30),
                pygame.Rect(400, 300, 150, 30),
                pygame.Rect(600, 200, 200, 30),
            ],
        },
        {
            "background": "assets/Bosque 2d.jpg",
            "platforms": [
                pygame.Rect(50, 500, 250, 30),
                pygame.Rect(300, 350, 200, 30),
                pygame.Rect(650, 250, 150, 30),
            ],
        },
    ]
    return scenes

# Nueva función para la pantalla de inicio con imagen de fondo
def start_screen(screen):
    # Cargar la imagen de fondo
    background_image = load_image("assets/Bosque 2d.jpg", scale=(WIDTH, HEIGHT))
    
    font = pygame.font.Font(None, 36)
    title_text = font.render("La tierra que llueve", True, (0, 0, 0))
    background1_text = font.render("Presiona espacio para empezar", True, (0, 0, 0))
    background2_text = font.render("Creado por: Jeison Gomez y Alejandro Campillo", True, (0, 0, 0))
    clock = pygame.time.Clock()

    selected_background = None
    while selected_background is None:
        # Dibujar la imagen de fondo
        screen.blit(background_image, (0, 0))
        
        # Dibujar los textos
        screen.blit(title_text, (50, 200))
        screen.blit(background1_text, (50, 250))
        screen.blit(background2_text, (50, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    selected_background = "assets/Bosque 2d.jpg"
                elif event.key == pygame.K_2:
                    selected_background = "assets/Bosque 2d.jpg"

        pygame.display.flip()
        clock.tick(30)

    return selected_background

# Función principal
def main():
    screen = initialize_game()
    clock = pygame.time.Clock()

    # Llamar a la pantalla de inicio
    selected_background = start_screen(screen)

    # Crear datos de las escenas con el fondo seleccionado
    scenes = create_scene_data()
    for scene in scenes:
        scene["background"] = selected_background

    current_scene = 0  # Escena inicial

    # Cargar fondo y plataformas
    background = load_image(scenes[current_scene]["background"], scale=(WIDTH,HEIGHT))
    platforms = scenes[current_scene]["platforms"]

    # Cargar imágenes de las plataformas
    platform_image = load_image("assets/plataforma 2d.png")

    # Cargar la skin del jugador
    skin_path = "assets/campesino_2d.png"
    player_skin = load_image(skin_path, scale=(FRAME_WIDTH, FRAME_HEIGHT))

    # Variables del jugador
    player_x, player_y = 100, 500
    player_speed = 5
    vertical_speed = 0
    is_jumping = False
    falling = False

    # Suelo
    ground = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        #ruta = os.path.join("assets", "campesino_2d.png")
        if keys[pygame.K_a]:  # Mover izquierda
            player_x -= player_speed
        if keys[pygame.K_d]:  # Mover derecha
            player_x += player_speed
        if keys[pygame.K_w] and not is_jumping and not falling:  # Saltar
            is_jumping = True
            vertical_speed = JUMP_STRENGTH

        if is_jumping:
            player_y += vertical_speed
            vertical_speed += GRAVITY
        if falling:
            player_y += FALL_SPEED

        player_x = max(0, min(WIDTH, player_x))

        if player_x >= WIDTH:  # Límite derecho
            current_scene += 1
            if current_scene >= len(scenes):  # Reiniciar si no hay más escenas
                current_scene = 0
            background = load_image(scenes[current_scene]["background"], scale=(WIDTH, HEIGHT))
            platforms = scenes[current_scene]["platforms"]
            player_x = 0  # Reiniciar posición al borde izquierdo

        if player_y >= ground.y - FRAME_HEIGHT:
            player_y = ground.y - FRAME_HEIGHT
            is_jumping = False
            falling = False

        on_platform = False
        for platform in platforms:
            if platform.colliderect(pygame.Rect(player_x, player_y, FRAME_WIDTH, FRAME_HEIGHT)):
                if vertical_speed > 0:
                    player_y = platform.y - FRAME_HEIGHT
                    is_jumping = False
                    falling = False
                    on_platform = True

        if not on_platform and player_y < ground.y - FRAME_HEIGHT:
            falling = True

        # Dibujar fondo
        screen.blit(background, (0, 0))

        # Dibujar plataformas con imágenes
        for platform in platforms:
            scaled_image = pygame.transform.scale(platform_image, (platform.width, platform.height))
            screen.blit(scaled_image, (platform.x, platform.y))

        # Dibujar jugador (skin)
        screen.blit(player_skin, (player_x, player_y))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()