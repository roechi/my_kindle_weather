import json
import datetime
import codecs
from pprint import pprint
try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import urlopen

def KelvToCels(temp):
    return temp - 273.15

def getJSON(url):
    req = urlopen(url).read()
    return json.loads(req)

city_id = "2950159"; #Berlin
current_api_url = "http://api.openweathermap.org/data/2.5/weather?id=" + city_id;
forecast_api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?id=" + city_id;

current_weather = getJSON(current_api_url)

forecast_weather = getJSON(forecast_api_url)['list'][0]
print('current:\n')
pprint(current_weather)
print('forecast\n')
pprint(forecast_weather)

current_temp = int(round(KelvToCels(current_weather['main']['temp']), 0))
max_temp = int(round(KelvToCels(forecast_weather['temp']['max']), 0))
min_temp = int(round(KelvToCels(forecast_weather['temp']['min']), 0))
icon = forecast_weather['weather'][0]['icon']

output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()
output = output.replace('ICON_ONE', icon)
output = output.replace('CURRENT', str(current_temp))
output = output.replace('DAY', str(min_temp) + "/" + str(max_temp))

codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)

