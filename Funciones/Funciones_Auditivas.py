import pygame.mixer as mixer
import random

mixer.init()

def reproducir_música(estado_de_juego: str, duración: int = -1):
    """
    Reproduce la música correspondiente al estado del juego.

    Parámetros:
        estado_de_juego (str): El estado actual del juego.
        duración (int): Duración de la música en milisegundos. Por defecto es -1 (bucle).
    """
    músicas = {
        "inicio": "./Música/Ancient Sadness.mp3",
        "nombre": "./Música/Astrologer.mp3",
        "victoria": "./Música/Grim.mp3",
        "derrota": "./Música/Master Alarich Theme.mp3",
        "sin preguntas": "./Música/Tavern Theme.mp3",
        "atrapado": "./Música/Disturbing.mp3"
    }
    if not mixer.music.get_busy():
        for estado, canción in músicas.items():
            if estado == estado_de_juego:
                mixer.music.load(canción)
                mixer.music.play(duración)

def detener_música():
    """
    Detiene la música que se está reproduciendo.

    Parámetros:
        Ninguno
    """
    mixer.music.stop()

def reproducir_sonido(sonido: str):
    """
    Reproduce un efecto de sonido según el nombre indicado.

    Parámetros:
        sonido (str): Nombre del sonido a reproducir.
    """
    sonidos = {
        "click": "./Sonidos/Click.mp3",
        "escalera": "./Sonidos/Escalera.mp3",
        "serpiente": "./Sonidos/Serpiente.mp3",
        "temporizador": "./Sonidos/Temporizador.mp3"
    }
    for nombre_sonido, ruta_sonido in sonidos.items():
        if nombre_sonido == sonido:
            efecto = mixer.Sound(ruta_sonido)
            efecto.set_volume(0.4)
            efecto.play()

def reproducir_sonido_aleatorio():
    """
    Reproduce un sonido aleatorio de teclas.

    Parámetros:
        Ninguno
    """
    sonidos = ["./Sonidos/Tecla1.mp3", "./Sonidos/Tecla2.mp3", "./Sonidos/Tecla3.mp3", "./Sonidos/Tecla4.mp3"]
    número_aleatorio = random.randint(0, 3)
    sonido_aleatorio = sonidos[número_aleatorio]
    efecto = mixer.Sound(sonido_aleatorio)
    efecto.set_volume(0.4)
    efecto.play()