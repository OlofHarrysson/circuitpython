import displayio
import time
import board
import busio
import random

from adafruit_featherwing import minitft_featherwing

from .graphics import GraphicsHandler
from .pressure import MockPressureHandler, PressureHandler
from .storage import StorageHandler

print("START PROGRAM")

spi = board.SPI()
i2c = board.I2C()
minitft = minitft_featherwing.MiniTFTFeatherWing(i2c=i2c, spi=spi)
graphics_handler = GraphicsHandler(minitft)
pressure_handler = PressureHandler(i2c)
storage_handler = StorageHandler(spi)

data = "YOYOYOYO OLOF\r\n"
path = "/sd/test.txt"
storage_handler.write_data(data, path)
storage_handler.read_data(path)

update_frequency = 2  # Frames per second
while True:
    pressures = pressure_handler.measure()
    graphics_handler.draw(pressures)

    time.sleep(1 / update_frequency)
    graphics_handler.clear_screen()

    buttons = minitft.buttons
    if buttons.select or buttons.left or buttons.right or buttons.up or buttons.down:
        pressure_handler.calibrate()

    if buttons.a:
        print("Button A!")
