import sys
import time
from drawing import draw_custom_char, draw_custom_string
from fonts.custom_font import LOGO_DATA, FLAG_DATA, font_5x9, font_4x7, class_lines
from example_data import mock_json


# ─── MOCKING ENVIRONMENT FOR LOCAL LAPTOP TESTING ───
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    RUNNING_ON_HARDWARE = True
except ImportError:
    print("'rgbmatrix' not found. Running in Laptop Dummy/Mock mode.")
    RUNNING_ON_HARDWARE = False

    class RGBMatrixOptions:
        def __init__(self):
            pass

    class DummyCanvas:
        def Clear(self):
            pass
        def SetPixel(self, x, y, r, g, b):
            # Optional: Print pixels to console if you want to see coordinates
            # print(f"Pixel set at ({x}, {y}) with color RGB({r},{g},{b})")
            pass

    class RGBMatrix:
        def __init__(self, options=None):
            print("Initialised Mock LED Matrix.")
        def CreateFrameCanvas(self):
            return DummyCanvas()
        def SwapOnVSync(self, canvas):
            return canvas

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


class RenderRow:
    """Heading of page"""

    def __init__(self, status, country, category):
        self.status = status
        self.country = country
        self.category = category

    def render(self, canvas, o_mgr, y_pos):
        logo_char_w, logo_char_h = draw_custom_char(canvas, o_mgr, self.status, start_x=2, start_y=y_pos, font_data=LOGO_DATA)
        flag_char_w, flag_char_h = draw_custom_char(canvas, o_mgr, self.country, start_x=20, start_y=y_pos, font_data=FLAG_DATA)
        draw_custom_string(canvas, o_mgr, "Test!", start_x=40, start_y=y_pos-2, font_data=font_4x7)
        draw_custom_char(canvas, o_mgr, self.category, start_x=40, start_y=y_pos, font_data=class_lines)
        draw_custom_string(canvas, o_mgr, "P1", start_x=80, start_y=y_pos, font_data=font_5x9)

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

    data = mock_json


    rows = [
        RenderRow(status="FERRARI", country="GBR", category='LMP1'),
        RenderRow(status="PORSCHE", country="JAP", category='LMP2'),
        RenderRow(status="BMW", country="ITY", category='LMGT'),
        RenderRow(status="COLOUR1", country="JAP", category='LMP1'),
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