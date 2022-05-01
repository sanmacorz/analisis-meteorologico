def load_key(path):
    """
    Loads the API key from the current directory
    """
    file = open(path, "r")
    key = str(file.read().splitlines()[0])
    file.close()
    return(key)

def convertir_direccion(grados):
    if grados == 0 or grados == 360:
        direccion = "N"
    elif grados > 0 and grados < 90:
        direccion = "NE"
    elif grados == 90:
        direccion = "E"
    elif grados > 90 and grados < 180:
        direccion = "SE"
    elif grados == 180:
        direccion = "S"
    elif grados > 180 and grados < 270:
        direccion = "SO"
    elif grados == 270:
        direccion = "O"
    elif grados > 270 and grados < 360:
        direccion = "NO"
    return(direccion)
