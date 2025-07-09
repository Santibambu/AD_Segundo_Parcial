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