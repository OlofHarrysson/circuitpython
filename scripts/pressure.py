import random


class MockPressureHandler:
    def __init__(self):
        pass

    def measure(self):
        r = 2.5
        val1 = random.uniform(-r, r)
        val2 = random.uniform(-r, r)

        diff = val1 - val2
        return val1, val2, diff

    def calibrate(self):
        pass
