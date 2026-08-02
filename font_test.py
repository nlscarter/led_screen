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


class TelemetryRow:
    """Represents a static row of racing data aligned into columns."""

    def __init__(self, position, team, driver, laps):
        self.position = str(position)
        self.team = str(team)
        self.driver = str(driver)
        self.laps = str(laps)

    def render(self, canvas, o_mgr, y_pos):
        """Draws data fields sequentially across the X axis, tracking both layout dimensions."""
        current_x = 2
        col_padding = 4 if o_mgr.portrait_mode else 10  # Cinch columns closer if screen is narrow
        max_h = 0

        # Column 1: Position
        w1, h1 = draw_custom_string(canvas, o_mgr, self.position, start_x=current_x, start_y=y_pos,
                                    font_data=SMALL_FONT)
        current_x += w1 + col_padding
        max_h = max(max_h, h1)

        # Column 2: Team Logo
        w2, h2 = draw_custom_char(canvas, o_mgr, self.team, start_x=current_x, start_y=y_pos, font_data=LOGO_DATA)
        current_x += w2 + col_padding
        max_h = max(max_h, h2)

        # Column 3: Driver Name
        w3, h3 = draw_custom_string(canvas, o_mgr, self.driver, start_x=current_x, start_y=y_pos, font_data=SMALL_FONT)
        current_x += w3 + col_padding
        max_h = max(max_h, h3)

        # Column 4: Laps
        w4, h4 = draw_custom_string(canvas, o_mgr, self.laps, start_x=current_x, start_y=y_pos, font_data=SMALL_FONT)
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
        HeaderRow(status="COLOUR1"),
        HeaderRow(status="PORSCHE"),
        HeaderRow(status="RAINBOW"),
        HeaderRow(status="SC"),
        HeaderRow(status="BMW"),
        HeaderRow(status="FERRARI"),
        HeaderRow(status="PEUGEOT"),

    ]

    mode_str = "PORTRAIT (48x96)" if IS_PORTRAIT else "LANDSCAPE (96x48)"
    print(f"Running layout engine in {mode_str} mode. Press Ctrl+C to stop.")

    try:
        while True:
            canvas.Clear()

            current_y = 0
            row_padding = 1  # Spacing between the 8px blocks

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
