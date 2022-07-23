#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk
from pyowm import OWM
from pyowm.utils.geo import Point
from pyowm.commons.tile import Tile
from pyowm.tiles.enums import MapLayerEnum
import funciones

ventana_principal = tk.Tk()
ventana_principal.geometry("1280x720")
ventana_principal.resizable(False, False)
ventana_principal.configure(background="#4DBFD9")
ventana_principal.title("Análisis meterológico")
ventana_principal.iconphoto(True, tk.PhotoImage(file="icono.png"))

seleccion = tk.IntVar()
seleccion.set(1)

frame_principal = tk.Frame(
    ventana_principal,
    width="1120",
    height="540",
    highlightthickness=5,
    highlightbackground="#4D4D4D",
)
frame_principal.configure(background="#FAFAFA")
frame_principal.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

canvas_principal = tk.Canvas(
    frame_principal,
    width="1024",
    height="576",
    highlightthickness=0,
    highlightbackground="#4D4D4D",
)
canvas_principal.configure(background="#FAFAFA")
canvas_principal.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

ruta = "media/"

titulo_proyecto = tk.Label(ventana_principal, text="Análisis meterológico")
titulo_proyecto.config(background="#4DBFD9", font=("Arial", 16, "bold"))
titulo_proyecto.place(x=550, y=50)

logo = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(ventana_principal, background="#4DBFD9", image=logo)
logo_label.place(x=1000, y=15)

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
    ("Índice de precipitación", 11),
    ("Índice de temperatura", 12),
    ("Índice de presión atmosférica", 13),
    ("Índice de velocidad del viento", 14),
]

canvas_principal.create_window(
    400,
    200,
    window=tkinter.ttk.Separator(canvas_principal, orient="vertical").grid(
        column=1, row=2, rowspan="18", sticky="ns"
    ),
)
canvas_principal.create_window(
    400,
    200,
    window=tk.Label(
        canvas_principal,
        text="Ciudad: ",
        background="#FAFAFA",
        font=(10),
    ).grid(row=2, column=2),
)
campo_texto = tk.Entry(canvas_principal)
campo_texto.config(font=(10), highlightthickness=3)
canvas_principal.create_window(400, 200, window=campo_texto.grid(row=2, column=3))

texto = tk.Label(canvas_principal)
imagen = tk.PhotoImage()


def obtener_datos():
    global ciudad, latitud, longitud, temperatura, velocidad_viento, direccion_viento, humedad, clima_general, nubes, calidad_aire, iuv, lluvia, numero_archivo_prec, numero_archivo_temp, numero_archivo_pres, numero_archivo_viento
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
    latitud = float(round(ciudad_actual.lat, 4))
    longitud = float(round(ciudad_actual.lon, 4))
    llamada = adm_clima.one_call(lat=latitud, lon=longitud)
    clima = observacion.weather
    temperatura = int(
        round(float(list(llamada.current.temperature("celsius").values())[0]), 0)
    )
    velocidad_viento = llamada.current.wind().get("speed", 0)
    direccion_viento = funciones.convertir_direccion(clima.wind().get("deg", 0))
    humedad = llamada.current.humidity
    clima_general = clima.detailed_status
    nubes = clima.clouds
    calidad_aire = adm_contaminacion.air_quality_at_coords(latitud, longitud)
    iuv = adm_iuv.uvindex_around_coords(latitud, longitud)
    try:
        lluvia = list(clima.rain.values())[0]
    except IndexError:
        lluvia = 0
    punto_geologico = Point(longitud, latitud)
    zoom_precipitacion = 7  # Radio de 250 km
    zoom_temperatura = 8  # Radio de 100 km
    x_tile, y_tile = Tile.tile_coords_for_point(punto_geologico, zoom_precipitacion)
    tm_prec = owm.tile_manager(MapLayerEnum.PRECIPITATION)
    cuadricula = tm_prec.get_tile(x_tile, y_tile, zoom_precipitacion)
    numero_archivo_prec = funciones.archivo_repetido(ruta)
    cuadricula.persist(ruta + numero_archivo_prec)
    x_tile, y_tile = Tile.tile_coords_for_point(punto_geologico, zoom_temperatura)
    tm_temp = owm.tile_manager(MapLayerEnum.TEMPERATURE)
    cuadricula = tm_temp.get_tile(x_tile, y_tile, zoom_temperatura)
    numero_archivo_temp = funciones.archivo_repetido(ruta)
    cuadricula.persist(ruta + numero_archivo_temp)
    x_tile, y_tile = Tile.tile_coords_for_point(punto_geologico, zoom_precipitacion)
    tm_pres = owm.tile_manager(MapLayerEnum.PRESSURE)
    cuadricula = tm_pres.get_tile(x_tile, y_tile, zoom_precipitacion)
    numero_archivo_pres = funciones.archivo_repetido(ruta)
    cuadricula.persist(ruta + numero_archivo_pres)
    x_tile, y_tile = Tile.tile_coords_for_point(punto_geologico, zoom_precipitacion)
    tm_viento = owm.tile_manager(MapLayerEnum.WIND)
    cuadricula = tm_viento.get_tile(x_tile, y_tile, zoom_precipitacion)
    numero_archivo_viento = funciones.archivo_repetido(ruta)
    cuadricula.persist(ruta + numero_archivo_viento)


