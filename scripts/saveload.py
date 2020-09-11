print("HEHE")

import board
import busio
import digitalio
import adafruit_sdcard
import storage

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D10)

sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)

storage.mount(vfs, "/sd")

# Write data
with open("/sd/test.txt", "w") as f:
    f.write("Hello world! OLOOOFOOLF\r\n")

# Read data
with open("/sd/test.txt", "r") as f:
    print("Read line from file:")
    print(f.readline())
