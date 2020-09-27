import board
import busio
import digitalio
import adafruit_sdcard
import storage
import adafruit_pcf8523

class StorageHandler:
    def __init__(self, spi, i2c):
        cs = digitalio.DigitalInOut(board.D10)
        sdcard = adafruit_sdcard.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")

        # The storage unit responsible for time
        self.rtc = adafruit_pcf8523.PCF8523(i2c)

    def write_data(self, data, path):
        with open(path, "w") as f:
            f.write(data)

    def read_data(self, path):
        with open(path) as f:
            return f.read()

    def save_pressure_offsets(self, p1, p2):
        path = "/sd/pressure.txt"
        d = self.rtc.datetime
        date = f'{d.tm_year}-{d.tm_mon}-{d.tm_mday}-{d.tm_hour}-{d.tm_min}-{d.tm_sec}'
        header = 'Pressure-offset-1 Pressure-offset-2 Date'
        data = f'{header}\n{p1} {p2} {date}'
        self.write_data(data, path)

    def load_pressure_offsets(self):
        path = "/sd/pressure.txt"
        file_data = self.read_data(path)
        data = file_data.splitlines()[1].split() # Throw away header
        p1 = float(data[0])
        p2 = float(data[1])
        return p1, p2
