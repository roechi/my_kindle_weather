#!/bin/sh

cd "$(dirname "$0")"

python fetch_weather.py
rsvg-convert --background-color=white -o weather-script-output-pre.png weather-script-output.svg
pngcrush -c 0 weather-script-output-pre.png weather-script-output.png
cp -f weather-script-output.png /var/www/weather-script-output.png
