"""
More info at https://learn.adafruit.com/circuitpython-display-support-using-displayio/text
We didnt get custom fonts to work with the
from adafruit_bitmap_font import bitmap_font
because the board ran out of memory?


"""

import time
import board
import displayio
import terminalio

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

from adafruit_featherwing import minitft_featherwing
minitft = minitft_featherwing.MiniTFTFeatherWing()

display = minitft.display


# Set text, font, and color
text = "HELLO WORLD"
#font = terminalio.FONT
font = bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf")
color = 0xFF00FF


# Create the test label
text_area = label.Label(font, text=text, color=color)

# Set the location
text_area.x = 10
text_area.y = 40

while True:
    # Show it
    display.show(text_area)
    time.sleep(1.03)
    color = 0xFF0000
    text_area.color=color

    display.show(text_area)

    color = 0x0000FF
    text_area.color=color
    #text_area = label.Label(font, text=text, color=color)
    time.sleep(1.03)