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

sunrise = jsonObject['sys']['sunrise']
sunset = jsonObject['sys']['sunset']
timenow = time.time()

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

offscreen_canvas = matrix.CreateFrameCanvas()

pos= 64

font1 = graphics.Font()
font1.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")
font = graphics.Font()
font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")
textColor = graphics.Color(255, 230, 200)
textColor1 = graphics.Color(200, 200, 200)

try:
        seite = ('http://widgets.vvo-online.de/abfahrtsmonitor/Abfahrten.do?hst=lisztstrasse&vz=7&ort=Dresden&vm=Straßenbahn&lim=3&timestamp=0')
        a = requests.get(seite, timeout=300)
        b = a.text
        c = b.replace("[", "")
        b = c.replace("]", "")
        c = b.replace('"', "")
        abfahrt = c.split(",")
        ziel0 = len(abfahrt[1])
        ziel1 = len(abfahrt[4])
        ziel2 = len(abfahrt[7])
except requests.exceptions.ConnectionError:
        abfahrt = abfahrt

while True:
       
        offscreen_canvas.Clear()
        leng = offscreen_canvas.width

        graphics.DrawText(offscreen_canvas, font1, 0, 5, textColor1, "LINIE")
        graphics.DrawText(offscreen_canvas, font1, 53, 5, textColor, "MIN")

        leer = graphics.Color(0, 0, 0)

        if (ziel0 > 9):
                graphics.DrawText(offscreen_canvas, font, pos, 14, textColor1, abfahrt[1])

        else:
                graphics.DrawText(offscreen_canvas, font, 12, 14, textColor1, abfahrt[1])

        if (ziel1 > 9):
                graphics.DrawText(offscreen_canvas, font, pos, 22, textColor1, abfahrt[4])

        else:
                graphics.DrawText(offscreen_canvas, font, 12, 22, textColor1, abfahrt[4])

        if (ziel2 > 9):
                graphics.DrawText(offscreen_canvas, font, pos, 30, textColor1, abfahrt[7])

        else:
                graphics.DrawText(offscreen_canvas, font, 12, 30, textColor1, abfahrt[7])

        pos = pos-1
        if (pos + leng < 0):
                pos = offscreen_canvas.width

        for y in range(7, 32):
                graphics.DrawLine(offscreen_canvas, 51, y, 64, y, leer)
                graphics.DrawText(offscreen_canvas, font, 53, 14, textColor, abfahrt[2])
                graphics.DrawText(offscreen_canvas, font, 53, 22, textColor, abfahrt[5])
                graphics.DrawText(offscreen_canvas, font, 53, 30, textColor, abfahrt[8])

        for y in range(7, 32):
                graphics.DrawLine(offscreen_canvas, 0, y, 11, y, leer)
        graphics.DrawText(offscreen_canvas, font, 0, 14, textColor1, abfahrt[0])
        graphics.DrawText(offscreen_canvas, font, 0, 22, textColor1, abfahrt[3])
        graphics.DrawText(offscreen_canvas, font, 0, 30, textColor1, abfahrt[6])
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
