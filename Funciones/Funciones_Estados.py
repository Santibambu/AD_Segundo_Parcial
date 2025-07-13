import pygame
from Imágenes import *
from Coordenadas import *
from Preguntas import *
from Funciones.Funciones_Auditivas import *
from Funciones.Funciones_Generales import *
from Funciones.Funciones_Color import *
from Funciones.Funciones_Jugando import *
from Funciones.Funciones_Validación import *

def manejar_estado_inicio(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str) -> str:
    """
    Maneja la lógica y la interfaz del estado de inicio del juego.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        pantalla (pygame.surface.Surface): Superficie donde se dibuja la pantalla de inicio.
        estado_juego (str): Estado actual del juego.

    Devuelve:
        str: Nuevo estado del juego según la interacción del usuario.
    """
    pantalla.blit(título, (0, 0))
    reproducir_música("inicio")

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if BOTÓN_JUGAR.collidepoint(evento.pos):
                reproducir_sonido("click")
                detener_música()
                estado_juego = "nombre"
            elif BOTÓN_SALIR.collidepoint(evento.pos):
                estado_juego = "salir"
            elif BOTÓN_VER_PUNTUACIONES.collidepoint(evento.pos):
                reproducir_sonido("click")
                estado_juego = "ver puntuación"
    return estado_juego

def manejar_estado_nombre(eventos: list, pantalla: pygame.surface.Surface, fuente: pygame.font.Font, estado_juego: str, nombre_jugador: str) -> tuple[str, str]:
    """
    Maneja la lógica y la interfaz para ingresar el nombre del jugador.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        pantalla (pygame.surface.Surface): Superficie donde se dibuja la pantalla de nombre.
        fuente (pygame.font.Font): Fuente utilizada para mostrar el texto.
        estado_juego (str): Estado actual del juego.
        nombre_jugador (str): Nombre actual ingresado por el jugador.

    Devuelve:
        tuple[str, str]: Nuevo estado del juego y el nombre actualizado del jugador.
    """
    def blitear_nombre_ingresado() -> str:
        nombre_mostrado = nombre_jugador[:caracteres_máximos]
        texto_ingresado = fuente.render(nombre_mostrado, True, BLANCO)
        texto_rectángulo = texto_ingresado.get_rect(center=(pantalla.get_width() // 2, 490))
        pantalla.blit(texto_ingresado, texto_rectángulo)
        return nombre_mostrado
    
    pantalla.blit(nombre, (0, 0))
    reproducir_música("nombre")

    caracteres_máximos = 29
    nombre_mostrado = blitear_nombre_ingresado()

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            reproducir_sonido_aleatorio()
            if evento.key == pygame.K_RETURN:
                if not nombre_mostrado.strip() == "":
                    nombre_jugador = nombre_mostrado
                    estado_juego = "color"
            elif evento.key == pygame.K_BACKSPACE:
                nombre_jugador = nombre_jugador[:-1]
            else:
               if len(nombre_jugador) < caracteres_máximos:
                    nombre_jugador += evento.unicode
    return (estado_juego, nombre_jugador)

def manejar_estado_color(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str) -> tuple[str, tuple[int, int, int]]:
    """
    Maneja la lógica y la interfaz para seleccionar el color del jugador.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        pantalla (pygame.surface.Surface): Superficie donde se dibuja la pantalla de colores.
        estado_juego (str): Estado actual del juego.

    Devuelve:
        tuple[str, tuple[int, int, int]]: Nuevo estado del juego y el color seleccionado por el jugador.
    """
    
    pantalla.blit(colores, (0, 0))

    color_jugador = None

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            color = asignar_color_seleccionado(evento.pos)
            if color:
                reproducir_sonido("click")
                color_jugador = color
                estado_juego = "jugando"
    return (estado_juego, color_jugador)

def manejar_estado_jugando(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str, fuente: pygame.font.Font, color_jugador: tuple[int, int, int], posición_actual: int, sin_tiempo: bool, variables_estado_jugando: dict) -> str:
    pantalla.blit(fondo_tablero, (0, 0))
    pygame.draw.circle(pantalla, color_jugador, POSICIONES_TABLERO[posición_actual], 15)
    
    estado_juego, variables_estado_jugando = manejar_pregunta(estado_juego, variables_estado_jugando)

    for clave, posición in zip(variables_estado_jugando["pregunta_actual"].keys(), COORDENADAS_PREGUNTA.values()):
        blitear_texto_centrado(pantalla, variables_estado_jugando["pregunta_actual"][clave], fuente, BLANCO, posición)

    texto_temporizador = fuente.render(str(variables_estado_jugando["tiempo_restante"]), True, BLANCO)
    pantalla.blit(texto_temporizador, texto_temporizador.get_rect(center=NÚMERO_TEMPORIZADOR.center))

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            nuevo_estado, respuesta_seleccionada = manejar_click_respuesta(evento, variables_estado_jugando)
            if respuesta_seleccionada:
                estado_juego = nuevo_estado
        if evento.type == pygame.USEREVENT + 1 and variables_estado_jugando["temporizador_activado"]:
            variables_estado_jugando["tiempo_restante"] -= 1
            if variables_estado_jugando["tiempo_restante"] <= 0:
                variables_estado_jugando["respuesta"] = False
                sin_tiempo = True
                estado_juego = "validación"
                variables_estado_jugando["temporizador_activado"] = False
            elif variables_estado_jugando["tiempo_restante"] == 3:
                reproducir_sonido("temporizador")
    return (estado_juego, variables_estado_jugando["respuesta"], sin_tiempo)