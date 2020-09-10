"""
This example display a CircuitPython console and
print which button that is being pressed if any
"""

import board
import neopixel

import time


from adafruit_featherwing import minitft_featherwing
minitft = minitft_featherwing.MiniTFTFeatherWing()

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL

# The number of NeoPixels
num_pixels = 1

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

#pixels = neopixel.NeoPixel(
#    pixel_pin, num_pixels, brightness=0.1, auto_write=True, pixel_order=ORDER
#)
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    #pixels.fill((255, 128, 0))
    #pixels.show()
    color = (0, 0, 10)


    buttons = minitft.buttons

    if buttons.right:
        print("Button RIGHT!")

    if buttons.down:
        print("Button DOWN!")

    if buttons.left:
        print("Button LEFT!")

    if buttons.up:
        print("Button UP!")

    if buttons.select:
        print("Button SELECT!")

    if buttons.a:
        print("Button A!")
        color = (0, 10, 0)
        #pixels.fill((128,0,0))

    if buttons.b:
        print("Button B!")

    pixels[0] = color

    time.sleep(0.0001)