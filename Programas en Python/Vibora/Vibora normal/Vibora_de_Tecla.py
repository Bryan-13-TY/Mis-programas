import pygame
import random

# Inicializar pygame
pygame.init()

# Tamaño de la ventana
ancho = 600 # 600
alto = 400 # 400
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego de la Víborita (Snake)")

# Colores
negro = (0, 0, 0)
verde = (0, 255, 0)
rojo = (255, 0, 0)
blanco = (255, 255, 255)

# Tamaño de bloques
tam_bloque = 20
velocidad = 10

# Reloj
clock = pygame.time.Clock()

def mostrar_mensaje(msg, color):
    fuente = pygame.font.SysFont(None, 30)
    texto = fuente.render(msg, True, color)
    ventana.blit(texto, (ancho/6, alto/3))

def juego():
    game_over = False
    game_close = False

    x = ancho // 2
    y = alto // 2

    dx = 0
    dy = 0

    cuerpo = []
    longitud_cuerpo = 1

    # Comida al azar
    comida_x = round(random.randrange(0, ancho - tam_bloque) / 20.0) * 20
    comida_y = round(random.randrange(0, alto - tam_bloque) / 20.0) * 20

    while not game_over:

        while game_close:
            ventana.fill(negro)
            mostrar_mensaje("Perdiste! Presiona C para continuar o Q para salir", rojo)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        juego()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -tam_bloque
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = tam_bloque
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -tam_bloque
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = tam_bloque
                    dx = 0

        x += dx
        y += dy

        # Si la víbora choca con los bordes
        if x >= ancho or x < 0 or y >= alto or y < 0:
            game_close = True

        ventana.fill(negro)

        # Dibujar comida
        pygame.draw.rect(ventana, rojo, [comida_x, comida_y, tam_bloque, tam_bloque])

        # Actualizar cuerpo
        cabeza = []
        cabeza.append(x)
        cabeza.append(y)
        cuerpo.append(cabeza)

        if len(cuerpo) > longitud_cuerpo:
            del cuerpo[0]

        # Si la cabeza toca el cuerpo = game over
        for parte in cuerpo[:-1]:
            if parte == cabeza:
                game_close = True

        # Dibujar víbora
        for bloque in cuerpo:
            pygame.draw.rect(ventana, verde, [bloque[0], bloque[1], tam_bloque, tam_bloque])

        pygame.display.update()

        # Comer
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, ancho - tam_bloque) / 20.0) * 20
            comida_y = round(random.randrange(0, alto - tam_bloque) / 20.0) * 20
            longitud_cuerpo += 1

        clock.tick(velocidad)

    pygame.quit()
    quit()

juego()
