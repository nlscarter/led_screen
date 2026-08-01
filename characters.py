#!/usr/bin/env python3
import sys
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


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

    # Load 8px high font (Make sure this path points to your actual font file)
    font = graphics.Font()
    font_path = "./fonts/6x10.bdf"  # 10px bounding box, but characters are ~8px high
    # Alternative: Use "clshack.bdf" or "tom-thumb.bdf" (5x5) if you want even smaller
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

            # Row 1: Y-coordinate represents the baseline of the text
            # For 8-10px fonts, a baseline at Y=10 works perfectly
            graphics.DrawText(canvas, font, 2, 10, white, "ROW 1: ABCD")

            # Row 2: Spaced down by ~12-14 pixels
            graphics.DrawText(canvas, font, 2, 24, red, "ROW 2: 1234")

            # Row 3
            graphics.DrawText(canvas, font, 2, 38, green, "ROW 3: EFGH")

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping test pattern. Clearing screen...")
        canvas.Clear()
        matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    run_text_pattern()
