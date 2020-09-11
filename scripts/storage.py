import board
import busio
import digitalio
import adafruit_sdcard
import storage


class StorageHandler:
    def __init__(self, spi):
        cs = digitalio.DigitalInOut(board.D10)
        sdcard = adafruit_sdcard.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")

    def write_data(self, data, path):
        with open(path, "w") as f:
            print("Writing to file:", path)
            f.write(data)

    def read_data(self, path):
        with open(path) as f:
            print("Read line from file:", path)
            print(f.readline())
