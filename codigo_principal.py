import pygame
import sys

# Constantes globales
WIDTH, HEIGHT = 800, 600
FRAME_WIDTH, FRAME_HEIGHT = 40, 80  # Tamaño del jugador
FPS = 60
GRAVITY = 0.5
FALL_SPEED = 10  # Velocidad de caída
JUMP_STRENGTH = -22

# Inicializar Pygame
def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juego 2D con Skin y Plataformas con Imágenes")
    return screen

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
            "background": r"C:\Users\jeiso\OneDrive\Escritorio\Bosque 2d.jpg",
            "platforms": [
                pygame.Rect(100, 400, 200, 20),
                pygame.Rect(400, 300, 150, 20),
                pygame.Rect(600, 200, 200, 20),
            ],
        },
        {
            "background": r"C:\Users\jeiso\OneDrive\Escritorio\Bosque 2d.jpg",
            "platforms": [
                pygame.Rect(50, 500, 250, 20),
                pygame.Rect(300, 350, 200, 20),
                pygame.Rect(650, 250, 150, 20),
            ],
        },
    ]
    return scenes

# Función principal
def main():
    screen = initialize_game()
    clock = pygame.time.Clock()

    # Cargar datos de las escenas
    scenes = create_scene_data()
    current_scene = 0  # Escena inicial

    # Cargar fondo y plataformas
    background = load_image(scenes[current_scene]["background"], scale=(WIDTH, HEIGHT))
    platforms = scenes[current_scene]["platforms"]

    # Cargar imágenes de las plataformas
    platform_image = load_image(r"C:\Users\jeiso\OneDrive\Escritorio\plataforma.jpg")

    # Cargar la skin del jugador
    skin_path = r"C:\Users\jeiso\OneDrive\Escritorio\campesino 2d.jpg"
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