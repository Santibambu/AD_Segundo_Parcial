import pygame
from Imágenes import *
from Coordenadas import *
from Colores import *
from Funciones.Funciones_Auditivas import *

def detectar_evento_salir(eventos: list) -> bool:
    resultado = False
    for evento in eventos:
        if evento.type == pygame.QUIT:
            resultado = True
    return resultado

def manejar_estado_inicio(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str) -> str:
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

def manejar_estado_nombre(eventos: list, pantalla: pygame.surface.Surface, estado_juego: str, fuente: pygame.font.Font, nombre_jugador: str) -> tuple[str, str]:
    pantalla.blit(nombre, (0, 0))
    reproducir_música(estado_juego)
    
    caracteres_máximos = 29
    nombre_mostrado = nombre_jugador[:caracteres_máximos]

    texto_ingresado = fuente.render(nombre_mostrado, True, BLANCO)
    texto_rectángulo = texto_ingresado.get_rect(center=(pantalla.get_width() // 2, 490)) # Crea un rectángulo para el texto centrado horizontalmente en la pantalla
    pantalla.blit(texto_ingresado, texto_rectángulo)
    
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
    return estado_juego, nombre_jugador