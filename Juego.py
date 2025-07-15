import pygame
from Funciones.Funciones_Generales import *
from Funciones.Funciones_Estados import *

pygame.init()
DIMENSIÓN_PANTALLA = ((600, 620))
pantalla = pygame.display.set_mode(DIMENSIÓN_PANTALLA)
pygame.display.set_caption("Serpientes y Escaleras")
pygame.display.set_icon(ícono)

correr = True
estado_juego = "inicio"
resolución = None
FUENTE = pygame.font.Font("Kavoon-Regular.ttf", 18)

nombre_jugador = ""
variables_estado_jugando_validación = {
    "pregunta_actual": None,
    "respuesta": None,
    "tiempo_restante": 15,
    "temporizador_activado": False,
    "sin_tiempo": False,
    "movimiento_procesado": False,
    "avanzar": False,
    "extra": 0,
}
TABLERO = [0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0]
posición_actual = 15
EVENTO_TEMPORIZADOR = pygame.USEREVENT + 1
EVENTOS_SONIDOS = {
    "SONIDO_ESCALERA": pygame.USEREVENT + 2,
    "SONIDO_SERPIENTE": pygame.USEREVENT + 3,
}
puntuación_guardada = False

while correr:
    eventos = pygame.event.get()
    correr = not detectar_abandono(eventos, estado_juego)

    if estado_juego == "inicio":
        estado_juego = manejar_estado_inicio(eventos, pantalla, estado_juego)
    elif estado_juego == "nombre":
        estado_juego, nombre_jugador = manejar_estado_nombre(eventos, pantalla, FUENTE, estado_juego, nombre_jugador)
    elif estado_juego == "color":
        estado_juego, color_jugador = manejar_estado_color(eventos, pantalla, estado_juego)
    elif estado_juego == "jugando":
        estado_juego, variables_estado_jugando_validación = manejar_estado_jugando(eventos, pantalla, estado_juego, FUENTE, color_jugador, posición_actual, variables_estado_jugando_validación, EVENTO_TEMPORIZADOR)
    elif estado_juego == "validación":
        estado_juego, resolución, posición_actual = manejar_estado_validación(eventos, pantalla, estado_juego, FUENTE, TABLERO, posición_actual, variables_estado_jugando_validación, EVENTOS_SONIDOS)
    elif estado_juego == "victoria" or estado_juego == "derrota" or estado_juego == "sin preguntas":
        estado_juego, resolución = manejar_estados_resoluciones(eventos, pantalla, estado_juego)
    elif estado_juego == "fin del juego":
        estado_juego, puntuación_guardada = manejar_estado_final(eventos, pantalla, estado_juego, resolución, nombre_jugador, posición_actual, puntuación_guardada)
    elif estado_juego == "puntuación" or estado_juego == "ver puntuación":
        estado_juego = manejar_estados_puntuación(eventos, pantalla, estado_juego, resolución, FUENTE)
    pygame.display.flip()
pygame.quit()