import pygame
import pygame.mixer as mixer
from Funciones import *
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
color_jugador = None
TABLERO = [0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0]
posición_actual = 15
pregunta_actual = None
respuesta = None
movimiento_procesado = False
resolución = ""
puntuación_guardada = False

tiempo_restante = 15
temporizador_activado = False
evento_tiempo = pygame.USEREVENT + 1
sin_tiempo = False
sonido_escalera = pygame.USEREVENT + 2
sonido_serpiente = pygame.USEREVENT + 3
sonido_procesado = False

while correr:
    if estado_juego == "inicio":
        pantalla.blit(título, (0, 0))
        reproducir_música(estado_juego)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if BOTÓN_JUGAR.collidepoint(evento.pos):
                    reproducir_sonido("click")
                    estado_juego = "nombre"
                    detener_música()
                elif BOTÓN_SALIR.collidepoint(evento.pos):
                    correr = False
                elif BOTÓN_VER_PUNTUACIONES.collidepoint(evento.pos):
                    reproducir_sonido("click")
                    estado_juego = "ver puntuación"
    elif estado_juego == "nombre":
        pantalla.blit(nombre, (0, 0))
        reproducir_música(estado_juego)

        caracteres_máximos = 29
        nombre_mostrado = nombre_jugador[:caracteres_máximos]

        texto_ingresado = fuente.render(nombre_mostrado, True, BLANCO)
        texto_rectángulo = texto_ingresado.get_rect(center=(pantalla.get_width() // 2, 490)) # Crea un rectángulo para el texto centrado horizontalmente en la pantalla
        pantalla.blit(texto_ingresado, texto_rectángulo)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
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
    elif estado_juego == "color":
        pantalla.blit(colores, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                botones_colores = {
                BOTÓN_NEGRO: NEGRO,
                BOTÓN_GRIS: GRIS,
                BOTÓN_BLANCO: BLANCO,
                BOTÓN_ROJO: ROJO,
                BOTÓN_VERDE: VERDE,
                BOTÓN_AZUL: AZUL,
                BOTÓN_NARANJA: NARANJA,
                BOTÓN_AMARILLO: AMARILLO,
                BOTÓN_CELESTE: CELESTE,
                BOTÓN_VIOLETA: VIOLETA,
                BOTÓN_ROSA: ROSA
                }

                for botón, color in botones_colores.items():
                    if verificar_click_círculo(evento.pos, botón):
                        reproducir_sonido("click")
                        color_jugador = color
                        estado_juego = "jugando"
                        break
    elif estado_juego == "jugando":
        pantalla.blit(fondo_tablero, (0, 0))
        pygame.draw.circle(pantalla, color_jugador, POSICIONES_TABLERO[posición_actual], 15)
        sin_tiempo = False
        movimiento_procesado = False
        
        if pregunta_actual is None:
            pregunta_actual = generar_pregunta_aleatoria(preguntas)
            if not pregunta_actual:
                estado_juego = "sin preguntas"
                detener_música()
                continue

            tiempo_restante = 15
            pygame.time.set_timer(evento_tiempo, 1000)
            temporizador_activado = True
        
        texto_temporizador = fuente.render(str(tiempo_restante), True, BLANCO)
        círculo_temporizador = texto_temporizador.get_rect(center=NÚMERO_TEMPORIZADOR.center)

        blitear_texto_centrado(pantalla, pregunta_actual["pregunta"], fuente, BLANCO, TEXTO_PREGUNTA)
        blitear_texto_centrado(pantalla, pregunta_actual["respuesta_a"], fuente, BLANCO, BOTÓN_OPCIÓN1)
        blitear_texto_centrado(pantalla, pregunta_actual["respuesta_b"], fuente, BLANCO, BOTÓN_OPCIÓN2)
        blitear_texto_centrado(pantalla, pregunta_actual["respuesta_c"], fuente, BLANCO, BOTÓN_OPCIÓN3)
        pantalla.blit(texto_temporizador, círculo_temporizador)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                botones_opciones = [
                (BOTÓN_OPCIÓN1, "a"),
                (BOTÓN_OPCIÓN2, "b"),
                (BOTÓN_OPCIÓN3, "c")
                ]

                for botón, letra in botones_opciones:
                    if botón.collidepoint(evento.pos):
                        reproducir_sonido("click")
                        respuesta = validar_respuesta(letra, pregunta_actual)
                        estado_juego = "validación"
                        temporizador_activado = False
                        pygame.time.set_timer(evento_tiempo, 0)
                        break
            if evento.type == evento_tiempo and temporizador_activado:
                tiempo_restante -= 1
                if tiempo_restante <= 0:
                    respuesta = False
                    sin_tiempo = True
                    estado_juego = "validación"
                    temporizador_activado = False
                    pygame.time.set_timer(evento_tiempo, 0)
                elif tiempo_restante == 3:
                    reproducir_sonido("temporizador")
    elif estado_juego == "validación":
        pantalla.blit(validación, (0, 0))
        pregunta_actual = None

        if not movimiento_procesado:
            avanzar, extra, posición_actual = realizar_movimiento(respuesta, TABLERO, posición_actual)

            if extra in [1, 2] and avanzar:
                pygame.event.post(pygame.event.Event(sonido_escalera))
            elif extra in [1, 2, 3] and not avanzar:
                pygame.event.post(pygame.event.Event(sonido_serpiente))

            nuevo_estado = verificar_posición(posición_actual)
            if nuevo_estado is not None:
                estado_juego = nuevo_estado
                detener_música()

            movimiento_procesado = True
            
        if not sin_tiempo:
            if avanzar:
                blitear_texto_centrado(pantalla, "Respondiste correctamente. Avanzás una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
                if extra == 1:
                    blitear_texto_centrado(pantalla, "¡Encontraste una escalera! La subís y avanzás 1 casilla hacia arriba.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
                elif extra == 2:
                    blitear_texto_centrado(pantalla, "¡Encontraste una escalera! La subís y avanzás 2 casillas hacia arriba.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
            else:
                blitear_texto_centrado(pantalla, "Respondiste incorrectamente. Retrocedés una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
                if extra == 1:
                    blitear_texto_centrado(pantalla, "¡Pisaste una serpiente! Te arrastró 1 casilla hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
                elif extra == 2:
                    blitear_texto_centrado(pantalla, "¡Pisaste una serpiente! Te arrastró 2 casillas hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
                elif extra == 3:
                    blitear_texto_centrado(pantalla, "¡Pisaste una serpiente! Te arrastró 3 casillas hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
        else:
            blitear_texto_centrado(pantalla, "Se te acabó el tiempo para responder. Retrocedés una casilla.", fuente, BLANCO, RESPUESTA_VALIDADA)
            if extra == 1:
                blitear_texto_centrado(pantalla, "¡Pisaste una serpiente! Te arrastró 1 casilla hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
            elif extra == 2:
                blitear_texto_centrado(pantalla, "¡Pisaste una serpiente! Te arrastró 2 casillas hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)
            elif extra == 3:
                blitear_texto_centrado(pantalla, "¡Pisaste una serpiente! Te arrastró 3 casillas hacia abajo.", fuente, BLANCO, MOVIMIENTOS_EXTRA)

        for evento in pygame.event.get():
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
    elif estado_juego in ("victoria", "derrota", "sin preguntas"):
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

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                reproducir_sonido("click")
                resolución = resoluciones[estado_juego]
                estado_juego = "fin del juego"
    elif estado_juego == "fin del juego":
        match resolución:
            case "victoria": pantalla.blit(resolución_victoria, (0, 0))
            case "derrota": pantalla.blit(resolución_derrota, (0, 0))
            case "atrapado": pantalla.blit(resolución_atrapado, (0, 0)); reproducir_música(resolución)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if BOTÓN_PUNTUACIÓN.collidepoint(evento.pos):
                    estado_juego = "puntuación"
                    reproducir_sonido("click")
                if BOTÓN_CERRAR.collidepoint(evento.pos):
                    correr = False
    elif estado_juego in ("puntuación", "ver puntuación"):
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

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                reproducir_sonido("click")
                if estado_juego == "ver puntuación":
                    if BOTÓN_VOLVER.collidepoint(evento.pos):
                        estado_juego = "inicio"
                else:
                    correr = False
    pygame.display.flip()
pygame.quit()