#!/usr/bin/env python3
import time
import math
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from config import led_rows, led_cols


def run_test_pattern():
    options = RGBMatrixOptions()
    options.rows = led_rows
    options.cols = led_cols
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

    CANVAS = matrix.CreateFrameCanvas()
    width = CANVAS.width
    height = CANVAS.height

    print("Running test pattern on " + str(width) + "x" + str(height) + " matrix. Press Ctrl+C to stop.")

    offset = 0
    try:
        while True:
            CANVAS.Clear()
            for x in range(width):
                for y in range(height):
                    r = int((math.sin(x / 8.0 + offset) + 1.0) * 127.5)
                    g = int((math.sin(y / 6.0 + offset + 2.0) + 1.0) * 127.5)
                    b = int((math.sin((x + y) / 10.0 + offset + 4.0) + 1.0) * 127.5)
                    CANVAS.SetPixel(x, y, r, g, b)

            CANVAS = matrix.SwapOnVSync(CANVAS)
            offset += 0.05
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nStopping test pattern. Clearing screen...")
        CANVAS.Clear()
        matrix.SwapOnVSync(CANVAS)


if __name__ == "__main__":
    run_test_pattern()
