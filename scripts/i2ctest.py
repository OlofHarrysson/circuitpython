
print("START")
import time
import board
import busio
import adafruit_mprls
import displayio
from adafruit_featherwing import minitft_featherwing

from .graphics import Bar

# sensor, display
#addresses = ['0x18', '0x5e']

# Simplest use, connect to default over I2C
i2c = board.I2C()
i2c.unlock()
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)
minitft = minitft_featherwing.MiniTFTFeatherWing(i2c=i2c)

display = minitft.display
splash = displayio.Group(max_size=10)
display.show(splash)
bar = Bar()
splash.append(bar.left)

# Loops until i2c is locked
print("LOCKING")
#while not i2c.try_lock():
#    pass
print("DONE LOCKING")

#i2c.unlock()
while True:
    print((mpr.pressure, ))
    time.sleep(1)

try:
    while True:
        print("I2C addresses found:",
              [hex(device_address) for device_address in i2c.scan()])
        time.sleep(2)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()
