import pandas as pd
import numpy as np
import requests
import json
import time


def data_get(zipcode, key):
    '''A helper function to grab data from openweathermap.org
    Args:
        zipcode: a zipcode, str
        key: secret key, str
    Returns:
    '''
    # Getting the dictionary object
    info_dict = json.loads(requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' +
                                        zipcode + ',us&appid=' + key).content)

    # Getting relevant info
    lat = info_dict['coord']['lat']
    lon = info_dict['coord']['lon']
    status = info_dict['weather'][0]['description']
    temp = (info_dict['main']['temp'] - 273.15) * (9 / 5) + 32
    pressure = info_dict['main']['pressure']
    humidity = info_dict['main']['humidity']
    temp_min = (info_dict['main']['temp_min'] - 273.15) * (9 / 5) + 32
    temp_max = (info_dict['main']['temp_max'] - 273.15) * (9 / 5) + 32
    wind = info_dict['wind']['speed']
    sunrise = time.ctime(info_dict['sys']['sunrise']).split(' ')[3]
    sunset = time.ctime(info_dict['sys']['sunset']).split(' ')[3]

    # Creating a pandas df
    return pd.DataFrame(data=[[zipcode, lat, lon, status, temp, pressure, humidity, temp_min,
                               temp_max, wind, sunrise, sunset]],
                        columns=['zipcode', 'lat', 'lon', 'status', 'temp', 'pressure',
                                 'humidity', 'temp_min', 'temp_max', 'wind',
                                 'sunrise', 'sunset'])

