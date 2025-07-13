import pygame
import pygame.mixer as mixer
from Funciones.Funciones_Auditivas import *
from Funciones.Funciones_Generales import *
from Funciones.Funciones_Estados import *
from Funciones.Funciones_Validación import *
from Funciones.Funciones_Archivos import *
from Imágenes import *
from Coordenadas import *
from Colores import *

pygame.init()
mixer.init()
DIMENSIÓN_PANTALLA = ((600, 620))
pantalla = pygame.display.set_mode(DIMENSIÓN_PANTALLA)
pygame.display.set_caption("Serpientes y Escaleras")
pygame.display.set_icon(ícono)

correr = True
estado_juego = "inicio"
fuente = pygame.font.Font("Kavoon-Regular.ttf", 18)

nombre_jugador = ""
variables_estado_jugando = {
    "pregunta_actual": None,
    "respuesta": None,
    "tiempo_restante": 15,
    "temporizador_activado": False,
}
sin_tiempo = False
TABLERO = [0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0]
posición_actual = 15
movimiento_procesado = False
resolución = ""
puntuación_guardada = False

sonido_escalera = pygame.USEREVENT + 2
sonido_serpiente = pygame.USEREVENT + 3
sonido_procesado = False

while correr:
    eventos = pygame.event.get()
    correr = not detectar_abandono(eventos, estado_juego)

    if estado_juego == "inicio":
        estado_juego = manejar_estado_inicio(eventos, pantalla, estado_juego)
    elif estado_juego == "nombre":
        estado_juego, nombre_jugador = manejar_estado_nombre(eventos, pantalla, fuente, estado_juego, nombre_jugador)
    elif estado_juego == "color":
        estado_juego, color_jugador = manejar_estado_color(eventos, pantalla, estado_juego)
    elif estado_juego == "jugando":
        estado_juego, respuesta, sin_tiempo = manejar_estado_jugando(eventos, pantalla, estado_juego, fuente, color_jugador, posición_actual, sin_tiempo, variables_estado_jugando)
    elif estado_juego == "validación":
        pantalla.blit(validación, (0, 0))
        pregunta_actual = None

        if not movimiento_procesado:
            avanzar, extra, posición_actual = realizar_movimiento(respuesta, TABLERO, posición_actual)

            if (extra == 1 or extra == 2) and avanzar:
                pygame.event.post(pygame.event.Event(sonido_escalera))
            elif (extra == 1 or extra == 2 or extra == 3) and not avanzar:
                pygame.event.post(pygame.event.Event(sonido_serpiente))

            nuevo_estado = verificar_posición(posición_actual)
            if nuevo_estado is not None:
                estado_juego = nuevo_estado
                detener_música()

            movimiento_procesado = True
            
        if not sin_tiempo:
            if avanzar:
                blitear_texto_centrado(pantalla, "Respondiste correctamente. Avanzás una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
                if extra != 0:
                    blitear_texto_centrado(pantalla, f"¡Encontraste una escalera! La subís y avanzás {extra} casilla/s hacia arriba.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
            else:
                blitear_texto_centrado(pantalla, "Respondiste incorrectamente. Retrocedés una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
                if extra != 0:
                    blitear_texto_centrado(pantalla, f"¡Pisaste una serpiente! Te arrastró {extra} casilla/s hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
        else:
            blitear_texto_centrado(pantalla, "Se te acabó el tiempo para responder. Retrocedés una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
            if extra != 0:
                blitear_texto_centrado(pantalla, f"¡Pisaste una serpiente! Te arrastró {extra} casilla/s hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)

        for evento in eventos:
                if evento.type == pygame.QUIT:
                    correr = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if BOTÓN_CONTINUAR.collidepoint(evento.pos):
                        reproducir_sonido("click")
                        estado_juego = "jugando"
                    if BOTÓN_ABANDONAR.collidepoint(evento.pos):
                        reproducir_sonido("click")
                        estado_juego = "fin del juego"
                        resolución = "atrapado"
                        detener_música()
                if evento.type == sonido_escalera:
                    reproducir_sonido("escalera")
                if evento.type == sonido_serpiente:
                    reproducir_sonido("serpiente")
    elif estado_juego == "victoria" or estado_juego == "derrota" or estado_juego == "sin preguntas":
        fondos = {
            "victoria": victoria,
            "derrota": derrota,
            "sin preguntas": sin_preguntas
        }

        resoluciones = {
            "victoria": "victoria",
            "derrota": "derrota",
            "sin preguntas": "atrapado"
        }

        pantalla.blit(fondos[estado_juego], (0, 0))
        reproducir_música(estado_juego)

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                reproducir_sonido("click")
                resolución = resoluciones[estado_juego]
                estado_juego = "fin del juego"
    elif estado_juego == "fin del juego":
        fondos = {
            "victoria": resolución_victoria,
            "derrota": resolución_derrota,
            "atrapado": resolución_atrapado
        }
        if resolución == "atrapado":
            reproducir_música("atrapado")
        pantalla.blit(fondos[resolución], (0, 0))

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if BOTÓN_PUNTUACIÓN.collidepoint(evento.pos):
                    estado_juego = "puntuación"
                    reproducir_sonido("click")
                if BOTÓN_CERRAR.collidepoint(evento.pos):
                    correr = False
    elif estado_juego == "puntuación" or estado_juego == "ver puntuación":
        fondos_puntuación = {
            "victoria": puntuación_victoria,
            "derrota": puntuación_derrota,
            "atrapado": puntuación_atrapado
        }

        if estado_juego == "puntuación":
            pantalla.blit(fondos_puntuación[resolución], (0, 0))

            if not puntuación_guardada:
                crear_tablero_puntuación(nombre_jugador, posición_actual)
                puntuación_guardada = True
        else:
            pantalla.blit(ver_puntuación, (0, 0))

        datos = ordenar_csv("Puntuación.csv")
        max_filas = 5
        for (nombre_puntuación, casillas), rect_nombre, rect_casilla in zip(datos[:max_filas], COLUMNA_NOMBRE, COLUMNA_CASILLAS):
            blitear_texto_centrado(pantalla, nombre_puntuación, fuente, BLANCO, rect_nombre)
            blitear_texto_centrado(pantalla, casillas, fuente, BLANCO, rect_casilla)

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                reproducir_sonido("click")
                if estado_juego == "ver puntuación":
                    if BOTÓN_VOLVER.collidepoint(evento.pos):
                        estado_juego = "inicio"
                else:
                    correr = False
    pygame.display.flip()
pygame.quit()

"""
CAMBIOS A EFECTUAR
4) Modularizar cada bloque de código de cada estado de juego en una función dedicada. En el archivo principal solo debe quedar el bucle correr y los ifs de los estados
"""