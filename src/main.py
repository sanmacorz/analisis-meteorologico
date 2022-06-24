import tkinter as tk
import tkinter.ttk
from pyowm import OWM
from pyowm.utils.geo import Point
from pyowm.commons.tile import Tile
from pyowm.tiles.enums import MapLayerEnum
import funciones

# #4DBFD9 - Segundo plano
# #FAFAFA - Primer plano
# #4D4D4D - Barra
# #1A1A1A - Texto
# #FEE573 - Imagenes

raiz = tk.Tk()
raiz.geometry("1920x1080")
raiz.configure(bg="#4DBFD9")

seleccion = tk.IntVar()
seleccion.set(1)

canvas_principal = tk.Canvas(
    raiz,
    width="1280",
    height="720",
    highlightthickness=5,
    highlightbackground="#4D4D4D",
)
canvas_principal.configure(bg="#FAFAFA")
canvas_principal.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

titulo_proyecto = tk.Label(canvas_principal, text="Análisis meterológico")
titulo_proyecto.config(bg="#FAFAFA", font=("Arial", 14))
titulo_proyecto.grid(row=0, column=1, padx=15, pady=15)

bienvenido_proyecto = tk.Label(canvas_principal, text="Bienvenido a nuestro proyecto!")
bienvenido_proyecto.config(bg="#FAFAFA", font=("Arial", 14))
bienvenido_proyecto.grid(row=1, column=1)

opciones = [
    ("Coordenadas de la ubicación", 1),
    ("Velocidad del viento", 2),
    ("Humedad actual", 3),
    ("Temperatura actual", 4),
    ("Estado del clima", 5),
    ("Lluvia actual", 6),
    ("Nubosidad actual", 7),
    ("Luz ultra violeta", 8),
    ("Calidad del aire", 9),
    ("Estadisticas completas", 10),
    ("Mapa del índice de precipitación", 11),
    ("Mapa del índice de temperatura", 12),
]

canvas_principal.create_window(
    400,
    200,
    window=tk.Label(canvas_principal, text="Qué desea consultar?").grid(
        row=2, column=0
    ),
)
canvas_principal.create_window(
    400,
    200,
    window=tkinter.ttk.Separator(canvas_principal, orient="vertical").grid(
        column=1, row=2, rowspan="19", sticky="ns"
    ),
)
canvas_principal.create_window(
    400,
    200,
    window=tk.Label(
        canvas_principal, text="Ingrese la ciudad a la que desea consultar: "
    ).grid(row=2, column=2),
)
campo_texto = tk.Entry(canvas_principal)
canvas_principal.create_window(400, 200, window=campo_texto.grid(row=2, column=3))
global texto
texto = tk.Label(canvas_principal)


def obtenerDatos():
    global ciudad
    ciudad = campo_texto.get()
    llave_api = str(funciones.cargar_llave("api.key"))
    owm = OWM(llave_api)
    config_dict = owm.configuration
    config_dict["language"] = "es"
    registro = owm.city_id_registry()
    pais = "CO"
    lista_ubicaciones = registro.locations_for(ciudad, country=pais, matching="like")
    adm_clima = owm.weather_manager()
    adm_contaminacion = owm.airpollution_manager()
    adm_iuv = owm.uvindex_manager()
    observacion = adm_clima.weather_at_place(ciudad + ", " + pais)
    ciudad_actual = lista_ubicaciones[0]
    global latitud
    latitud = float(round(ciudad_actual.lat, 4))
    global longitud
    longitud = float(round(ciudad_actual.lon, 4))
    llamada = adm_clima.one_call(lat=latitud, lon=longitud)
    clima = observacion.weather
    global temperatura
    temperatura = int(
        round(float(list(llamada.current.temperature("celsius").values())[0]), 0)
    )
    global velocidad_viento
    velocidad_viento = llamada.current.wind().get("speed", 0)
    global direccion_viento
    direccion_viento = funciones.convertir_direccion(clima.wind().get("deg", 0))
    global humedad
    humedad = llamada.current.humidity
    global clima_general
    clima_general = clima.detailed_status
    global nubes
    nubes = clima.clouds
    global calidad_aire
    calidad_aire = adm_contaminacion.air_quality_at_coords(latitud, longitud)
    global iuv
    iuv = adm_iuv.uvindex_around_coords(latitud, longitud)
    global lluvia
    try:
        lluvia = list(clima.rain.values())[0]
    except IndexError as error:
        lluvia = 0
    punto_geologico = Point(longitud, latitud)
    zoom_precipitacion = 7  # Radio de 250 km
    zoom_temperatura = 8  # Radio de 100 km
    x_tile, y_tile = Tile.tile_coords_for_point(punto_geologico, zoom_precipitacion)
    tm_prec = owm.tile_manager(MapLayerEnum.PRECIPITATION)
    cuadricula = tm_prec.get_tile(x_tile, y_tile, zoom_precipitacion)
    global numero_archivo_prec
    numero_archivo_prec = funciones.archivo_repetido("media/")
    cuadricula.persist("media/" + numero_archivo_prec)
    x_tile, y_tile = Tile.tile_coords_for_point(punto_geologico, zoom_temperatura)
    tm_temp = owm.tile_manager(MapLayerEnum.TEMPERATURE)
    cuadricula = tm_temp.get_tile(x_tile, y_tile, zoom_temperatura)
    global numero_archivo_temp
    numero_archivo_temp = funciones.archivo_repetido("media/")
    cuadricula.persist("media/" + numero_archivo_temp)