def mostrar_datos():
    global texto, imagen
    opcion = seleccion.get()
    resultado_coordenadas = str(latitud) + " latitud, " + str(longitud) + " longuitud."
    resultado_velocidad_viento = (
        "La velocidad del viento actual es de "
        + str(velocidad_viento)
        + "m/s "
        + str(direccion_viento)
    )
    unidad_particulas = " μg/m3"
    resultado_humedad = "La humedad actual es del " + str(humedad) + "%"
    resultado_temperatura = "La temperatura actual es de " + str(temperatura) + "°C"
    resultado_clima_general = "El estado del clima actual es de " + str(clima_general)
    resultado_lluvia = "La lluvia actual es de " + str(lluvia) + "mm"
    resultado_nubes = "La nubosidad actual es del " + str(nubes) + "%"
    resultado_co = "El nivel de CO es de " + str(calidad_aire.co) + unidad_particulas
    resultado_no = "El nivel de NO es de " + str(calidad_aire.no) + unidad_particulas
    resultado_no2 = "El nivel de NO2 es de " + str(calidad_aire.no2) + unidad_particulas
    resultado_o3 = "El nivel de O3 es de " + str(calidad_aire.o3) + unidad_particulas
    resultado_so2 = "El nivel de SO2 es de " + str(calidad_aire.so2) + unidad_particulas
    resultado_nh3 = "El nivel de NH3 es de " + str(calidad_aire.nh3) + unidad_particulas
    resultado_pm25 = (
        "El nivel de PM25 es de " + str(calidad_aire.pm2_5) + unidad_particulas
    )
    resultado_pm10 = (
        "El nivel de PM10 es de " + str(calidad_aire.pm10) + unidad_particulas
    )
    resultado_iuv = "El índice de luz UV es de " + str(iuv.value)

    if opcion == 1:
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado_coordenadas)
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, columnspan=5)
        )
    elif opcion == 2:
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado_velocidad_viento)
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, columnspan=5)
        )
    elif opcion == 3:
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado_humedad)
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, columnspan=5)
        )
    elif opcion == 4:
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado_temperatura)
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, columnspan=5)
        )
    elif opcion == 5:
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado_clima_general)
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, columnspan=5)
        )
    elif opcion == 6:
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado_lluvia)
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, columnspan=5)
        )
    elif opcion == 7:
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado_nubes)
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, columnspan=5)
        )
    elif opcion == 8:
        texto.destroy()
        texto = tk.Label(canvas_principal, text=resultado_iuv)
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, columnspan=5)
        )
    elif opcion == 9:
        texto.destroy()
        texto = tk.Label(
            canvas_principal,
            text=resultado_co
            + "\n"
            + resultado_no
            + "\n"
            + resultado_no2
            + "\n"
            + resultado_o3
            + "\n"
            + resultado_so2
            + "\n"
            + resultado_nh3
            + "\n"
            + resultado_pm25
            + "\n"
            + resultado_pm10,
        )
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, rowspan=12, columnspan=5)
        )
    elif opcion == 10:
        texto.destroy()
        texto = tk.Label(
            canvas_principal,
            text=resultado_velocidad_viento
            + "\n"
            + resultado_humedad
            + "\n"
            + resultado_temperatura
            + "\n"
            + resultado_clima_general
            + "\n"
            + resultado_lluvia
            + "\n"
            + resultado_nubes
            + "\n"
            + resultado_co
            + "\n"
            + resultado_no
            + "\n"
            + resultado_no2
            + "\n"
            + resultado_o3
            + "\n"
            + resultado_so2
            + "\n"
            + resultado_nh3
            + "\n"
            + resultado_pm25
            + "\n"
            + resultado_pm10
            + "\n"
            + resultado_iuv,
            background="#FAFAFA",
        )
        texto.config(background="#FAFAFA", foreground="#1A1A1A", font=(10))
        canvas_principal.create_window(
            400, 200, window=texto.grid(row=3, column=2, rowspan=15, columnspan=5)
        )

    elif opcion == 11:
        texto.destroy()
        canvas_principal.delete(imagen)
        archivo = ruta + numero_archivo_prec
        imagen = tk.PhotoImage(file=archivo)
        canvas_principal.create_image(500, 120, anchor=tk.CENTER, image=imagen)
    elif opcion == 12:
        texto.destroy()
        canvas_principal.delete(imagen)
        archivo = ruta + numero_archivo_temp
        imagen = tk.PhotoImage(file=archivo)
        canvas_principal.create_image(500, 120, anchor=tk.CENTER, image=imagen)
    elif opcion == 13:
        texto.destroy()
        canvas_principal.delete(imagen)
        archivo = ruta + numero_archivo_pres
        imagen = tk.PhotoImage(file=archivo)
        canvas_principal.create_image(500, 120, anchor=tk.CENTER, image=imagen)
    elif opcion == 14:
        texto.destroy()
        canvas_principal.delete(imagen)
        archivo = ruta + numero_archivo_viento
        imagen = tk.PhotoImage(file=archivo)
        canvas_principal.create_image(500, 120, anchor=tk.CENTER, image=imagen)


filas = 3

for opcion, val in opciones:
    filas += 1
    boton = tk.Radiobutton(
        canvas_principal,
        text=opcion,
        variable=seleccion,
        value=val,
        background="#FAFAFA",
        highlightthickness=0,
        font=(10),
    ).grid(row=filas, column=0, sticky=tk.W)
    canvas_principal.create_window(400, 200, window=boton)


canvas_principal.create_window(
    400,
    200,
    window=tk.Button(
        canvas_principal,
        text="Consultar",
        borderwidth=3,
        relief="raised",
        command=lambda: [obtener_datos(), mostrar_datos()],
    ).grid(row=20, column=1, pady=(30, 10)),
)

canvas_principal.create_window(
    400,
    200,
    window=tk.Button(
        canvas_principal,
        text="Salir",
        borderwidth=3,
        relief="raised",
        command=ventana_principal.destroy,
    ).grid(row=21, column=1),
)

ventana_principal.mainloop()
