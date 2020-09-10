import time
import board
import busio
import adafruit_mprls

i2c = busio.I2C(board.SCL, board.SDA)

# Simplest use, connect to default over I2C
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

while True:
    print((mpr.pressure, ))
    time.sleep(1)
