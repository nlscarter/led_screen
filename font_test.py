#!/usr/bin/env python3
import os
import sys
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pathlib

# ==============================================================================
# ORIENTATION TOGGLE
# ==============================================================================
IS_PORTRAIT = True  # Set to True for Portrait (48x96), False for Landscape (96x48)
# ==============================================================================

# Dynamically import the custom font dictionary and logo data
sys.path.append(str(pathlib.Path(__file__).parent / "fonts"))
try:
    from custom_font import BIG_FONT, LOGO_DATA, SMALL_FONT
except ImportError:
    sys.stderr.write("Failed to import FONT_DATA or LOGO_DATA from fonts/custom_font.py\n")
    sys.exit(1)

# Color map translating the 4-bit font value (0-15) to specific RGB tuples
FONT_COLOR_MAP = {
    0: (0, 0, 0),  # Black (Unused/Empty space background)
    1: (255, 0, 0),  # Red
    2: (0, 128, 0),  # Green
    3: (123, 61, 0),  # Brown
    4: (0, 0, 128),  # Dark Blue / Navy
    5: (128, 0, 0),  # Dark Red / Maroon
    6: (187, 227, 61),  # Lime
    7: (50, 50, 50),  # Dark Charcoal / Off-Black
    8: (192, 192, 192),  # Gray
    9: (255, 90, 45),  # Coral / Pinkish Red
    10: (0, 255, 128),  # Light Mint Green
    11: (255, 255, 0),  # Pale Yellow
    12: (30, 30, 255),  # Light Blue / Lavender
    13: (128, 255, 255),  # Light Cyan / Sky Blue
    14: (255, 128, 0),  # Orange
    15: (255, 255, 255),  # White
}


