import pygame
import random
from Preguntas import *
from Coordenadas import *
from Funciones.Funciones_Auditivas import *
from Funciones.Funciones_Validación import *

def generar_pregunta_aleatoria(preguntas: list) -> dict | bool:
        """
        Selecciona y elimina una pregunta aleatoria de la lista.

        Parámetros:
            preguntas (list): Lista de preguntas disponibles.

        Devuelve:
            dict: Pregunta seleccionada.
            bool: False si no hay preguntas disponibles.
        """
        if preguntas:
            pregunta_aleatoria = preguntas[random.randint(0, len(preguntas) - 1)]
            preguntas.remove(pregunta_aleatoria)
            resultado = pregunta_aleatoria
        else:
            resultado = False
        return resultado

def manejar_pregunta(estado_juego: str, variables_estado_jugando: dict) -> str:
    if variables_estado_jugando["pregunta_actual"] is None:
        variables_estado_jugando["pregunta_actual"] = generar_pregunta_aleatoria(preguntas)
        if not variables_estado_jugando["pregunta_actual"]:
            estado_juego = "sin preguntas"
            detener_música()
        else:
            variables_estado_jugando["tiempo_restante"] = 15
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
            variables_estado_jugando["temporizador_activado"] = True
    return (estado_juego, variables_estado_jugando)

def manejar_click_respuesta(evento: pygame.event.Event, variables_estado_jugando: dict) -> tuple[str, bool]:
    respuesta_seleccionada = False
    for botón, letra in zip(list(COORDENADAS_PREGUNTA.values())[1:], ["a", "b", "c"]):
        if botón.collidepoint(evento.pos):
            reproducir_sonido("click")
            variables_estado_jugando["respuesta"] = validar_respuesta(letra, variables_estado_jugando["pregunta_actual"])
            variables_estado_jugando["temporizador_activado"] = False
            respuesta_seleccionada = True
    return ("validación", respuesta_seleccionada)