#!/usr/bin/env python3
import os
import sys
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pathlib


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

    # 1. Initialize the font object first
    font = graphics.Font()

    # 2. Dynamically resolve the absolute font path
    project_folder = pathlib.Path(__file__).parent
    font_folder = project_folder / "fonts"
    font_path = font_folder / "6x10.bdf"

    # 3. Load the font file
    if not font.LoadFont(font_path):
        sys.stderr.write(f"Failed to load font from: {font_path}\n")
        sys.exit(1)

    # Define text colors
    white = graphics.Color(255, 255, 255)
    red = graphics.Color(255, 0, 0)
    green = graphics.Color(0, 255, 0)

    print(
        f"Running text pattern on {width}x{height} matrix. Press Ctrl+C to stop."
    )

    try:
        while True:
            canvas.Clear()

            # Row 1 (Top) - Baseline at Y=12
            graphics.DrawText(canvas, font, 2, 12, white, "ROW 1: ABCD")

            # Row 2 (Middle) - Baseline at Y=26
            graphics.DrawText(canvas, font, 2, 26, red, "ROW 2: 1234")

            # Row 3 (Bottom) - Baseline at Y=40
            graphics.DrawText(canvas, font, 2, 40, green, "ROW 3: EFGH")

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping text pattern. Clearing screen...")
        canvas.Clear()
        matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    run_text_pattern()
