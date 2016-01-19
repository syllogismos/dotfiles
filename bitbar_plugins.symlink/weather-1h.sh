#!/bin/bash

# Weather 
# BitBar plugin

curl -s "http://api.openweathermap.org/data/2.5/weather?q=$(curl -s ipinfo.io/city),in&appid=2de143494c0b295cca9337e1e96b00e0&units=metric" | sed -e 's/\(.*\)temp":\([0-9.]*\),\(.*\)/\2/' | awk '{print $1" ℃"}'