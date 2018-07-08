#!/usr/bin/env python
# coding: utf8

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import requests
import json
from PIL import Image

# Get weather Information

jsonFile = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Dresden,DE&appid=811b454803e4631ae80e51d40248b7e6", timeout=2)
jsonFileContent = jsonFile.text
jsonObject = json.loads(jsonFileContent)

temperature = jsonObject['main']['temp']
humidity = jsonObject['main']['humidity']
sunrise = jsonObject['sys']['sunrise']
sunset = jsonObject['sys']['sunset']
timenow = time.time()

temp = temperature - 273.15


# Configuration for the matrix

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'regular'
options.brightness = 80
options.gpio_slowdown = 2
options.pwm_bits = 8

# Dimm the Brightness during the night

if timenow < sunrise:
	options.brightness = 30
elif timenow > sunset:
	options.brightness = 30

# Initialise Matrix

matrix = RGBMatrix(options = options)
offscreen_canvas = matrix.CreateFrameCanvas()

# Font for time

font3= graphics.Font()
font3.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/8x13B.bdf")

# Font for temp and humidity

font2 = graphics.Font()
font2.LoadFont("/home/pi/LED-Matrix-Clock/fonts/6x9_t.bdf")

textColor = graphics.Color(255, 230, 200)

# Load and set the images for temp and humidity

image1 = Image.open('drop.png')
matrix.SetImage(image1.convert('RGB'), 37, 20)

image2 = Image.open('temp.png')
matrix.SetImage(image2.convert('RGB'), -1, 20)

while True:

    leer = graphics.Color(0, 0, 0)
	
    for y in range (0, 13):
        graphics.DrawLine(offscreen_canvas,0 , y, 64, y, leer)
    graphics.DrawText(offscreen_canvas, font3, 0, 13, textColor, time.strftime("%H:%M:%S", time.localtime()))
    graphics.DrawText(offscreen_canvas, font2, 46, 28, textColor, "{}%".format(str(humidity)))
    graphics.DrawText(offscreen_canvas, font2, 8, 28, textColor, "{:.0f}'".format(temp))
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
