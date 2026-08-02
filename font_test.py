#!/usr/bin/env python3
import os
import sys
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pathlib

# Dynamically import the custom font dictionary
sys.path.append(str(pathlib.Path(__file__).parent / "fonts"))
try:
    from custom_font import FONT_DATA
except ImportError:
    sys.stderr.write("Failed to import FONT_DATA from fonts/custom_font.py\n")
    sys.exit(1)


def draw_custom_char(canvas, char, start_x, start_y, base_color):
    """
    Renders a single 5x8 custom 4-bit character on the matrix canvas.
    A character is a list of 5 integers, each packing 8 rows of 4-bit colour values.
    """
    if char not in FONT_DATA:
        char = ' '  # Fallback to a space if character is missing

    if char == ' ':
        return 5  # Width of a space character

    col_data = FONT_DATA[char]

    for col_idx in range(5):
        packed_col = col_data[col_idx]
        x = start_x + col_idx

        # Draw all 8 rows for this column
        for row_idx in range(8):
            y = start_y + row_idx

            # Skip drawing if the pixel goes out of vertical bounds
            if y < 0 or y >= canvas.height:
                continue

            # Extract 4-bit value using MSB-first shifts (Row 0 is bits 31-28)
            shift_amount = 28 - (row_idx * 4)
            pixel_4bit = (packed_col >> shift_amount) & 0x0F

            if pixel_4bit > 0:
                # Scale the base color by the 4-bit brightness multiplier (0 to 1)
                brightness = pixel_4bit / 15.0
                r = int(base_color[0] * brightness)
                g = int(base_color[1] * brightness)
                b = int(base_color[2] * brightness)

                # Draw the pixel only if it is horizontally within screen limits
                if 0 <= x < canvas.width:
                    canvas.SetPixel(x, y, r, g, b)

    return 5  # Return character width


def draw_custom_string(canvas, text, start_x, start_y, color, kerning=1):
    """Renders an entire string using the custom 5x8 font."""
    current_x = start_x
    for char in text:
        char_width = draw_custom_char(canvas, char, current_x, start_y, color)
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

    # Define RGB tuples instead of graphics.Color objects for easier manipulation
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

    row1_str = "ROW 1: ABCD"
    row2_str = "ROW 2: 1234"
    row3_str = "ROW 3: EFGH"

    scroll_x = width

    # Custom font metrics (5px width + 1px spacing spacing = 6px total footprint)
    char_width = 5
    kerning = 1
    total_char_footprint = char_width + kerning

    max_text_length = max(len(row1_str), len(row2_str), len(row3_str))
    text_width_pixels = max_text_length * total_char_footprint

    print(
        f"Running scrolling custom font pattern on {width}x{height} matrix. Press Ctrl+C to stop."
    )

    try:
        while True:
            canvas.Clear()

            # Note: Top-left rendering means Y coordinates are the top of the characters,
            # instead of the font baseline coordinates used by BDF rendering.
            # Row 1 (Top) - Top edge at Y=4
            draw_custom_string(canvas, row1_str, scroll_x, 4, white, kerning)

            # Row 2 (Middle) - Top edge at Y=18
            draw_custom_string(canvas, row2_str, scroll_x, 18, red, kerning)

            # Row 3 (Bottom) - Top edge at Y=32
            draw_custom_string(canvas, row3_str, scroll_x, 32, green, kerning)

            scroll_x -= 1

            if scroll_x < -text_width_pixels:
                scroll_x = width

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.03)

    except KeyboardInterrupt:
        print("\nStopping text pattern. Clearing screen...")
        canvas.Clear()
        matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    run_text_pattern()