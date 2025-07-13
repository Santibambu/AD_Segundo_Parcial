import pygame
from Colores import *
from Coordenadas import *
from Funciones.Funciones_Auditivas import *
from Funciones.Funciones_Generales import *

def validar_respuesta(variables: dict) -> bool:
    """
    Valida si la respuesta seleccionada es correcta, usando el diccionario de estado.

    Parámetros:
        variables (dict): Diccionario que contiene la respuesta seleccionada y la pregunta actual.

    Devuelve:
        bool: True si la respuesta es correcta, False en caso contrario.
    """
    return variables["respuesta"] == variables["pregunta_actual"]["respuesta_correcta"]

def realizar_movimiento(avanzar: bool, tablero: list, posición: int) -> tuple[int, int]:
    """
    Calcula el nuevo movimiento del jugador en el tablero.

    Parámetros:
        avanzar (bool): Indica si el jugador avanza o retrocede.
        tablero (list): Lista que representa el tablero.
        posición (int): Posición actual del jugador.

    Devuelve:
        tuple[int, int]: (extra, posición) con el resultado del movimiento.
    """
    extra = 0
    if avanzar == True:
        posición += 1
        extra += tablero[posición]
        posición += extra
    else:
        posición -= 1
        extra += tablero[posición]
        posición -= extra
    return (extra, posición)

def verificar_posición(posición: int) -> str | None:
    """
    Verifica si la posición del jugador corresponde a victoria, derrota o continúa.

    Parámetros:
        posición (int): Posición actual del jugador.

    Devuelve:
        str: "victoria" o "derrota" si corresponde, None en caso contrario.
    """
    nuevo_estado = None
    if posición + 1 == 30:
        nuevo_estado = "victoria"
    elif posición == 0:
        nuevo_estado = "derrota"
    return nuevo_estado

def publicar_evento(variables: dict, EVENTOS_SONIDOS: dict):
    """
    Publica un evento de sonido según el tipo de movimiento realizado.

    Parámetros:
        variables (dict): Diccionario con el estado del movimiento (extra, avanzar)
        EVENTOS_SONIDOS (dict): Diccionario con los identificadores de eventos de sonido.
    """
    if variables["extra"] != 0:
        tipo_evento = "SONIDO_ESCALERA" if variables["avanzar"] else "SONIDO_SERPIENTE"
        pygame.event.post(pygame.event.Event(EVENTOS_SONIDOS[tipo_evento]))

def mostrar_mensaje_movimiento(pantalla: pygame.surface.Surface, fuente: pygame.font.Font, variables: dict):
    """
    Muestra el mensaje correspondiente al movimiento realizado por el jugador.

    Parámetros:
        pantalla (pygame.surface.Surface): Superficie donde se dibuja el mensaje.
        fuente (pygame.font.Font): Fuente utilizada para mostrar el texto.
        variables (dict): Diccionario con el estado del movimiento (avanzar, extra, sin_tiempo).
    """
    if not variables["sin_tiempo"]:
        if variables["avanzar"]:
            blitear_texto_centrado(pantalla, "Respondiste correctamente. Avanzás una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
            if variables["extra"] != 0:
                blitear_texto_centrado(pantalla, f"¡Encontraste una escalera! La subís y avanzás {variables['extra']} casilla/s hacia arriba.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
        else:
            blitear_texto_centrado(pantalla, "Respondiste incorrectamente. Retrocedés una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
            if variables["extra"] != 0:
                blitear_texto_centrado(pantalla, f"¡Pisaste una serpiente! Te arrastró {variables['extra']} casilla/s hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
    else:
        blitear_texto_centrado(pantalla, "Se te acabó el tiempo para responder. Retrocedés una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
        if variables["extra"] != 0:
            blitear_texto_centrado(pantalla, f"¡Pisaste una serpiente! Te arrastró {variables['extra']} casilla/s hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)