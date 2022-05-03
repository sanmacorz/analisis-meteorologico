#!/usr/bin/env python3

# Primero se importan todas las funciones, requerimientos y demas para que el programa pueda funcionar

from pyowm import OWM
import functions
import requests
from datetime import datetime
import pytz

# Despues se despliega una pequeña interfaz
while True:
    print("----------------------------------------------")
    print("-----  Análisis Metereológico \U0001F327 --------------")
    print("----------------------------------------------")

    titulo = "Bienvenido a nuestro proyecto!!!\n"
    print(titulo)

    # A continuación pedimos la información necesaria para que el programa pueda funcionar 

    ciudad = str(input("Ingrese la ciudad a la que desea consultar: "))
    pais = str(input("Por favor, utilice la convención ISO 3166 (https://www.iso.org/obp/ui/es/#search)\nIngrese el país a el que desea consultar: "))

    # Seguido de esto se solicita la opción que requiera el usuario

    print("¿Que desea buscar?\n")
    print("1. Coordenadas de la ubicación")
    print("2. Zona horaria")
    print("3. Velocidad del viento")
    print("4. Humedad actual")
    print("5 Temperatura actual")
    print("6. Estado del clima")
    print("7. Lluvia actual")
    print("8. Nubosidad actual")
    print("9. Luz ultra violeta")
    print("10. Calidad del aire")
    print("11. Mapa indice de calor")
    print("12. Predicción del clima")
    print("13. Estadisticas completas")
    print("15. Salir del programa")
    opcion = int(input("Digite el número de su opción: "))

    # Según los datos obtenidos de los anteriores puntos, se procesa la información y se extrae la información de la base de datos

    api_key = str(functions.cargar_llave("api.key"))
    owm = OWM(api_key)
    config_dict = owm.configuration
    config_dict['language'] = 'es'
    reg = owm.city_id_registry()
    list_of_locations = reg.locations_for(ciudad, country=pais, matching='like')
    weather_mgr = owm.weather_manager()
    pollution_mgr = owm.airpollution_manager()
    uvi_mgr = owm.uvindex_manager()
    observation = weather_mgr.weather_at_place(ciudad + ", " + pais)
    current_city = list_of_locations[0]
    lat = float(round(current_city.lat,4))
    lon = float(round(current_city.lon,4))
    peticion = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=***REMOVED***')
    zona_horaria = str(peticion.json()['timezone'])
    one_call = weather_mgr.one_call(lat=current_city.lat, lon=current_city.lon)
    weather = observation.weather
    zona_horaria = pytz.timezone(zona_horaria)
    zona_horaria = datetime.now(zona_horaria)
    temperatura = int(round(float(list(one_call.current.temperature('celsius').values())[0]),0))
    viento = one_call.current.wind().get('speed', 0)
    velocidad_viento = functions.convertir_direccion(weather.wind().get('deg', 0))
    humedad = one_call.current.humidity
    clima = weather.detailed_status
    nubes = weather.clouds
    calidad_aire = pollution_mgr.air_quality_at_coords(lat, lon)
    uvi = uvi_mgr.uvindex_around_coords(lat, lon)
    try:
        lluvia = list(weather.rain.values())[0]
    except IndexError as error:
        lluvia = 0

    # Al final, con los datos ya obtenidos de la base de datos, se imprime los resultados según la información que requiera el usuario

    if opcion == 1:
        print("\n---Coordenadas---\U0001F5FA\n")
        print("Las coordenadas son: " + str(lat) + " latitud, " + str(lon) + " longuitud.")

    elif opcion == 2:
        print("\n---Zona Horaria---\U0000231B\n")
        print("La zona horaria es: " + str(zona_horaria))

    elif opcion == 3:
        print("\n---Velocidad del viento---\U0001F32C\n")
        print("La velocidad del viento actual es de " + str(viento) + "m/s " + str(velocidad_viento))

    elif opcion == 4:
        print("\n---Humedad---\U0001F4A7\n")
        print("La humedad actual es del " + str(humedad) + "%")

    elif opcion == 5:
        print("\n---Temperatura---\U0001F321\n")
        print("La temperatura actual es de " + str(temperatura) + "°C")

    elif opcion == 6:
        print("\n---Estado del clima---\U0001F32C\n")
        print("El estado del clima actual es de " + str(clima))

    elif opcion == 7:
        print("\n---Lluvia---\U0001F327\n")
        print("La lluvia actual es de " + str(lluvia) + "mm")

    elif opcion == 8:
        print("\n---Nubosidad---\U000026C5\n")
        print("La nubosidad actual es del " + str(nubes) + "%")

    elif opcion == 9:
        print("\n---Luz Ultra Violeta---\U00002600\n")
        print("El índice de luz UV es de: " + str(uvi.value))

    elif opcion == 10:
        print("\n---Estadisticas de calidad del aire---\n")
        print("El nivel de CO es de: " + str(calidad_aire.co) + " μg/m3")
        print("El nivel de NO es de: " + str(calidad_aire.no) + " μg/m3")
        print("El nivel de NO2 es de: " + str(calidad_aire.no2) + " μg/m3")
        print("El nivel de O3 es de: " + str(calidad_aire.o3) + " μg/m3")
        print("El nivel de SO2 es de: " + str(calidad_aire.so2) + " μg/m3")
        print("El nivel de NH3 es de: " + str(calidad_aire.nh3) + " μg/m3")
        print("El nivel de PM25 es de: " + str(calidad_aire.pm2_5) + " μg/m3")
        print("El nivel de PM10 es de: " + str(calidad_aire.pm10) + " μg/m3")

    elif opcion == 13:
        print("Se utilizarán las coordenadas: " + str(lat) + ", " + str(lon) + " a las: " + str(zona_horaria))
        print("\n---Estadisticas climaticas---\n")
        print("La velocidad del viento actual es de " + str(viento) + "m/s " + str(velocidad_viento))
        print("La humedad actual es del " + str(humedad) + "%")
        print("La temperatura actual es de " + str(temperatura) + "°C")
        print("El estado del clima actual es de " + str(clima))
        print("La lluvia actual es de " + str(lluvia) + "mm")
        print("La nubosidad actual es del " + str(nubes) + "%")
        print("\n---Estadisticas de calidad del aire---\n")
        print("El nivel de CO es de: " + str(calidad_aire.co) + " μg/m3")
        print("El nivel de NO es de: " + str(calidad_aire.no) + " μg/m3")
        print("El nivel de NO2 es de: " + str(calidad_aire.no2) + " μg/m3")
        print("El nivel de O3 es de: " + str(calidad_aire.o3) + " μg/m3")
        print("El nivel de SO2 es de: " + str(calidad_aire.so2) + " μg/m3")
        print("El nivel de NH3 es de: " + str(calidad_aire.nh3) + " μg/m3")
        print("El nivel de PM25 es de: " + str(calidad_aire.pm2_5) + " μg/m3")
        print("El nivel de PM10 es de: " + str(calidad_aire.pm10) + " μg/m3")
        print("\n---Estadisticas de la luz ultravioleta---\n")
        print("El índice de luz UV es de: " + str(uvi.value))
    elif opcion == 15:
        print("Saliendo del programa ...")
        break
    else:
        print("Opción desconocida. \U0001F937")
