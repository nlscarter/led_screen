import sys
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from drawing import draw_custom_char
from fonts.custom_font import LOGO_DATA, FLAG_DATA

IS_PORTRAIT = False  # Set to True for Portrait (48x96), False for Landscape (96x48)


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
            canvas.SetPixel(y, x, r, g, b)
        else:
            canvas.SetPixel(x, y, r, g, b)


class TestRow:
    """Heading of page"""

    def __init__(self, status, country):
        self.status = status
        self.country = country

    def render(self, canvas, o_mgr, y_pos):
        logo_char_w, logo_char_h = draw_custom_char(canvas, o_mgr, self.status, start_x=2, start_y=y_pos, font_data=LOGO_DATA)
        flag_char_w, flag_char_h = draw_custom_char(canvas, o_mgr, self.country, start_x=20, start_y=y_pos, font_data=FLAG_DATA)

        max_char_h = max(flag_char_h, logo_char_h)
        return max_char_h


def run_text_pattern():
    options = RGBMatrixOptions()
    options.rows = 48
    options.cols = 96
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"

    # ─── ANTI-FLICKER & PERFORMANCE OPTIMISATIONS ───
    options.gpio_slowdown = 4  # Higher value handles RPi4 high-speed GPIO timing
    options.drop_privileges = False  # Keep root privileges for hardware timing accuracy
    options.pwm_bits = 11  # Lowers CPU overhead slightly to reduce flicker
    options.brightness = 100  # Caps maximum brightness to reduce power draw/flicker
    options.scan_mode = 0  # 0 = Progressive scan, helps reduce sync flicker

    try:
        matrix = RGBMatrix(options=options)
    except Exception as e:
        sys.stderr.write("Failed to initialize matrix: " + str(e) + "\n")
        sys.exit(1)

    canvas = matrix.CreateFrameCanvas()
    orientation_mgr = OrientationManager(matrix, portrait_mode=IS_PORTRAIT)

    rows = [
        TestRow(status="FERRARI", country="GBR"),
        TestRow(status="ROL", country="JAP"),
        TestRow(status="BMW", country="ITY"),
        TestRow(status="COLOUR1", country="JAP"),
    ]

    mode_str = "PORTRAIT (48x96)" if IS_PORTRAIT else "LANDSCAPE (96x48)"
    print(f"Running layout engine in {mode_str} mode. Press Ctrl+C to stop.")

    try:
        while True:
            canvas.Clear()

            current_y = 8
            row_padding = 0

            for row in rows:
                row_height = row.render(canvas, orientation_mgr, y_pos=current_y)
                current_y += row_height + row_padding

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping text pattern. Clearing screen...")
        canvas.Clear()
        matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    run_text_pattern()