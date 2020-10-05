import random
import time
import board
import digitalio
import math

import adafruit_mprls
from scripts.graphics import Point

# Points for the optimal pressure
P1 = Point(0.5, -3)  # Top left point. x,y
P2 = Point(12.8, -13.3)  # Bottom right point


class PressureHandler:
    def __init__(self, i2c, pressure_offset_1, pressure_offset_2):
        self.i2c = i2c
        self.pressure_offset_1 = pressure_offset_1
        self.pressure_offset_2 = pressure_offset_2
        self.mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

        self.calibration_points = 20
        self.calibration_delay = 0.01  # In seconds

        # Used to disable one sensor while measuring from the other
        self.sensor1 = digitalio.DigitalInOut(board.D11)
        self.sensor1.direction = digitalio.Direction.OUTPUT

        self.sensor2 = digitalio.DigitalInOut(board.D12)
        self.sensor2.direction = digitalio.Direction.OUTPUT

    def measure(self):
        p1 = self.measure_sensor(self.sensor1)
        p2 = self.measure_sensor(self.sensor2)

        # Add pressure offset
        p1 -= self.pressure_offset_1
        p2 -= self.pressure_offset_2

        diff = shortest_distance(p1, p2)
        return p1, p2, diff

    def measure_sensor(self, sensor):
        ''' Measure the pressure at a sensor '''
        self.sensor1.value = False
        self.sensor2.value = False
        sensor.value = True
        time.sleep(0.01)  # Wait small time before measuring
        mbar = self.mpr.pressure
        return mbar

    def calibrate(self):
        ''' Measure pressure over time that can be used as offsets for measurments in the future '''
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

        return self.pressure_offset_1, self.pressure_offset_2


def shortest_distance(x, y):
    # Calculates the shortest distance to line via https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    numerator = (P2.y - P1.y) * x - (P2.x -
                                     P1.x) * y + P2.x * P1.y - P2.y * P1.x
    numerator = math.fabs(numerator)

    denominator = math.sqrt((P2.y - P1.y)**2 + (P2.x - P1.x)**2)
    distance = numerator / denominator
    return distance
