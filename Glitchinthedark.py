import pygame
import sys
import random

pygame.init()

ANCHO = 640
ALTO = 480

COLOR_FONDO = (0, 0, 0)          # negro de fondo
COLOR_JUGADOR = (0, 100, 255)    # azul para el jugador
COLOR_PARED = (100, 100, 100)    # gris para las paredes
COLOR_META = (0, 200, 0)         # verde para la meta
COLOR_TEXTO = (255, 255, 255)    # blanco para texto
COLOR_LUZ = (255, 255, 255)      # blanco para la luz

# Creamos la ventana del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("GLITCH IN THE DARK")

# Fuente para mostrar texto en pantalla
fuente = pygame.font.SysFont(None, 36)

# Control de tiempo del juego
reloj = pygame.time.Clock()
TIEMPO_MOSTRAR = 2000  # 2000 milisegundos = 2 segundos
inicio_tiempo = pygame.time.get_ticks()

# Posición inicial del jugador
jugador_ancho = 25
jugador_alto = 25
jugador_x = 50
jugador_y = 50
jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_ancho, jugador_alto)

# Velocidad del jugador
velocidad = 3

# Meta final, siempre en una esquina diferente cada juego
meta_rect = pygame.Rect(ANCHO - 60, ALTO - 60, 30, 30)

# Guardamos la posición inicial para reiniciar al chocar
pos_inicial = (jugador_x, jugador_y)

# Contador de choques para hacer el juego más difícil
choques = 0
MAX_CHOQUES = 3

# Estado del juego: jugando o fin
estado = "jugando"

# Creamos un laberinto diferente en cada partida
paredes = []

# Zona segura alrededor del inicio y la meta para no poner paredes ahí
zona_inicio = pygame.Rect(0, 0, 150, 150)
zona_meta = pygame.Rect(ANCHO - 150, ALTO - 150, 150, 150)

# Agregamos muros fijos alrededor de la pantalla
paredes.append(pygame.Rect(0, 0, ANCHO, 20))
paredes.append(pygame.Rect(0, 0, 20, ALTO))
paredes.append(pygame.Rect(0, ALTO - 20, ANCHO, 20))
paredes.append(pygame.Rect(ANCHO - 20, 0, 20, ALTO))

# Creamos paredes aleatorias para un laberinto más difícil y diferente cada vez
while len(paredes) < 16:
    if len(paredes) % 2 == 0:
        # pared vertical aleatoria
        x = random.randrange(80, ANCHO - 100, 30)
        y = random.randrange(40, ALTO - 190, 30)
        ancho = 20
        alto = random.randrange(140, 240)
    else:
        # pared horizontal aleatoria
        x = random.randrange(80, ANCHO - 240, 30)
        y = random.randrange(60, ALTO - 120, 30)
        ancho = random.randrange(140, 260)
        alto = 20

    rect = pygame.Rect(x, y, ancho, alto)
    if rect.colliderect(zona_inicio) or rect.colliderect(zona_meta):
        continue
    paredes.append(rect)

# Mensaje de texto para la pantalla
def dibujar_texto(texto, x, y):
    superficie = fuente.render(texto, True, COLOR_TEXTO)
    pantalla.blit(superficie, (x, y))

# Bucle principal del juego
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if estado == "fin" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                jugando = False

    # Limpiamos la pantalla cada fotograma
    pantalla.fill(COLOR_FONDO)

    if estado == "jugando":
        # Movimiento con las flechas del teclado
        teclas = pygame.key.get_pressed()
        movimiento_x = 0
        movimiento_y = 0
        if teclas[pygame.K_LEFT]:
            movimiento_x = -velocidad
        if teclas[pygame.K_RIGHT]:
            movimiento_x = velocidad
        if teclas[pygame.K_UP]:
            movimiento_y = -velocidad
        if teclas[pygame.K_DOWN]:
            movimiento_y = velocidad

        jugador_rect.x += movimiento_x
        jugador_rect.y += movimiento_y

        # Colisión con paredes grises
        choque = False
        for pared in paredes:
            if jugador_rect.colliderect(pared):
                choque = True
                break
        if choque:
            choques += 1
            jugador_rect.x, jugador_rect.y = pos_inicial
            if choques >= MAX_CHOQUES:
                estado = "fin"
                gano = False

        # Si el jugador llega a la meta gana
        if jugador_rect.colliderect(meta_rect):
            estado = "fin"
            gano = True

        # Dibujamos las paredes grises
        for pared in paredes:
            pygame.draw.rect(pantalla, COLOR_PARED, pared)

        # Dibujamos la meta verde
        pygame.draw.rect(pantalla, COLOR_META, meta_rect)

        # Dibujamos el jugador azul
        pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador_rect)

        # Mostramos los choques en pantalla
        dibujar_texto(f"Choques: {choques}/{MAX_CHOQUES}", 20, 30)

        # Controlamos el tiempo antes de la oscuridad total
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual > inicio_tiempo + TIEMPO_MOSTRAR:
            luz_ancho = 80
            luz_alto = 80
            luz_x = jugador_rect.centerx - luz_ancho // 2
            luz_y = jugador_rect.centery - luz_alto // 2

            pantalla_oscura = pygame.Surface((ANCHO, ALTO))
            pantalla_oscura.fill((0, 0, 0))
            pygame.draw.rect(pantalla_oscura, (255, 255, 255), (luz_x, luz_y, luz_ancho, luz_alto))
            pantalla.blit(pantalla_oscura, (0, 0), special_flags=pygame.BLEND_MULT)

    elif estado == "fin":
        # Mensaje de victoria o derrota
        if gano:
            dibujar_texto("¡Ganaste! Llegaste a la meta.", 130, 180)
        else:
            dibujar_texto("Perdiste. Choqueaste muchas veces.", 100, 180)
        dibujar_texto("Presiona ESC para salir", 170, 240)

    # Actualizamos la pantalla y limitamos la velocidad
    pygame.display.flip()
    reloj.tick(60)

# Cerramos Pygame y salimos del programa
pygame.quit()
sys.exit()
