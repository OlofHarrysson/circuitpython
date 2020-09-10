import random
import time


class MockPressureHandler:
    def __init__(self):
        self.calibration_points = 5
        self.calibration_delay = 0.01  # In seconds

        # Find pressure offsets
        self.calibrate()

    def measure(self):
        r = 5
        val1 = random.uniform(0, r)
        val2 = random.uniform(0, r)

        # Add pressure offset
        val1 -= self.pressure_offset_1
        val2 -= self.pressure_offset_2

        diff = val1 - val2
        return val1, val2, diff

    def calibrate(self):
        print("CALIBRATING")
        p1s = []
        p2s = []
        r = 2.5
        for _ in range(self.calibration_points):
            p1 = random.uniform(0, r)
            p2 = random.uniform(0, r)
            
            p1s.append(p1)
            p2s.append(p2)

            # Wait until next measure point
            time.sleep(self.calibration_delay)

        p1_offset = sum(p1s) / len(p1s)
        p2_offset = sum(p2s) / len(p2s)
        print("Pressure offset", p1_offset, p2_offset)
        
        self.pressure_offset_1 = p1_offset
        self.pressure_offset_2 = p2_offset
