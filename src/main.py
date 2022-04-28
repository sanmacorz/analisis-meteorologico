#!/usr/bin/env python3

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

owm = OWM('your free OWM API key')
mgr = owm.weather_manager()

# Search for current weather in London (Great Britain) and get details
observation = mgr.weather_at_place('London,GB')
w = observation.weather
w.detailed_status
w.wind()
w.humidity
w.temperature('celsius')
w.rain
w.heat_index
w.clouds

# Will it be clear tomorrow at this time in Milan (Italy) ?
forecast = mgr.forecast_at_place('Milan,IT', 'daily')
answer = forecast.will_be_clear_at(timestamps.tomorrow())
