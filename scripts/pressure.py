import random
import time
import board
import digitalio

import adafruit_mprls


class PressureHandler:
    def __init__(self, i2c):
        self.i2c = i2c
        self.mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

        self.calibration_points = 20
        self.calibration_delay = 0.01  # In seconds

        # Used to disable one sensor while measuring from the other
        self.sensor1 = digitalio.DigitalInOut(board.D11)
        self.sensor1.direction = digitalio.Direction.OUTPUT

        self.sensor2 = digitalio.DigitalInOut(board.D12)
        self.sensor2.direction = digitalio.Direction.OUTPUT

        # Find pressure offsets
        self.calibrate()

    def measure_sensor(self, reset):
        self.sensor1.value = False
        self.sensor2.value = False
        reset.value = True
        time.sleep(0.01)  # Wait small time before measuring
        mbar = self.mpr.pressure
        return mbar

    def measure(self):
        p1 = self.measure_sensor(self.sensor1)
        p2 = self.measure_sensor(self.sensor2)

        # Add pressure offset
        p1 -= self.pressure_offset_1
        p2 -= self.pressure_offset_2

        diff = p1 - p2
        return p1, p2, diff

    def calibrate(self):
        p1s = []
        p2s = []
        for _ in range(self.calibration_points):
            p1 = self.measure_sensor(self.sensor1)
            p2 = self.measure_sensor(self.sensor2)

            p1s.append(p1)
            p2s.append(p2)

            # Wait until next measure point
            time.sleep(self.calibration_delay)

        self.pressure_offset_1 = sum(p1s) / len(p1s)
        self.pressure_offset_2 = sum(p2s) / len(p2s)