class OrientationManager:
    """Handles layout dimensions and pixel transformations based on rotation state."""

    def __init__(self, matrix, portrait_mode):
        self.matrix = matrix
        self.portrait_mode = portrait_mode

        # Base hardware configurations (assuming a physical 96x48 canvas)
        self.hw_width = 96
        self.hw_height = 48

        # Virtual layout dimensions exposed to drawing functions
        if self.portrait_mode:
            self.width = self.hw_height  # 48
            self.height = self.hw_width  # 96
        else:
            self.width = self.hw_width  # 96
            self.height = self.hw_height  # 48

    def set_pixel(self, canvas, x, y, r, g, b):
        """Maps virtual layout coordinates to physical matrix hardware pixels."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        if self.portrait_mode:
            # FIX: Properly maps coordinates for a 90-degree counter-clockwise rotation
            phys_x = y
            phys_y = x
            canvas.SetPixel(phys_x, phys_y, r, g, b)
        else:
            # Standard direct 1:1 mapping
            canvas.SetPixel(x, y, r, g, b)


class HeaderRow:
    """Heading of page"""

    def __init__(self, status):
        self.status = status

    def render(self, canvas, o_mgr, y_pos):
        char_w, char_h = draw_custom_char(canvas, o_mgr, self.status, start_x=2, start_y=y_pos, font_data=LOGO_DATA)
        return char_h

class Stint:
    def __init__(self, tyre, laps, length =12):
        self.tyre = tyre
        self.laps = laps
        self.complete = laps / length if (laps and length) else 0.0

class Driver:
    def __init__(self, initial, surname, country, stint1:Stint, stint2:Stint, stint3:Stint):
        self.name = f'{initial}.{surname}'
        self.country = country
        self.stint1 = stint1
        self.stint2 = stint2
        self.stint3 = stint3

class Car:
    def __init__(self, number, team, driver:Driver, category, laps, time_delta):
        self.category = category
        self.driver = driver
        self.team = team
        self.laps = laps
        self.time_delta = time_delta
        self.number = number

class Race:
    def __init__(self, status):
        self.time_left = '12:15:36' # change to time object


class Position:
    def __init__(self, num, car: Car):
        self.num = num
        self.car = car
        # Generate the flattened dictionary upon initialization
        self.dict = self.flatten_to_dict()

    def flatten_to_dict(self):
        car = self.car
        driver = car.driver

        return {
            # Position Data
            "position": self.num,

            # Car Data
            "car_number": car.number,
            "team": car.team,
            "category": car.category,
            "car_laps": car.laps,
            "time_delta": car.time_delta,

            # Driver Data
            "driver_name": driver.name,
            "driver_country": driver.country,

            # Stint 1 Data
            "stint1_tyre": driver.stint1.tyre,
            "stint1_laps": driver.stint1.laps,
            "stint1_complete": driver.stint1.complete,

            # Stint 2 Data
            "stint2_tyre": driver.stint2.tyre,
            "stint2_laps": driver.stint2.laps,
            "stint2_complete": driver.stint2.complete,

            # Stint 3 Data
            "stint3_tyre": driver.stint3.tyre,
            "stint3_laps": driver.stint3.laps,
            "stint3_complete": driver.stint3.complete,
        }

soft = "S"
hard = "H"
medium = "M"
position1 = Position(1,
                     Car(34,
                         "BMW",
                         Driver("S",
                                "Panish",
                                "ESP",
                                Stint(soft,12),
                                Stint(medium,8),
                                Stint(None, None)
                                ),
                         category='LMP2',
                         laps=12,
                         time_delta=None
                         )
                     )
positions = [position1]
print(position1.dict)


class TelemetryRow:
    """Represents a static row of racing data aligned into columns."""

    def __init__(self, positions: list[Position]):
        # Extract the flat dictionary from the first position in the list
        self.data = positions[0].dict

    def render(self, canvas, o_mgr, y_pos):
        """Draws data fields sequentially across the X axis, tracking both layout dimensions."""
        current_x = 0
        max_h = 0

        # Column 1: Position (Mapped to flat key "position")
        w1, h1 = draw_custom_string(canvas, o_mgr, str(self.data["position"]), start_x=current_x, start_y=y_pos,
                                    font_data=SMALL_FONT)
        current_x += w1
        max_h = max(max_h, h1)

        # Column 2: Team Logo (Mapped to flat key "team")
        w2, h2 = draw_custom_char(canvas, o_mgr, self.data["team"], start_x=current_x, start_y=y_pos, font_data=LOGO_DATA)
        current_x += w2
        max_h = max(max_h, h2)

        # Column 3: Driver Name (Mapped to flat key "driver_name")
        w3, h3 = draw_custom_string(canvas, o_mgr, self.data["driver_name"], start_x=current_x, start_y=y_pos, font_data=SMALL_FONT)
        current_x += w3
        max_h = max(max_h, h3)

        # Column 4: Laps (Mapped to flat key "car_laps")
        w4, h4 = draw_custom_string(canvas, o_mgr, str(self.data["car_laps"]), start_x=current_x, start_y=y_pos, font_data=SMALL_FONT)
        max_h = max(max_h, h4)

        return max_h


def draw_custom_char(canvas, o_mgr, char, start_x, start_y, font_data):
    """Renders a single variable character using virtual layout dimensions."""
    if char not in font_data:
        char = ' '

    if char == ' ':
        return 5, 8

    col_data = font_data[char]
    char_width = len(col_data)

    for col_idx in range(char_width):
        packed_col = col_data[col_idx]
        x = start_x + col_idx

        if x < 0 or x >= o_mgr.width:
            continue

        temp_col = packed_col
        for row_idx in range(8):
            y = start_y + row_idx
            pixel_4bit = temp_col & 0x0F

            if pixel_4bit > 0 and 0 <= y < o_mgr.height:
                r, g, b = FONT_COLOR_MAP.get(pixel_4bit, (255, 255, 255))
                o_mgr.set_pixel(canvas, x, y, r, g, b)

            temp_col >>= 4

    # Locked: Height is now directly returned as a static value of 8
    return char_width, 8


def draw_custom_string(canvas, o_mgr, text, start_x, start_y, font_data=SMALL_FONT, kerning=1):
    """Renders an entire string, tracking cumulative widths and maximum element heights."""
    current_x = start_x
    max_string_height = 0

    for char in text:
        char_width, char_height = draw_custom_char(canvas, o_mgr, char, current_x, start_y, font_data)
        current_x += char_width + kerning
        if char_height > max_string_height:
            max_string_height = char_height

    total_width = current_x - start_x
    return total_width, max_string_height


def run_text_pattern():
    options = RGBMatrixOptions()
    options.rows = 48
    options.cols = 96
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"
    options.gpio_slowdown = 2
    options.drop_privileges = False

    try:
        matrix = RGBMatrix(options=options)
    except Exception as e:
        sys.stderr.write("Failed to initialize matrix: " + str(e) + "\n")
        sys.exit(1)

    canvas = matrix.CreateFrameCanvas()
    o_mgr = OrientationManager(matrix, portrait_mode=IS_PORTRAIT)

    rows = [
        HeaderRow(status="SC"),
        HeaderRow(status="PORSCHE"),
        HeaderRow(status="BMW"),
        HeaderRow(status="FERRARI"),
        HeaderRow(status="PEUGEOT"),
        HeaderRow(status="ALPINE"),
        HeaderRow(status="MCLAREN"),
        HeaderRow(status="ALPINE"),
        TelemetryRow(positions[0])

    ]

    mode_str = "PORTRAIT (48x96)" if IS_PORTRAIT else "LANDSCAPE (96x48)"
    print(f"Running layout engine in {mode_str} mode. Press Ctrl+C to stop.")

    try:
        while True:
            canvas.Clear()

            current_y = 0
            row_padding = 0  # Spacing between the 8px blocks

            for row in rows:
                row_height = row.render(canvas, o_mgr, y_pos=current_y)
                current_y += row_height + row_padding

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping text pattern. Clearing screen...")
        canvas.Clear()
        matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    run_text_pattern()
