#!/usr/bin/env python3
import os
import sys
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pathlib

# Dynamically import the custom font dictionary and logo data
sys.path.append(str(pathlib.Path(__file__).parent / "fonts"))
try:
    from custom_font import BIG_FONT, LOGO_DATA, SMALL_FONT
except ImportError:
    sys.stderr.write("Failed to import FONT_DATA or LOGO_DATA from fonts/custom_font.py\n")
    sys.exit(1)

# Color map translating the 4-bit font value (0-15) to specific RGB tuples
FONT_COLOR_MAP = {
    0: (0, 0, 0),  # Transparent / Black
    1: (255, 255, 255),  # White
    2: (255, 0, 0),  # Red
    3: (0, 255, 0),  # Green
    4: (0, 0, 255),  # Blue
    5: (255, 255, 0),  # Yellow
    6: (0, 255, 255),  # Cyan
    7: (255, 0, 255),  # Magenta
    8: (255, 128, 0),  # Orange
    9: (128, 0, 128),  # Purple
    10: (0, 255, 128),  # Mint
    11: (255, 128, 128),  # Light Red / Pink
    12: (128, 255, 128),  # Light Green
    13: (128, 128, 255),  # Light Blue
    14: (192, 192, 192),  # Light Grey
    15: (64, 64, 64),  # Dark Grey
}

class HeaderRow:
    """Heading of page"""
    def __init__(self, status):
        self.status = status
        self.time = "SC"
        self.heading = "FER"

    def render(self, canvas, y_pos):
        # Fixed: Changed draw_team_logo to draw_custom_char and passed LOGO_DATA
        draw_custom_char(canvas, self.status, start_x=1, start_y=y_pos, font_data=LOGO_DATA)
        draw_custom_char(canvas, self.heading, start_x=10, start_y=y_pos, font_data=LOGO_DATA)
        draw_custom_char(canvas, self.time, start_x=20, start_y=y_pos, font_data=LOGO_DATA)

class TelemetryRow:
    """Represents a static row of racing data aligned into columns."""

    def __init__(self, position, team, driver, laps):
        self.position = str(position)
        self.team = str(team)  # Team key matching LOGO_DATA keys (e.g. 'RBR')
        self.driver = str(driver)
        self.laps = str(laps)

    def render(self, canvas, y_pos):
        """Draws the data fields at fixed X offsets, rendering the team as a logo."""
        draw_custom_string(canvas, self.position, start_x=2, start_y=y_pos, font_data=SMALL_FONT)

        # Fixed: Passed self.team instead of the hardcoded "SC" string
        draw_custom_char(canvas, self.team, start_x=20, start_y=y_pos, font_data=LOGO_DATA)

        # Adjusted driver column offset to accommodate the graphic logo boundaries cleanly
        draw_custom_string(canvas, self.driver, start_x=45, start_y=y_pos, font_data=SMALL_FONT)
        draw_custom_string(canvas, self.laps, start_x=80, start_y=y_pos, font_data=SMALL_FONT)

def draw_custom_char(canvas, char, start_x, start_y, font_data):
    """Renders a single variable-width custom character on the matrix canvas using decimal row data."""
    if char not in font_data:
        char = ' '

    # Handle space character width (defaulting to 5 or adapting to font style)
    if char == ' ':
        return 5

    col_data = font_data[char]
    char_width = len(col_data)  # Dynamically determine the width of the character

    for col_idx in range(char_width):
        packed_col = col_data[col_idx]
        x = start_x + col_idx

        # Skip rendering this column if it falls completely off the left/right canvas edges
        if x < 0 or x >= canvas.width:
            continue

        # Extract rows. Since we don't know the exact row height from a single decimal,
        # we loop until the remaining packed bits are exhausted (or standard max height)
        row_idx = 0
        while packed_col > 0:
            y = start_y + row_idx

            # Extract the lowest 4 bits (the active row's pixel value)
            pixel_4bit = packed_col & 0x0F

            if pixel_4bit > 0 and 0 <= y < canvas.height:
                r, g, b = FONT_COLOR_MAP.get(pixel_4bit, (255, 255, 255))
                canvas.SetPixel(x, y, r, g, b)

            # Shift right by 4 bits to process the next row down
            packed_col >>= 4
            row_idx += 1

    return char_width


def draw_custom_string(canvas, text, start_x, start_y, font_data=SMALL_FONT, kerning=1):
    """Renders an entire string using the custom variable width font."""
    current_x = start_x
    for char in text:
        # Fixed: Added the font_data argument here
        char_width = draw_custom_char(canvas, char, current_x, start_y, font_data)
        current_x += char_width + kerning


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
    width = canvas.width
    height = canvas.height

    # Data array with keys corresponding to LOGO_DATA
    rows = [
        HeaderRow(status="RBR"),
        TelemetryRow(position="1", team="RBR", driver="VER", laps="54"),
        TelemetryRow(position="2", team="MCL", driver="NOR", laps="54"),
        TelemetryRow(position="3", team="FER", driver="LEC", laps="53"),
        TelemetryRow(position="4", team="MER", driver="HAM", laps="53"),
        TelemetryRow(position="5", team="FER", driver="ALO", laps="52")
    ]

    print(f"Running static telemetry table with logo graphics on {width}x{height} matrix. Press Ctrl+C to stop.")

    try:
        while True:
            canvas.Clear()

            start_y = 2
            for idx, row in enumerate(rows):
                row.render(canvas, y_pos=start_y + (idx * 9))

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping text pattern. Clearing screen...")
        canvas.Clear()
        matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    run_text_pattern()
