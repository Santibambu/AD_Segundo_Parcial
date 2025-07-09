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
    extra = 0
    if avanzar == True:
        posición += 1
        extra += tablero[posición]
        posición += extra
    else:
        posición -= 1
        extra += tablero[posición]
        posición -= extra
    return (avanzar, extra, posición)

def verificar_posición(posición: int) -> str | None:
    """
    Verifica si la posición del jugador corresponde a victoria, derrota o continúa.

    Parámetros:
        posición (int): Posición actual del jugador.

    Devuelve:
        str: "victoria" o "derrota" si corresponde, None en caso contrario.
    """
    resultado = None
    if posición + 1 == 30:
        resultado = "victoria"
    elif posición == 0:
        resultado = "derrota"
    return resultado