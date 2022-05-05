import os

def cargar_llave(ruta):
    """
    Carga la llave de la API almacenada en el directorio actual
    """
    directorio = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta)
    archivo = open(directorio, "r")
    llave = str(archivo.read().splitlines()[0])
    archivo.close()
    return(llave)

def convertir_direccion(angulo):
    """
    Convierte un ángulo en una dirección usando letras
    """
    if angulo == 0 or angulo == 360:
        direccion = "N"
    elif angulo > 0 and angulo < 90:
        direccion = "NE"
    elif angulo == 90:
        direccion = "E"
    elif angulo > 90 and angulo < 180:
        direccion = "SE"
    elif angulo == 180:
        direccion = "S"
    elif angulo > 180 and angulo < 270:
        direccion = "SO"
    elif angulo == 270:
        direccion = "O"
    elif angulo > 270 and angulo < 360:
        direccion = "NO"
    return(direccion)