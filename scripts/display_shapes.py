import displayio
import time
import board
import busio
import random

from adafruit_featherwing import minitft_featherwing
from .graphics import Bar, GraphicsHandler
from .pressure import MockPressureHandler

print("START PROGRAM")

minitft = minitft_featherwing.MiniTFTFeatherWing()
graphics_handler = GraphicsHandler(minitft)
pressure_handler = MockPressureHandler()

# graphics_handler.draw_static()

while True:
    pressures = pressure_handler.measure()
    graphics_handler.draw(pressures)

    buttons = minitft.buttons
    if buttons.left:
        print("Button LEFT!")
        pressure_handler.calibrate()

    if buttons.a:
        print("Button A!")
