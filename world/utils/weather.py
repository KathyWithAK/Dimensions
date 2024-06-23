import requests, json
import time, re
from bs4 import BeautifulSoup

"""
Weather

    A module of all the weather-related functions and data collecting.

"""
direction_map = {
    'NORTH': 'N', 'SOUTH': 'S', 'EAST': 'E', 'WEST': 'W',
    'NORTHEAST': 'NE', 'NORTHWEST': 'NW',
    'SOUTHEAST': 'SE', 'SOUTHWEST': 'SW',
}

def get_weather_data(latitude=42.0158121, longitude=-71.5503353):
    weather_data = {}

    # Call the main NWS api using coords
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(url, headers=headers)
    json_data = response.json()

    j_properties = json_data['properties']

    weather_data['radarStation'] = j_properties['radarStation']            
    weather_data['timeZone'] = j_properties['timeZone']

    j_relativelocation = j_properties['relativeLocation']

    weather_data['city'] = j_relativelocation['properties']['city']
    weather_data['state'] = j_relativelocation['properties']['state']

    weekly_forecast = j_properties['forecast']
    hourly_forecast = j_properties['forecastHourly']

    response = requests.get(weekly_forecast)
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
        #weather_period['dewpoint'] = {'unit': p['dewpoint']['unitCode'],
        #                                    'value': p['dewpoint']['value'] }
        #weather_period['relativeHumidity'] = {'unit': p['relativeHumidity']['unitCode'],
        #                                            'value': p['relativeHumidity']['value'] }
        weather_period['windSpeed'] = p['windSpeed']
        weather_period['windDirection'] = p['windDirection']
        weather_period['shortForecast'] = p['shortForecast']
        weather_period['detailedForecast'] = p['detailedForecast']

        weather_data['weatherPeriods'].append(weather_period)

    response = requests.get(hourly_forecast)
    json_data = response.json()
    
    p = json_data['properties']['periods'][0]
    if p:
        weather_data['dewpoint'] = {'unit': p['dewpoint']['unitCode'],
                                                         'value': p['dewpoint']['value'] }
        weather_data['relativeHumidity'] = {'unit': p['relativeHumidity']['unitCode'],
                                                    'value': p['relativeHumidity']['value'] }

    # Call secondary API for more info using coords
    url = f"https://www.timeanddate.com/weather/@{latitude},{longitude}"    

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            info_table2 = soup.find('table', {'class' : 'table--inner-borders-rows'})
            if info_table2:
                for info_row in info_table2.find_all('tr'):
                    if 'Visibility' in info_row.th.text:
                        vis = ''.join(i for i in info_row.td.text if ord(i)<128)
                        d = re.search(r"([0-9.]*)([^s]*)", vis)
                        if d.groups():                    
                            weather_data['visibility'] = d.groups(1)[0]
                            weather_data['visibility_scale'] = d.groups(1)[1]
                    elif 'Pressure' in info_row.th.text:
                        pre = info_row.td.text.strip()
                        d = re.search(r"([0-9.]*)", pre)
                        if d.groups():                    
                            weather_data['pressure'] = d.groups(1)[0]                        
                    elif 'Humidity' in info_row.th.text:
                        weather_data['humidity'] = info_row.td.text.strip()[:-1]
    except:
        pass

    return weather_data

def get_sun_data(latitude=42.0158121, longitude=-71.5503353, tzid=None):
    sun_data = {}

    # Call the main api using coords\
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    if tzid:
        url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&tzid={tzid}"
    else: 
        url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}"
    
    response = requests.get(url, headers=headers)
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

    # Call secondary API for more info using coords
    url = f"https://www.timeanddate.com/astronomy/@{latitude},{longitude}"    

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            info_table1 = soup.find('table', {'class' : 'table--inner-borders-rows'})
            if info_table1:
                for info_row in info_table1.find_all('tr'):
                    if 'Sunrise Today:' in info_row.text:
                        d = re.search(r"[0-9]{1,2}:[0-9]{1,2}\s[apm]{2}[^\s][\s]([^\s]*)[\s]([^#]*)",
                                    info_row.td.text)
                        if d.groups():
                            sun_data['sunrise_degrees'] = d.groups(1)[0][:-1]
                            sun_data['sunrise_direction'] = d.groups(1)[1].strip()
                            sun_data['sunrise_direction'] = direction_map[sun_data['sunrise_direction'].upper()]
                    elif 'Sunset Today:' in info_row.text:
                        d = re.search(r"[0-9]{1,2}:[0-9]{1,2}\s[apm]{2}[^\s][\s]([^\s]*)[\s]([^#]*)",
                                    info_row.td.text)
                        if d.groups():
                            sun_data['sunset_degrees'] = d.groups(1)[0][:-1]
                            sun_data['sunset_direction'] = d.groups(1)[1].strip()
                            sun_data['sunset_direction'] = direction_map[sun_data['sunset_direction'].upper()]
    except:
        pass

    url = f"https://www.timeanddate.com/sun/@{latitude},{longitude}"    

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            info_table1 = soup.find('table', {'class' : 'table--inner-borders-rows'})
            if info_table1:
                for info_row in info_table1.find_all('tr'):

                    if 'Sun Direction:' in info_row.text:
                        d = re.search(r"[^0-9]*([0-9]*)[^\s]*[\s]([^~]*)",
                                      info_row.td.text.strip())
                        if d.groups():
                            sun_data['sun_direction_degrees'] = d.groups(1)[0]
                            sun_data['sun_direction_direction'] = d.groups(1)[1].strip()
                            sun_data['sun_direction_direction'] = direction_map[sun_data['sun_direction_direction'].upper()]

                    elif 'Sun Distance:' in info_row.text:
                        sun_data['sun_distance'] = info_row.td.text.strip()
                    elif 'Sun Altitude:' in info_row.text:
                        sun_data['sun_altitude'] = info_row.td.text.strip()[:-1]
                    elif 'Next Solstice:' in info_row.text:
                        sun_data['next_solstice'] = info_row.td.text.strip()
                    elif 'Next Equinox:' in info_row.text:
                        sun_data['next_equinox'] = info_row.td.text.strip()                        
    except:
        pass

    return sun_data
    
