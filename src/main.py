#!/usr/bin/env python3

# https://pyowm.readthedocs.io/en/latest/

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import geojson
import json
import functions

ciudad = str(input("Ingrese la ciudad a la que desea consultar: "))
pais = str(input("Por favor, utilice la convención ISO 3166 (https://www.iso.org/obp/ui/es/#search)\nIngrese el país a el que desea consultar: "))

api_key = str(functions.load_key("api.key"))
owm = OWM(api_key)
config_dict = owm.configuration
config_dict['language'] = 'es'
reg = owm.city_id_registry()
list_of_locations = reg.locations_for(ciudad, country=pais, matching='like')
mgr = owm.weather_manager()
observation = mgr.weather_at_place(ciudad + ", " + pais)
current_city = list_of_locations[0]
one_call = mgr.one_call(lat=current_city.lat, lon=current_city.lon)
weather = observation.weather

temperatura = int(round(float(list(one_call.current.temperature('celsius').values())[0]),0))
viento = one_call.current.wind().get('speed', 0)
velocidad_viento = functions.convertir_direccion(weather.wind().get('deg', 0))
humedad = one_call.current.humidity
clima = weather.detailed_status
nubes = weather.clouds

try:
    lluvia = list(weather.rain.values())[0]
except IndexError as error:
    lluvia = "0"

print("\nLa velocidad del viento actual es de " + str(viento) + "m/s " + str(velocidad_viento))
print("La humedad actual es del " + str(humedad) + "%")
print("La temperatura actual es de " + str(temperatura) + "°C")
print("El estado del clima actual es de " + str(clima))
print("La lluvia actual es de " + str(lluvia) + "mm")
print("La nubosidad actual es del " + str(nubes) + "%")
