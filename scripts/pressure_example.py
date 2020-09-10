import time
import board
import busio
import adafruit_mprls

# Simplest use, connect to default over I2C
i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

import digitalio
#from digitalio import DigitalInOut, Direction, Pull

reset1 = digitalio.DigitalInOut(board.D10)  #Drive to Ground to reset
reset1.direction = digitalio.Direction.OUTPUT

eoc = digitalio.DigitalInOut(board.D11)  #TRUE when ready
eoc.direction = digitalio.Direction.INPUT
#eoc.pull=digitalio.Pull.DOWN

reset2 = digitalio.DigitalInOut(board.D12)  #Drive to Ground to reset
reset2.direction = digitalio.Direction.OUTPUT

#mpr = adafruit_mprls.MPRLS(i2c, eoc_pin=eoc, reset_pin=reset ,psi_min=0, psi_max=25)

i = 0
reset1.value = False  #Reset 1
reset2.value = False  #Reset 2

while True:
    # Absolute pressure
    reset1.value = False  #Reset the pressure sensor
    time.sleep(0.03)
    #print(f'EOC: {eoc.value}')
    #print(f'Reset: {reset.value}')
    reset1.value = True  #Return to normal
    time.sleep(0.03)

    #while eoc.value == False:  #Only read the sensor when it is ready
    #   i=i+1
    #   print(i)

    hpa1 = mpr.pressure
    print(f'tryck1: {hpa1}')
    bar1 = hpa1 / 1000

    reset1.value = False
    time.sleep(0.03)

    reset2.value = True  #Return to normal
    time.sleep(0.03)

    hpa2 = mpr.pressure
    print(f'tryck2: {hpa2}')
    bar2 = hpa2 / 1000

    reset2.value = False
    time.sleep(0.03)

    # Relative pressure
    relative_bar = bar1 - 1
    mbar1 = relative_bar * 1000

    relative_bar = bar2 - 1
    mbar2 = relative_bar * 1000

    # To print text and variables combined
    print(f'Delta_Milli_Bar: {mbar1-mbar2}')
    #print(f'EOC: {eoc.value}')

    # Put value in a tuple. Parenthesis with values comma separated. One element ends with comma
    print_value = (mbar1, mbar2)
    print(print_value)

    time.sleep(0.01)
