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
        table += "<tspan x=\"150\" dy=\"1em\">" + item.str() + "</tspan>\n"
    return table

def buildDepartureTable(departures, name):
    table = "<tspan x=\"150\" dy=\"1em\">" + name + "</tspan>\n" + "<tspan x=\"150\" dy=\"1em\"> </tspan>\n"
    for item in departures:
        if len(item) > 0:
            table += getTable(item)
            table += "<tspan x=\"150\" dy=\"1em\"> </tspan>\n"
    return table

class Station:
    def __init__(self, )

fp = open("config.json")
config = json.load(fp)
config = config["city_id"]
city_id = config["city_id"]

current_api_url = "http://api.openweathermap.org/data/2.5/weather?id=" + city_id;
forecast_api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?id=" + city_id;

current_weather = getJSON(current_api_url)
forecast_weather = getJSON(forecast_api_url)['list'][0]

current_temp = int(round(KelvToCels(current_weather['main']['temp']), 0))
max_temp = int(round(KelvToCels(forecast_weather['temp']['max']), 0))
min_temp = int(round(KelvToCels(forecast_weather['temp']['min']), 0))
icon = forecast_weather['weather'][0]['icon']

stations

#using the BVG grabber api
station_sub_id = "U%20Bismarckstr.%20(Berlin)"
traffic_sub_api_url = "https://bvg-grabber-api.herokuapp.com/actual?station=" + station_sub_id

traffic_sub = getJSON(traffic_sub_api_url)

sub_departures = []

for item in traffic_sub[0][1]:
    sub_departures.append(Departure(item['line'], item['end'], item['remaining']))

u7_rudow_departures = getDepartures(sub_departures, "U7", "U Rudow (Berlin)", 5, 60, 3)
u7_rath_spandau_departures = getDepartures(sub_departures, "U7", "S+U Rathaus Spandau (Berlin)", 5, 60, 3)

u2_pankow_departures = getDepartures(sub_departures, "U2", "U Pankow (Berlin)", 5, 60, 3)
u2_ruhleben_departures = getDepartures(sub_departures, "U2", ["U Ruhleben(Berlin)", "U Olympia-Stadion (Berlin)", "U Theodor-Heuss-Platz (Berlin)"], 5, 60, 3)

bus_bismarck_departures = getDeparturesExcludedByLine(sub_departures, ["U2", "U7"], 5, 60, 3)

station_bus_id = "B%20Haubachstr.%20(Berlin)"
traffic_bus_api_url = "https://bvg-grabber-api.herokuapp.com/actual?station=" + station_bus_id

traffic_bus = getJSON(traffic_bus_api_url)
bus_departures = []

for item in traffic_bus[0][1]:
    bus_departures.append(Departure(item['line'], item['end'], item['remaining']))

tegel_departures = getDepartures(bus_departures,"Bus  109", "Flughafen Tegel Airport", 3, 60, 2);
zoo_departures = getDepartures(bus_departures,"Bus  109", "S+U Zoologischer Garten", 3, 60, 2);
bus_others = getDeparturesExcludedByLine(bus_departures,"Bus  109", 3, 60, 2)

table_sub = buildDepartureTable([u2_pankow_departures, u2_ruhleben_departures, u7_rudow_departures, u7_rath_spandau_departures, bus_bismarck_departures], 'Bismarckstr.')
table_bus = buildDepartureTable([tegel_departures, zoo_departures, bus_others], 'Haubachstr.')

output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()
output = output.replace('ICON_ONE', icon)
output = output.replace('CURRENT', str(current_temp))
output = output.replace('DAY', str(min_temp) + " / " + str(max_temp))

output = output.replace('DEPARTURES', table_sub + table_bus)

codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)

