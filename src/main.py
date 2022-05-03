#!/usr/bin/env python3
from pyowm import OWM
import functions
import requests
from datetime import datetime
import pytz

ciudad = str(input("Ingrese la ciudad a la que desea consultar: "))
pais = str(input("Por favor, utilice la convención ISO 3166 (https://www.iso.org/obp/ui/es/#search)\nIngrese el país a el que desea consultar: "))
api_key = str(functions.load_key("api.key"))
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
print("Se utilizarán las coordenadas: " + str(lat) + ", " + str(lon) + " a las: " + str(zona_horaria))
print("---Estadisticas climaticas---")
print("La velocidad del viento actual es de " + str(viento) + "m/s " + str(velocidad_viento))
print("La humedad actual es del " + str(humedad) + "%")
print("La temperatura actual es de " + str(temperatura) + "°C")
print("El estado del clima actual es de " + str(clima))
print("La lluvia actual es de " + str(lluvia) + "mm")
print("La nubosidad actual es del " + str(nubes) + "%")
print("---Estadisticas de calidad del aire---")
print("El nivel de CO es de: " + str(calidad_aire.co) + " μg/m3")
print("El nivel de NO es de: " + str(calidad_aire.no) + " μg/m3")
print("El nivel de NO2 es de: " + str(calidad_aire.no2) + " μg/m3")
print("El nivel de O3 es de: " + str(calidad_aire.o3) + " μg/m3")
print("El nivel de SO2 es de: " + str(calidad_aire.so2) + " μg/m3")
print("El nivel de NH3 es de: " + str(calidad_aire.nh3) + " μg/m3")
print("El nivel de PM25 es de: " + str(calidad_aire.pm2_5) + " μg/m3")
print("El nivel de PM10 es de: " + str(calidad_aire.pm10) + " μg/m3")
print("---Estadisticas de la luz ultravioleta---")
print("El índice de luz UV es de: " + str(uvi.value))