from Coordenadas import *
from Colores import *

def asignar_color_seleccionado(pos: tuple[int, int]) -> tuple[int, int, int]:
    """
    Asigna el color correspondiente según la posición seleccionada por el usuario.

    Parámetros:
        pos (tuple[int, int]): Coordenadas (x, y) del clic del usuario.

    Devuelve:
        tuple[int, int, int]: Color seleccionado en formato RGB, o None si no se selecciona ningún color.
    """
    def verificar_click_círculo(coordenadas: tuple[int, int], círculo: tuple[int, int, int]) -> bool:
        """
        Verifica si un punto está dentro de un círculo.

        Parámetros:
            coordenadas (tuple[int, int]): Coordenadas (x, y) del punto a verificar.
            círculo (tuple[int, int, int]): Tupla (centro_x, centro_y, radio) del círculo.

        Devuelve:
            bool: True si el punto está dentro del círculo, False en caso contrario.
        """
        x, y = coordenadas
        centro_x, centro_y, radio = círculo
        return (x - centro_x) ** 2 + (y - centro_y) ** 2 <= radio ** 2
    
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
        if verificar_click_círculo(pos, botón):
            return color