print("HEHE")

import time

import board
import digitalio
import microcontroller

led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()
# TODO: Also need to wire ground to the pin
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage

try:
    print("HERE")
    with open("/temperature.txt", "w") as fp:
        print("HEREasdas")
        for i in range(10):
            print("printing")
            temp = microcontroller.cpu.temperature
            # do the C-to-F conversion here if you would like
            fp.write('{0:f}\n'.format(temp))
            fp.flush()
            led.value = not led.value
            time.sleep(1)
except OSError as e:
    delay = 0.5
    if e.args[0] == 28:
        delay = 0.25
    for i in range(5):
        print("FAILING")
        led.value = not led.value
        time.sleep(delay)