def mostrarDatos():
    global texto
    opcion = seleccion.get()
    if opcion == 1:
        resultado = (
            "Las coordenadas de "
            + ciudad
            + " son "
            + str(latitud)
            + " latitud, "
            + str(longitud)
            + " longuitud."
        )
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        texto.config(bg="#FAFAFA", font=("Arial", 14))
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
    elif opcion == 2:
        resultado = (
            "La velocidad del viento actual es de "
            + str(velocidad_viento)
            + "m/s "
            + str(direccion_viento)
        )
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
    elif opcion == 3:
        resultado = "La humedad actual es del " + str(humedad) + "%"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
    elif opcion == 4:
        resultado = "La temperatura actual es de " + str(temperatura) + "°C"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
    elif opcion == 5:
        resultado = "El estado del clima actual es " + str(clima_general)
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
    elif opcion == 6:
        resultado = "La lluvia actual es de " + str(lluvia) + "mm"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
    elif opcion == 7:
        resultado = "La nubosidad actual es del " + str(nubes) + "%"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
    elif opcion == 8:
        resultado = "El índice de luz UV es de: " + str(iuv.value)
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
    elif opcion == 9:
        resultado = "El nivel de CO es de: " + str(calidad_aire.co) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
        resultado = "El nivel de NO es de: " + str(calidad_aire.no) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=4, column=2))
        resultado = "El nivel de NO2 es de: " + str(calidad_aire.no2) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=5, column=2))
        resultado = "El nivel de O3 es de: " + str(calidad_aire.o3) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=6, column=2))
        resultado = "El nivel de SO2 es de: " + str(calidad_aire.so2) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=7, column=2))
        resultado = "El nivel de NH3 es de: " + str(calidad_aire.nh3) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=8, column=2))
        resultado = "El nivel de PM25 es de: " + str(calidad_aire.pm2_5) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=9, column=2))
        resultado = "El nivel de PM10 es de: " + str(calidad_aire.pm10) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=10, column=2))
    elif opcion == 10:
        resultado = (
            "La velocidad del viento actual es de "
            + str(velocidad_viento)
            + "m/s "
            + str(direccion_viento)
        )
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))
        resultado = "La humedad actual es del " + str(humedad) + "%"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=4, column=2))
        resultado = "La temperatura actual es de " + str(temperatura) + "°C"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=5, column=2))
        resultado = "El estado del clima actual es de " + str(clima_general)
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=6, column=2))
        resultado = "La lluvia actual es de " + str(lluvia) + "mm"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=7, column=2))
        resultado = "La nubosidad actual es del " + str(nubes) + "%"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=8, column=2))
        resultado = "El nivel de CO es de: " + str(calidad_aire.co) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=9, column=2))
        resultado = "El nivel de NO es de: " + str(calidad_aire.no) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=10, column=2))
        resultado = "El nivel de NO2 es de: " + str(calidad_aire.no2) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=11, column=2))
        resultado = "El nivel de O3 es de: " + str(calidad_aire.o3) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=12, column=2))
        resultado = "El nivel de SO2 es de: " + str(calidad_aire.so2) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=13, column=2))
        resultado = "El nivel de NH3 es de: " + str(calidad_aire.nh3) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=14, column=2))
        resultado = "El nivel de PM25 es de: " + str(calidad_aire.pm2_5) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=15, column=2))
        resultado = "El nivel de PM10 es de: " + str(calidad_aire.pm10) + " μg/m3"
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=16, column=2))
        resultado = "El índice de luz UV es de: " + str(iuv.value)
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=17, column=2))
    elif opcion == 11:
        archivo = "media/" + numero_archivo_prec
        imagen = tk.PhotoImage(file=archivo)
        canvas_principal.create_image(600, 300, anchor=tk.W, image=imagen).grid(
            row=3, column=2
        )
    elif opcion == 12:
        archivo = "media/" + numero_archivo_temp
        imagen = tk.PhotoImage(file=archivo)
        canvas_principal.create_image(600, 300, anchor=tk.W, image=imagen).grid(
            row=3, column=2
        )
    else:
        resultado = "Opción desconocida."
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado)
        canvas_principal.create_window(400, 200, window=texto.grid(row=3, column=2))


canvas_principal.create_window(
    400,
    200,
    window=tk.Button(
        canvas_principal,
        text="Consultar",
        command=lambda: [obtenerDatos(), mostrarDatos()],
    ).grid(row=20, column=1),
)

filas = 3

for opcion, val in opciones:
    filas += 1
    boton = tk.Radiobutton(
        canvas_principal, text=opcion, variable=seleccion, value=val
    ).grid(row=filas, column=0)
    canvas_principal.create_window(400, 200, window=boton)

canvas_principal.create_window(
    400, 200, window=tk.Label(canvas_principal, text=opcion).grid(row=19, column=0)
)
canvas_principal.create_window(
    400,
    200,
    window=tk.Button(canvas_principal, text="Salir", command=raiz.destroy).grid(
        row=21, column=1
    ),
)

raiz.mainloop()
