import pygame

def detectar_abandono(eventos: list, estado_juego: str) -> bool:
    """
    Verifica si el usuario ha abandonado el juego.

    Parámetros:
        eventos (list): Lista de eventos capturados por pygame.
        estado_juego (str): Estado actual del juego.

    Devuelve:
        bool: True si el usuario abandona el juego, False en caso contrario.
    """
    salir = False
    for evento in eventos:
        if evento.type == pygame.QUIT:
            salir = True
    if estado_juego == "salir":
        salir = True
    return salir

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