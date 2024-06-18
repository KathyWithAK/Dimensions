import requests, json
import time

"""
Weather

    A module of all the weather-related functions and data collecting.

"""
def get_weather_data(latitude=42.0158121, longitude=-71.5503353):
    weather_data = {}

    # Call the main NWS api using coords
    url = f"https://api.weather.gov/points/{latitude},{longitude}"

    response = requests.get(url)
    json_data = response.json()

    j_properties = json_data['properties']

    weather_data['radarStation'] = j_properties['radarStation']            
    weather_data['timeZone'] = j_properties['timeZone']

    j_relativelocation = j_properties['relativeLocation']

    weather_data['city'] = j_relativelocation['properties']['city']
    weather_data['state'] = j_relativelocation['properties']['state']

    response = requests.get(j_properties['forecast'])
    json_data = response.json()

    j_properties = json_data['properties']

    weather_data['updated'] = json_data['properties']['generatedAt']

    j_properties = json_data['properties']['periods']

    weather_data['weatherPeriods'] = []

    for p in json_data['properties']['periods']:
        weather_period = {}

        weather_period['number'] = p['number']
        weather_period['name'] = p['name']
        weather_period['startTime'] = p['startTime']
        weather_period['endTime'] = p['endTime']
        weather_period['isDaytime'] = p['isDaytime']
        weather_period['temperature'] = p['temperature']                
        weather_period['temperatureUnit'] = p['temperatureUnit']
        weather_period['probabilityOfPrecipitation'] = {'unit': p['probabilityOfPrecipitation']['unitCode'],
                                                            'value': p['probabilityOfPrecipitation']['value'] }
        weather_period['dewpoint'] = {'unit': p['dewpoint']['unitCode'],
                                            'value': p['dewpoint']['value'] }
        weather_period['relativeHumidity'] = {'unit': p['relativeHumidity']['unitCode'],
                                                    'value': p['relativeHumidity']['value'] }
        weather_period['windSpeed'] = p['windSpeed']
        weather_period['windDirection'] = p['windDirection']
        weather_period['shortForecast'] = p['shortForecast']
        weather_period['detailedForecast'] = p['detailedForecast']

        weather_data['weatherPeriods'].append(weather_period)

    return weather_data

def get_sun_data(latitude=42.0158121, longitude=-71.5503353, tzid=None):
    sun_data = {}

    # Call the main api using coords
    if tzid:
        url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&tzid={tzid}"
    else: 
        url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}"
    
    response = requests.get(url)
    json_data = response.json()

    sun_data['sunrise'] = json_data['results']['sunrise']
    sun_data['sunset'] = json_data['results']['sunset']
    sun_data['solar_noon'] = json_data['results']['solar_noon']
    sun_data['day_length'] = json_data['results']['day_length']
    sun_data['civil_twilight_begin'] = json_data['results']['civil_twilight_begin']
    sun_data['civil_twilight_end'] = json_data['results']['civil_twilight_end']
    sun_data['nautical_twilight_begin'] = json_data['results']['nautical_twilight_begin']
    sun_data['nautical_twilight_end'] = json_data['results']['nautical_twilight_end']
    sun_data['astronomical_twilight_begin'] = json_data['results']['astronomical_twilight_begin']
    sun_data['astronomical_twilight_end'] = json_data['results']['astronomical_twilight_end']

    return sun_data
    
def get_moon_data(latitude=42.0158121, longitude=-71.5503353):
    moon_data = {}
    utc = time.time()

    # Call the main api using coords
    url = f"http://api.farmsense.net/v1/moonphases/?d={int(utc)}&lat={latitude}&lng={longitude}"
    
    response = requests.get(url, verify=True)
    json_data = response.json()

    moon_data['moon'] = json_data[0]['Moon'][0]
    moon_data['age'] = json_data[0]['Age']
    moon_data['phase'] = json_data[0]['Phase']
    moon_data['distance'] = json_data[0]['Distance']
    moon_data['illumination'] = json_data[0]['Illumination']
    moon_data['angularDiameter'] = json_data[0]['AngularDiameter']
    moon_data['distanceToSun'] = json_data[0]['DistanceToSun']
    moon_data['sunAngularDiameter'] = json_data[0]['SunAngularDiameter']

    return moon_data

def get_celcius_fahrenheit(temp, unit):
    if unit == 'F' or unit == "wmoUnit:degF":
        temp_f = float(temp)
        temp_c = (temp_f - 32.0) * (5.0 / 9.0)
    else:
        temp_c = float(temp)
        temp_f = (temp_c * (5.0 / 9.0)) + 32.0
    return temp_c, temp_f
