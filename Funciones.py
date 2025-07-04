from Preguntas import *
import random
import pygame
import pygame.mixer as mixer
mixer.init()

def reproducir_música(estado_de_juego: str, duración: int = -1):
    """
    Reproduce la música correspondiente al estado del juego.

    Parámetros:
        estado_de_juego (str): El estado actual del juego.
        duración (int): Duración de la música en milisegundos. Por defecto es -1 (bucle).
    """
    if not mixer.music.get_busy():
        match estado_de_juego:
            case "inicio": mixer.music.load("./Música/Ancient Sadness.mp3"); mixer.music.play(duración)
            case "nombre": mixer.music.load("./Música/Astrologer.mp3"); mixer.music.play(duración)
            case "victoria": mixer.music.load("./Música/Grim.mp3"); mixer.music.play(duración)
            case "derrota": mixer.music.load("./Música/Master Alarich Theme.mp3"); mixer.music.play(duración)
            case "sin preguntas": mixer.music.load("./Música/Tavern Theme.mp3"); mixer.music.play(duración)
            case "atrapado": mixer.music.load("./Música/Disturbing.mp3"); mixer.music.play(duración)

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
    match sonido:
        case "click": efecto = mixer.Sound("./Sonidos/Click.mp3"); efecto.set_volume(0.4); efecto.play()
        case "escalera": efecto = mixer.Sound("./Sonidos/Escalera.mp3"); efecto.set_volume(0.4); efecto.play()
        case "serpiente": efecto = mixer.Sound("./Sonidos/Serpiente.mp3"); efecto.set_volume(0.4); efecto.play()
        case "temporizador": efecto = mixer.Sound("./Sonidos/Temporizador.mp3"); efecto.set_volume(0.4); efecto.play()

def reproducir_sonido_aleatorio():
    """
    Reproduce un sonido aleatorio de teclas.

    Parámetros:
        Ninguno
    """
    número_aleatorio = random.randint(1, 4)
    match número_aleatorio:
        case 1: efecto = mixer.Sound("./Sonidos/Tecla1.mp3"); efecto.set_volume(0.4); efecto.play()
        case 2: efecto = mixer.Sound("./Sonidos/Tecla2.mp3"); efecto.set_volume(0.4); efecto.play()
        case 3: efecto = mixer.Sound("./Sonidos/Tecla3.mp3"); efecto.set_volume(0.4); efecto.play()
        case 4: efecto = mixer.Sound("./Sonidos/Tecla4.mp3"); efecto.set_volume(0.4); efecto.play()

def verificar_click_círculo(coordenadas: tuple, círculo: tuple) -> bool:
    """
    Verifica si un punto está dentro de un círculo.

    Parámetros:
        coordenadas (tuple): Coordenadas (x, y) del punto a verificar.
        círculo (tuple): Tupla (centro_x, centro_y, radio) del círculo.

    Devuelve:
        bool: True si el punto está dentro del círculo, False en caso contrario.
    """
    x, y = coordenadas
    centro_x, centro_y, radio = círculo
    return (x - centro_x) ** 2 + (y - centro_y) ** 2 <= radio ** 2 # Teorema de pitágoras ((x−h)^2 + (y−k)^2 ≤ r^2))

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

def blitear_texto_centrado(pantalla, texto: str, fuente: pygame.font.Font, color: tuple, espacio: pygame.Rect):
    """
    Dibuja texto multilínea centrado en un área específica de la pantalla.

    Parámetros:
        pantalla: Superficie de pygame donde se dibuja el texto.
        texto (str): Texto a mostrar.
        fuente (pygame.font.Font): Fuente del texto.
        color (tuple): Color del texto.
        espacio (pygame.Rect): Área donde centrar el texto.
    """
    palabras = texto.split(" ")
    líneas = []
    línea_actual = ""
    
    for palabra in palabras:
        línea_aux = línea_actual + palabra + " "
        if fuente.size(línea_aux)[0] <= espacio.width: # Si la línea no sobrepasa el espacio...
            línea_actual = línea_aux
        else:
            líneas.append(línea_actual)
            línea_actual = palabra + " " # Si la línea sobrepasa el espacio, se guarda lo que se tiene y se empieza a construir una nueva línea
    líneas.append(línea_actual) # Se crea la lista con todas las palabras (el texto)

    altura_total = len(líneas) * (fuente.get_height() + 5) - 5 # Multiplica la cantidad de líneas por la cantidad de pixeles que se usan para esa fuente y una separación de 5 pixeles extra entre cada línea, luego resta 5 pixeles de la última línea, que no debería tener separación
    eje_vertical_inicial = espacio.centery - altura_total // 2 + 10 # Resta el centro vertical del espacio donde se va a dibujar el texto con la mitad de la altura total que ocupa dicho texto, y luego suma un márgen de espaciado de 10 pixeles

    for i, línea in enumerate(líneas):
        render_pantalla = fuente.render(línea, True, color)
        espacio_texto = render_pantalla.get_rect(center=(espacio.centerx, eje_vertical_inicial + i * (fuente.get_height() + 5))) # Crea un espacio para cada línea individual, ubicando cada línea centrada horizontal y verticalmente, una debajo de la otra, con separación de 5 pixeles
        pantalla.blit(render_pantalla, espacio_texto)

