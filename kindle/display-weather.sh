#!/bin/sh

cd "$(dirname "$0")"

rm weather-script-output.png
eips -c
eips -c

if wget http://192.168.2.158/weather-script-output.png; then
	eips -g weather-script-output.png
else
	eips -g weather-image-error.png
fi
