import displayio
import time
import board
import busio
import random

from adafruit_featherwing import minitft_featherwing

from .graphics import GraphicsHandler
from .pressure import MockPressureHandler, PressureHandler

print("START PROGRAM")

i2c = board.I2C()
minitft = minitft_featherwing.MiniTFTFeatherWing(i2c=i2c)
graphics_handler = GraphicsHandler(minitft)
pressure_handler = PressureHandler(i2c)

update_frequency = 2 # Frames per second
while True:
    pressures = pressure_handler.measure()
    graphics_handler.draw(pressures)

    time.sleep(1/update_frequency)
    graphics_handler.clear_screen()

    buttons = minitft.buttons
    if buttons.select or buttons.left or buttons.right or buttons.up or buttons.down:
        pressure_handler.calibrate()

    if buttons.a:
        print("Button A!")
