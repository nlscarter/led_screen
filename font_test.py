#!/usr/bin/env python3
import os
import sys
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pathlib

# Dynamically import the custom font dictionary and logo data
sys.path.append(str(pathlib.Path(__file__).parent / "fonts"))
try:
    from custom_font import FONT_DATA, LOGO_DATA
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


class TelemetryRow:
    """Represents a static row of racing data aligned into columns."""

    def __init__(self, position, team, driver, laps):
        self.position = str(position)
        self.team = str(team)  # Team key matching LOGO_DATA keys (e.g. 'RBR')
        self.driver = str(driver)
        self.laps = str(laps)

    def render(self, canvas, y_pos):
        """Draws the data fields at fixed X offsets, rendering the team as a logo."""
        draw_custom_string(canvas, self.position, start_x=2, start_y=y_pos)

        # Render the graphics-based logo from LOGO_DATA instead of text characters
        draw_team_logo(canvas, self.team, start_x=20, start_y=y_pos)

        # Adjusted driver column offset to accommodate the graphic logo boundaries cleanly
        draw_custom_string(canvas, self.driver, start_x=45, start_y=y_pos)
        draw_custom_string(canvas, self.laps, start_x=80, start_y=y_pos)


def draw_team_logo(canvas, team_key, start_x, start_y):
    """
    Looks up a team asset in LOGO_DATA and renders its 4-bit pixel data array.
    Falls back to rendering the string if the team key cannot be found.
    """
    if team_key not in LOGO_DATA:
        # Graceful fallback: text rendering if logo asset is absent
        draw_custom_string(canvas, team_key, start_x, start_y)
        return

    logo_col_data = LOGO_DATA[team_key]
    logo_width = len(logo_col_data)

    for col_idx in range(logo_width):
        packed_col = logo_col_data[col_idx]
        x = start_x + col_idx

        for row_idx in range(8):
            y = start_y + row_idx

            if y < 0 or y >= canvas.height:
                continue

            # Extract 4-bit value using MSB-first shifts
            shift_amount = 28 - (row_idx * 4)
            pixel_4bit = (packed_col >> shift_amount) & 0x0F

            if pixel_4bit > 0:
                r, g, b = FONT_COLOR_MAP.get(pixel_4bit, (255, 255, 255))
                if 0 <= x < canvas.width:
                    canvas.SetPixel(x, y, r, g, b)


def draw_custom_char(canvas, char, start_x, start_y):
    """Renders a single 5x8 custom 4-bit character on the matrix canvas."""
    if char not in FONT_DATA:
        char = ' '

    if char == ' ':
        return 5

    col_data = FONT_DATA[char]

    for col_idx in range(5):
        packed_col = col_data[col_idx]
        x = start_x + col_idx

        for row_idx in range(8):
            y = start_y + row_idx

            if y < 0 or y >= canvas.height:
                continue

            shift_amount = 28 - (row_idx * 4)
            pixel_4bit = (packed_col >> shift_amount) & 0x0F

            if pixel_4bit > 0:
                r, g, b = FONT_COLOR_MAP.get(pixel_4bit, (255, 255, 255))
                if 0 <= x < canvas.width:
                    canvas.SetPixel(x, y, r, g, b)

    return 5


def draw_custom_string(canvas, text, start_x, start_y, kerning=1):
    """Renders an entire string using the custom 5x8 font."""
    current_x = start_x
    for char in text:
        char_width = draw_custom_char(canvas, char, current_x, start_y)
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