def get_moon_data(latitude=42.0158121, longitude=-71.5503353):
    moon_data = {}
    utc = time.time()

    # Call the main api using coords
    url = f"http://api.farmsense.net/v1/moonphases/?d={int(utc)}&lat={latitude}&lng={longitude}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    response = requests.get(url, headers=headers, verify=True)
    json_data = response.json()

    moon_data['moon'] = json_data[0]['Moon'][0]
    moon_data['age'] = json_data[0]['Age']
    moon_data['phase'] = json_data[0]['Phase']
    moon_data['distance'] = json_data[0]['Distance']
    moon_data['illumination'] = json_data[0]['Illumination']
    moon_data['angularDiameter'] = json_data[0]['AngularDiameter']
    moon_data['distanceToSun'] = json_data[0]['DistanceToSun']
    moon_data['sunAngularDiameter'] = json_data[0]['SunAngularDiameter']

    # Call secondary API for more info using coords
    url = f"https://www.timeanddate.com/astronomy/@{latitude},{longitude}"    

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            info_table1 = soup.find('table', {'class' : 'table--inner-borders-rows'})
            if info_table1:
                for info_row in info_table1.find_all('tr'):
                    if 'Moonrise Today:' in info_row.text:
                        d = re.search(r"([0-9]{1,2}:[0-9]{1,2}\s[apm]{2})[^\s][\s]([^\s]*)[\s]([^#]*)",
                                    info_row.td.text)
                        if d.groups():
                            moon_data['moonrise_time'] = d.groups(1)[0].upper()
                            moon_data['moonrise_degrees'] = d.groups(1)[1][:-1]
                            moon_data['moonrise_direction'] = d.groups(1)[2].strip()
                            moon_data['moonrise_direction'] = direction_map[moon_data['moonrise_direction'].upper()]
                    elif 'Moonset Today:' in info_row.text:
                        d = re.search(r"([0-9]{1,2}:[0-9]{1,2}\s[apm]{2})[^\s][\s]([^\s]*)[\s]([^#]*)",
                                    info_row.td.text)
                        if d.groups():
                            moon_data['moonset_time'] = d.groups(1)[0].upper()
                            moon_data['moonset_degrees'] = d.groups(1)[1][:-1]
                            moon_data['moonset_direction'] = d.groups(1)[2].strip()
                            moon_data['moonset_direction'] = direction_map[moon_data['moonset_direction'].upper()]
    except:
        pass

    url = f"https://www.timeanddate.com/moon/@{latitude},{longitude}"    

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            info_table1 = soup.find('table', {'class' : 'table--inner-borders-rows'})
            if info_table1:
                for info_row in info_table1.find_all('tr'):

                    if 'Next New Moon:' in info_row.text:
                        moon_data['next_new_moon'] = info_row.td.text.strip()
                    elif 'Next Full Moon:' in info_row.text:
                        moon_data['next_full_moon'] = info_row.td.text.strip()
                     
    except:
        pass


    return moon_data

def get_celcius_fahrenheit(temp, unit):
    if unit == 'F' or unit == "wmoUnit:degF":
        temp_f = float(temp)
        temp_c = (temp_f - 32.0) * (5.0 / 9.0)
    else:
        temp_c = float(temp)
        temp_f = (temp_c * (5.0 / 9.0)) + 32.0
    return temp_c, temp_f
