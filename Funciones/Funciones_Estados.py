import pygame
from Imágenes import *
from Funciones.Funciones_Auditivas import *
from Funciones.Funciones_Generales import *
from Funciones.Funciones_Color import *
from Funciones.Funciones_Jugando import *
from Funciones.Funciones_Validación import *
from Funciones.Funciones_Archivos import *

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

def manejar_estado_jugando(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str, fuente: pygame.font.Font, color_jugador: tuple[int, int, int], posición_actual: int, variables: dict, evento_temporizador) -> tuple[str, dict]:
    """
    Maneja la lógica y la interfaz del estado de juego activo.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        pantalla (pygame.surface.Surface): Superficie donde se dibuja la ficha del jugador.
        estado_juego (str): Estado actual del juego.
        fuente (pygame.font.Font): Fuente utilizada para mostrar el texto.
        color_jugador (tuple[int, int, int]): Color del jugador en formato RGB.
        posición_actual (int): Posición actual del jugador en el tablero.
        variables (dict): Diccionario con el estado interno del juego.

    Devuelve:
        tuple[str, dict]: Nuevo estado del juego y el diccionario actualizado de variables del estado.
    """
    pantalla.blit(fondo_tablero, (0, 0))
    pygame.draw.circle(pantalla, color_jugador, POSICIONES_TABLERO[posición_actual], 15)
    
    estado_juego, variables = manejar_pregunta(estado_juego, variables, evento_temporizador)
    
    continuar_programa = estado_juego != "sin preguntas"

    if continuar_programa and variables["pregunta_actual"]:
        for clave, posición in zip(variables["pregunta_actual"].keys(), COORDENADAS_PREGUNTA.values()):
            blitear_texto_centrado(pantalla, variables["pregunta_actual"][clave], fuente, BLANCO, posición)
    texto_temporizador = fuente.render(str(variables["tiempo_restante"]), True, BLANCO)
    pantalla.blit(texto_temporizador, texto_temporizador.get_rect(center=NÚMERO_TEMPORIZADOR.center))

    if continuar_programa:
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                nuevo_estado, respuesta_seleccionada = manejar_click_respuesta(evento, variables)
                if respuesta_seleccionada:
                    estado_juego = nuevo_estado
            if evento.type == evento_temporizador and variables["temporizador_activado"]:
                estado_juego, variables = actualizar_temporizador(variables)
    return (estado_juego, variables)

def manejar_estado_validación(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str, fuente: pygame.font.Font, TABLERO: list, posición_actual: int, variables: dict, EVENTOS_SONIDOS: dict) -> tuple[str, str, int]:
    """
    Maneja la lógica y la interfaz del estado de validación de respuesta.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        pantalla (pygame.surface.Surface): Superficie donde se dibuja la pantalla de validación.
        estado_juego (str): Estado actual del juego.
        fuente (pygame.font.Font): Fuente utilizada para mostrar el texto.
        TABLERO (list): Lista que representa el tablero de juego.
        posición_actual (int): Posición actual del jugador en el tablero.
        variables (dict): Diccionario con el estado interno del juego.
        EVENTOS_SONIDOS (dict): Diccionario con los identificadores de eventos de sonido.

    Devuelve:
        tuple[str, str, int]: Nuevo estado del juego, resolución y posición actual del jugador.
    """
    pantalla.blit(validación, (0, 0))

    resolución = None

    if not variables["movimiento_procesado"]:
        variables["avanzar"] = validar_respuesta(variables)
        variables["extra"], posición_actual = realizar_movimiento(variables["avanzar"], TABLERO, posición_actual)
        publicar_evento(variables, EVENTOS_SONIDOS)
        nuevo_estado = verificar_posición(posición_actual)
        if nuevo_estado:
            estado_juego = nuevo_estado
            detener_música()
        variables["movimiento_procesado"] = True

    mostrar_mensaje_movimiento(pantalla, fuente, variables)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if BOTÓN_CONTINUAR.collidepoint(evento.pos):
                reproducir_sonido("click")
                estado_juego = "jugando"
                variables["pregunta_actual"] = None
                variables["respuesta"] = None
                variables["sin_tiempo"] = False
                variables["movimiento_procesado"] = False
                variables["avanzar"] = False
                variables["extra"] = 0
            if BOTÓN_ABANDONAR.collidepoint(evento.pos):
                reproducir_sonido("click")
                estado_juego = "fin del juego"
                resolución = "atrapado"
                detener_música()
        if evento.type == EVENTOS_SONIDOS["SONIDO_ESCALERA"]:
            reproducir_sonido("escalera")
        if evento.type == EVENTOS_SONIDOS["SONIDO_SERPIENTE"]:
            reproducir_sonido("serpiente")
    return (estado_juego, resolución, posición_actual)

def manejar_estados_resoluciones(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str) -> tuple[str, str]:
    """
    Muestra la pantalla de resolución (victoria, derrota o atrapado) y gestiona la transición de estado.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        pantalla (pygame.surface.Surface): Superficie donde se dibuja la pantalla de resolución.
        estado_juego (str): Estado actual del juego.

    Devuelve:
        tuple[str, str]: Nuevo estado del juego y la resolución alcanzada.
    """
    fondos = {
        "victoria": victoria,
        "derrota": derrota,
        "sin preguntas": sin_preguntas,
    }

    resoluciones = {
        "victoria": "victoria",
        "derrota": "derrota",
        "sin preguntas": "atrapado",
    }

    pantalla.blit(fondos[estado_juego], (0, 0))
    reproducir_música(estado_juego)

    resolución = None
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            reproducir_sonido("click")
            resolución = resoluciones[estado_juego]
            estado_juego = "fin del juego"
    return (estado_juego, resolución)

def manejar_estado_final(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str, resolución: str) -> str:
    """
    Muestra la pantalla final según la resolución y gestiona la transición de estado.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        pantalla (pygame.surface.Surface): Superficie donde se dibuja la pantalla final.
        estado_juego (str): Estado actual del juego.
        resolución (str): Resolución alcanzada ("victoria", "derrota" o "atrapado").

    Devuelve:
        str: Nuevo estado del juego.
    """
    fondos = {
        "victoria": resolución_victoria,
        "derrota": resolución_derrota,
        "atrapado": resolución_atrapado,
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
                estado_juego = "salir"
    return estado_juego

def manejar_estados_puntuación(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str, resolución: str, nombre_jugador: str, posición_actual: int, fuente: pygame.font.Font, puntuación_guardada: bool) -> tuple[str, bool]:
    """
    Muestra la pantalla de puntuaciones y gestiona la transición de estado y el guardado de la puntuación.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        pantalla (pygame.surface.Surface): Superficie donde se dibuja la pantalla de puntuaciones.
        estado_juego (str): Estado actual del juego.
        resolución (str): Resolución alcanzada ("victoria", "derrota" o "atrapado").
        nombre_jugador (str): Nombre del jugador.
        posición_actual (int): Posición alcanzada por el jugador.
        fuente (pygame.font.Font): Fuente utilizada para mostrar el texto.
        puntuación_guardada (bool): Indica si la puntuación ya fue guardada.

    Devuelve:
        tuple[str, bool]: Nuevo estado del juego y si la puntuación fue guardada.
    """
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
                estado_juego = "salir"
    return (estado_juego, puntuación_guardada)