def validar_respuesta(respuesta: str, pregunta: dict) -> bool:
    """
    Valida si la respuesta dada es correcta.

    Parámetros:
        respuesta (str): Respuesta seleccionada por el usuario.
        pregunta (dict): Pregunta con la respuesta correcta.

    Devuelve:
        bool: True si la respuesta es correcta, False en caso contrario.
    """
    return respuesta == pregunta["respuesta_correcta"]

def realizar_movimiento(avanzar: bool, tablero: list, posición: int):
    """
    Calcula el nuevo movimiento del jugador en el tablero.

    Parámetros:
        avanzar (bool): Indica si el jugador avanza o retrocede.
        tablero (list): Lista que representa el tablero.
        posición (int): Posición actual del jugador.

    Devuelve:
        tuple: (avanzar, extra, posición) con el resultado del movimiento.
    """
    extra = None

    if avanzar == True:
        posición += 1
        if tablero[posición] != 0:
            match tablero[posición]:
                case 1: posición += 1; extra = 1
                case 2: posición += 2; extra = 2
    else:
        posición -= 1
        if tablero[posición] != 0:
            match tablero[posición]:
                case 1: posición -= 1; extra = 1
                case 2: posición -= 2; extra = 2
                case 3: posición -= 3; extra = 3
    return avanzar, extra, posición

def verificar_posición(posición: int) -> str | None:
    """
    Verifica si la posición del jugador corresponde a victoria, derrota o continúa.

    Parámetros:
        posición (int): Posición actual del jugador.

    Devuelve:
        str: "victoria" o "derrota" si corresponde, None en caso contrario.
    """
    if posición + 1 == 30:
        resultado = "victoria"
    elif posición == 0:
        resultado = "derrota"
    else:
        resultado = None
    return resultado

def crear_tablero_puntuación(nombre: str, posición: int):
    """
    Guarda el nombre y la puntuación del jugador en un archivo CSV.

    Parámetros:
        nombre (str): Nombre del jugador.
        posición (int): Posición alcanzada por el jugador.
    """
    try:
        with open("Puntuación.csv", "r") as archivo:
            líneas = archivo.readlines() # Intenta leer el archivo
    except FileNotFoundError:
        líneas = [] # Si no existe, líneas pasa a ser una lista vacía
    with open("Puntuación.csv", "a") as archivo:
        if len(líneas) == 0:
            archivo.write("jugador,puntuacion\n") # Si está vacío, escribe la cabecera
        archivo.write(f"{nombre}, {posición + 1}\n")

def leer_csv(nombre_archivo: str) -> tuple:
    """
    Lee los datos de un archivo CSV y los devuelve como una lista de tuplas.

    Parámetros:
        nombre_archivo (str): Nombre del archivo CSV.

    Devuelve:
        list: Lista de tuplas con los datos del archivo.
    """
    datos = []
    with open(nombre_archivo, "r") as archivo:
        líneas = archivo.readlines()[1:] # Descarta la cabecera del archivo
        for línea in líneas:
            elemento1, elemento2 = línea.split(",") # Separa el nombre del jugador de su posición
            datos.append((elemento1, elemento2))
    return datos

def convertir_puntuación_a_entero(tupla: tuple) -> int:
    """
    Convierte el string de la puntuación a un número entero para su uso como clave de ordenamiento.

    Parámetros:
        tupla (tuple): Tupla con el nombre y la puntuación.

    Devuelve:
        int: Puntuación convertida a entero.
    """
    return int(tupla[1])

def ordenar_csv(nombre_archivo:str) -> list:
    """
    Ordena los datos de un archivo CSV por puntuación de mayor a menor.

    Parámetros:
        nombre_archivo (str): Nombre del archivo CSV.

    Devuelve:
        list: Lista ordenada de tuplas con los datos del archivo.
    """
    elementos = leer_csv(nombre_archivo)
    elementos.sort(key=convertir_puntuación_a_entero, reverse=True) # Se pasa la función convertir_puntuación_a_entero como clave d eordenamiento, para que sort haga uso de ella por cada elemento de la tupla
    return elementos