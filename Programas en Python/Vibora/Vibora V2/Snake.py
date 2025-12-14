import pygame
import random

import utils

# inicializar pygame
pygame.init()

# tamaño de la ventana
ancho = 600
alto = 400
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Snake")

# tamaño de bloques
tam_bloque = 20
velocidad = 10.0

# reloj
clock = pygame.time.Clock()

def mostrar_mensaje(msg: str, color: tuple[int, int, int]):
    fuente = pygame.font.SysFont(None, 35)
    texto = fuente.render(msg, True, color)
    ventana.blit(texto, (ancho / 6, alto / 3))

def snake():
    global velocidad

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
            ventana.fill(utils.negro)
            mostrar_mensaje("Perdiste! Presiona C para continuar o Q para salir", utils.rojo)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        snake()
            
            # se reinicia la velocidad
            velocidad = 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    dx = -tam_bloque
                    dy = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    dx = tam_bloque
                    dy = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    dy = -tam_bloque
                    dx = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    dy = tam_bloque
                    dx = 0

        x += dx
        y += dy

        # Si la víbora choca con los bordes
        if x >= ancho or x < 0 or y >= alto or y < 0:
            game_close = True

        ventana.fill(utils.negro)

        # Dibujar comida
        pygame.draw.rect(ventana, utils.rojo, [comida_x, comida_y, tam_bloque, tam_bloque])

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
            pygame.draw.rect(ventana, utils.color(), [bloque[0], bloque[1], tam_bloque, tam_bloque])

        pygame.display.update()

        # Comer
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, ancho - tam_bloque) / 20.0) * 20
            comida_y = round(random.randrange(0, alto - tam_bloque) / 20.0) * 20
            longitud_cuerpo += 1
            velocidad += 0.2

        clock.tick(velocidad)

    pygame.quit()
    quit()

if __name__ == "__main__":
    snake()