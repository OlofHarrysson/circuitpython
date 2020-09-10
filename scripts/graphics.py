import displayio
import time

from adafruit_display_shapes.rect import Rect
from adafruit_featherwing import minitft_featherwing

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Supports addition. Point + Point or Point + (x, y)
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return Point(self.x + other[0], self.y + other[1])

    def __str__(self):
        return f"Point(x={self.x}, y={self.y})"


# The number of pixels for the display
SCREEN_WIDTH, SCREEN_HEIGHT = 160, 80
TOP_LEFT = Point(0, 0)
TOP_RIGHT = Point(SCREEN_WIDTH, 0)
BOTTOM_LEFT = Point(0, SCREEN_HEIGHT)
BOTTOM_RIGHT = Point(SCREEN_WIDTH, SCREEN_HEIGHT)
BOTTOM_MIDDLE = Point(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT)

# Colors
GREEN = 0x00ff00
PURPLE = 0xFF00FF
BLACK = 0x0
ORANGE = 0xFF8000
BLUE = 0x0080FF
RED = 0xFF0000

# The range for the pressure bar values
BAR_MIN = -5
BAR_MAX = 5

FONT = bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf")

# TODO NOTES
# Save and read from file. Write after calibrate and read on startup

class Bar:
    ''' Graphics that shows the difference in pressure as a bar '''
    def __init__(self, height=15):
        self.height = height

        p1 = BOTTOM_LEFT + (0, -height)
        p2 = BOTTOM_MIDDLE
        self.left = PointRect(p1, p2, fill=0x0, outline=GREEN, stroke=2)

        p1 = BOTTOM_MIDDLE + (0, -height)
        p2 = BOTTOM_RIGHT
        self.right = PointRect(p1, p2, fill=0x0, outline=PURPLE, stroke=2)

    def change_value(self, value):
        # Orange color for normal cases and red otherwise
        color = ORANGE
        if value < BAR_MIN or value > BAR_MAX:
            color = RED

        width = int(value / (abs(BAR_MIN) + BAR_MAX) * SCREEN_WIDTH)
        if value >= 0:
            p1 = BOTTOM_MIDDLE + (0, -self.height)
            p2 = BOTTOM_MIDDLE + (width, 0)
            self.filled = PointRect(p1, p2, fill=color, outline=color)
        else:
            p1 = BOTTOM_MIDDLE + (width, -self.height)
            self.filled = PointRect(p1, BOTTOM_MIDDLE, fill=color, outline=color)


class GraphicsHandler:
    def __init__(self, minitft):
        self.minitft = minitft
        self.display = minitft.display

        # Splash is a collection of drawable objects. You can add/remove from the splash
        self.splash = displayio.Group(max_size=10)
        self.display.show(self.splash)

        self.bar = Bar()
        self.static_graphics = self.make_static_graphics()
        self.add_to_screen(self.static_graphics)

    def draw(self, values):
        dynamic_graphics = self.make_dynamic_graphics(values)
        self.add_to_screen(dynamic_graphics)

        time.sleep(1)  # TODO: Make it stay on screen some other way
        self.clear_screen()

    def add_to_screen(self, graphics):
      for graphic in graphics:
        self.splash.append(graphic)

    def clear_screen(self, only_dynamic=True):
        nbr_to_keep = 0
        if only_dynamic:
          nbr_to_keep = len(self.static_graphics)

        while len(self.splash) > nbr_to_keep:
            self.splash.pop()

    def make_static_graphics(self):
        graphics = []
        graphics.append(self.bar.left)
        graphics.append(self.bar.right)

        # Draw bar range text
        point1 = BOTTOM_LEFT + (0, -25)
        textarea1 = make_text(str(BAR_MIN), point1, color=GREEN)
        graphics.append(textarea1)

        point2 = BOTTOM_RIGHT + (-20, -25)
        textarea2 = make_text(f'+{BAR_MAX}', point2, color=PURPLE)
        graphics.append(textarea2)
        return graphics

    def make_dynamic_graphics(self, values):
        graphics = []

        # Add filled bar
        p1, p2, diff = values
        self.bar.change_value(diff)
        graphics.append(self.bar.filled)

        texts = [
            f"In: {p1:.2f}",
            f"Out: {p2:.2f}",
            f"Diff: {diff:.2f}",
        ]
        points = [
            TOP_LEFT + (0, 10),
            TOP_RIGHT + (-80, 10),
            Point(int(SCREEN_WIDTH / 2) - 40, 30),
        ]
        colors = [BLUE, BLUE, ORANGE]

        # Add texts
        for text, point, color in zip(texts, points, colors):
            textarea = make_text(text, point, color)
            graphics.append(textarea)

        return graphics


def make_text(text, point, color=PURPLE):
    ''' Create drawable text label '''
    text_area = label.Label(FONT, text=text, color=color)

    # Set the location
    text_area.x = point.x
    text_area.y = point.y
    return text_area


def PointRect(p1, p2, fill=BLUE, outline=ORANGE, stroke=2):
    width = p2.x - p1.x
    height = p2.y - p1.y

    # Set minimum height and width to stroke thickness to avoid error
    if width < stroke:
        width = stroke
    if height < stroke:
        height = stroke

    return Rect(p1.x,
                p1.y,
                width,
                height,
                fill=fill,
                outline=outline,
                stroke=stroke)
