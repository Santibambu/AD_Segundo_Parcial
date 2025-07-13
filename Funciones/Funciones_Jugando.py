import pygame
import random
from Preguntas import *
from Funciones.Funciones_Validación import *

def generar_pregunta_aleatoria(preguntas: list) -> dict | None:
    """
    Selecciona y elimina una pregunta aleatoria de la lista.

    Parámetros:
        preguntas (list): Lista de preguntas disponibles.

    Devuelve:
        dict: Pregunta seleccionada.
        None: Si no hay preguntas disponibles.
    """
    if preguntas:
        pregunta_aleatoria = preguntas[random.randint(0, len(preguntas) - 1)]
        preguntas.remove(pregunta_aleatoria)
        pregunta = pregunta_aleatoria
    else:
        pregunta = None
    return pregunta

def manejar_pregunta(estado_juego: str, variables: dict, evento_temporizador) -> tuple[str, dict]:
    """
    Maneja la lógica para obtener y preparar la pregunta actual del juego.

    Parámetros:
        estado_juego (str): Estado actual del juego.
        variables (dict): Diccionario con el estado interno del juego.

    Devuelve:
        tuple[str, dict]: Nuevo estado del juego y el diccionario actualizado de variables del estado.
    """
    if variables["pregunta_actual"] is None:
        variables["pregunta_actual"] = generar_pregunta_aleatoria(preguntas)
        if not variables["pregunta_actual"]:
            estado_juego = "sin preguntas"
            detener_música()
        else:
            variables["tiempo_restante"] = 15
            pygame.time.set_timer(evento_temporizador, 1000)
            variables["temporizador_activado"] = True
    return (estado_juego, variables)

def manejar_click_respuesta(evento: pygame.event.Event, variables: dict) -> tuple[str, bool]:
    """
    Procesa el clic del usuario sobre una respuesta y actualiza el estado.

    Parámetros:
        evento (pygame.event.Event): Evento de clic del usuario.
        variables (dict): Diccionario con el estado interno del juego.

    Devuelve:
        tuple[str, bool]: Nuevo estado del juego y si se seleccionó una respuesta.
    """
    respuesta_seleccionada = False
    for botón, letra in zip(list(COORDENADAS_PREGUNTA.values())[1:], ["a", "b", "c"]):
        if botón.collidepoint(evento.pos):
            reproducir_sonido("click")
            variables["respuesta"] = letra
            variables["temporizador_activado"] = False
            respuesta_seleccionada = True
    return ("validación", respuesta_seleccionada)

def actualizar_temporizador(variables: dict) -> tuple[str, dict]:
    """
    Actualiza el temporizador, reproduce sonidos y determina si se cambia de estado.

    Parámetros:
        variables (dict): Diccionario con el estado interno del juego.

    Devuelve:
        tuple[str, dict]: Nuevo estado del juego y el diccionario actualizado de variables del estado.
    """
    estado_juego = "jugando"
    variables["tiempo_restante"] -= 1
    if variables["tiempo_restante"] <= 0:
        variables["respuesta"] = False
        variables["temporizador_activado"] = False
        variables["sin_tiempo"] = True
        estado_juego = "validación"
    elif variables["tiempo_restante"] == 3:
        reproducir_sonido("temporizador")
    return (estado_juego, variables)