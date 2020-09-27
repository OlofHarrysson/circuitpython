import displayio
import time
import board
import busio
import random
from adafruit_featherwing import minitft_featherwing

from scripts.graphics import GraphicsHandler, make_text, Point
from scripts.pressure import PressureHandler
from scripts.storage import StorageHandler

# TODO: Set the clock to current date. Or get date somehow
# Read, write file. Offset1, 2 and the date

print("START PROGRAM")
spi = board.SPI()
i2c = board.I2C()
minitft = minitft_featherwing.MiniTFTFeatherWing(i2c=i2c, spi=spi)
graphics_handler = GraphicsHandler(minitft)

storage_handler = StorageHandler(spi, i2c)
dp1, dp2 = storage_handler.load_pressure_offsets()
pressure_handler = PressureHandler(i2c, dp1, dp2)

update_frequency = 2  # Frames per second
while True:
    pressures = pressure_handler.measure()
    graphics_handler.draw(pressures)
    buttons = minitft.buttons

    # Calibrate on button press
    if buttons.select or buttons.left or buttons.right or buttons.up or buttons.down:
        graphics_handler.clear_screen()
        text = make_text('Calibrating...', Point(30, 30))
        graphics_handler.add_to_screen([text])
        dp1, dp2 = pressure_handler.calibrate()
        storage_handler.save_pressure_offsets(dp1, dp2)
        time.sleep(2) # Let text stay on display for a while

    time.sleep(1 / update_frequency)