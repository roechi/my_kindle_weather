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

class Departure:
    def __init__(self, line, end, remaining):
        self.line = line
        self.end = end
        self.remaining = remaining
    def str(self):
        return self.line + " " + self.end + " in " + str(self.remaining / 60) + " Min."

def getDepartures(departures, line, end, min_time, max_time, max_list_length):
    dep_list = []
    for item in departures:
        if len(dep_list) < max_list_length:
            if (line == item.line) and (item.end in end) and (min_time <= (item.remaining / 60)) and ((item.remaining / 60) <= max_time):
                dep_list.append(item)
    return dep_list  

def getDeparturesExcludedByLine(departures, lines, min_time, max_time, max_list_length):
    dep_list = []
    for item in departures:
        if len(dep_list) < max_list_length:
            if (item.line not in lines) and (min_time <= (item.remaining / 60)) and ((item.remaining / 60) <= max_time):
                dep_list.append(item)
    return dep_list 

def getTable(departures):
    table = ""
    for item in departures:
        table += "<tspan x=\"10\" dy=\"1em\">" + item.str() + "</tspan>\n"
    return table

def buildDepartureTable(departures, name):
    table = "<tspan x=\"10\" dy=\"1em\">" + name + "</tspan>\n"
    for item in departures:
        if len(item) > 0:
            table += getTable(item)
            table += "<tspan x=\"10\" dy=\"1em\"> </tspan>\n"
    return table

# using the openweathermap api
city_id = "2950159"; #Berlin
current_api_url = "http://api.openweathermap.org/data/2.5/weather?id=" + city_id;
forecast_api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?id=" + city_id;

current_weather = getJSON(current_api_url)

forecast_weather = getJSON(forecast_api_url)['list'][0]
# print('current:\n')
# pprint(current_weather)
# print('forecast\n')
# pprint(forecast_weather)

current_temp = int(round(KelvToCels(current_weather['main']['temp']), 0))
max_temp = int(round(KelvToCels(forecast_weather['temp']['max']), 0))
min_temp = int(round(KelvToCels(forecast_weather['temp']['min']), 0))
icon = forecast_weather['weather'][0]['icon']

#using the BVG grabber api
station_sub_id = "U%20Bismarckstr.%20(Berlin)"
traffic_sub_api_url = "https://bvg-grabber-api.herokuapp.com/actual?station=" + station_sub_id

traffic_sub = getJSON(traffic_sub_api_url)

# print("Sub Traffic:\n")
# pprint(traffic_sub)

sub_departures = []

for item in traffic_sub[0][1]:
    sub_departures.append(Departure(item['line'], item['end'], item['remaining']))

u7_rudow_departures = getDepartures(sub_departures, "U7", "U Rudow (Berlin)", 5, 60, 5)
u7_rath_spandau_departures = getDepartures(sub_departures, "U7", "S+U Rathaus Spandau (Berlin)", 5, 60, 5)

u2_pankow_departures = getDepartures(sub_departures, "U2", "U Pankow (Berlin)", 5, 60, 5)
u2_ruhleben_departures = getDepartures(sub_departures, "U2", ["U Ruhleben(Berlin)", "U Olympia-Stadion (Berlin)", "U Theodor-Heuss-Platz (Berlin)"], 5, 60, 5)

bus_bismarck_departures = getDeparturesExcludedByLine(sub_departures, ["U2", "U7"], 5, 60, 5)

print(getTable(u7_rath_spandau_departures))

station_bus_id = "B%20Haubachstr.%20(Berlin)"
traffic_bus_api_url = "https://bvg-grabber-api.herokuapp.com/actual?station=" + station_bus_id

traffic_bus = getJSON(traffic_bus_api_url)

# print("Bus Traffic:\n")
# pprint(traffic_bus)

# for item in traffic_bus[0][1]:
    # print(item['line'] + " " + item['end'] + " in " + str(item['remaining'] / 60) + " Min.")



output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()
output = output.replace('ICON_ONE', icon)
output = output.replace('CURRENT', str(current_temp))
output = output.replace('DAY', str(min_temp) + "/" + str(max_temp))

output = output.replace('U2_RUHLEBEN', buildDepartureTable([u2_pankow_departures, u2_ruhleben_departures, u7_rudow_departures, u7_rath_spandau_departures, bus_bismarck_departures], 'Bismarckstr.'))

codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)

