import sys
import time
from drawing import draw_custom_char, draw_custom_string
from fonts.custom_font import LOGO_DATA, FLAG_DATA, font_5x9, font_4x7, class_lines
from example_data import mock_json

# ─── ENVIRONMENT DETECTOR & MOCK INTERFACE ───
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

    RUNNING_ON_HARDWARE = True
except ImportError:
    RUNNING_ON_HARDWARE = False


    class RGBMatrixOptions:
        pass


    class DummyCanvas:
        def Clear(self):
            pass

        def SetPixel(self, x, y, r, g, b):
            # Optional: uncomment to see every individual pixel draw instruction
            print(f"  -> SetPixel({x}, {y}) RGB({r},{g},{b})")
            pass


    class RGBMatrix:
        def __init__(self, options=None):
            pass

        def CreateFrameCanvas(self):
            return DummyCanvas()

        def SwapOnVSync(self, canvas):
            return canvas
# ──────────────────────────────────────────────

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
        logo_char_w, logo_char_h = draw_custom_char(canvas, o_mgr, self.status, start_x=2, start_y=y_pos,
                                                    font_data=LOGO_DATA)
        flag_char_w, flag_char_h = draw_custom_char(canvas, o_mgr, self.country, start_x=20, start_y=y_pos,
                                                    font_data=FLAG_DATA)
        draw_custom_string(canvas, o_mgr, "Test!", start_x=40, start_y=y_pos - 2, font_data=font_4x7)
        draw_custom_char(canvas, o_mgr, self.category, start_x=40, start_y=y_pos, font_data=class_lines)
        draw_custom_string(canvas, o_mgr, "P1", start_x=80, start_y=y_pos, font_data=font_5x9)

        max_char_h = max(flag_char_h, logo_char_h)
        return max_char_h


def run_text_pattern():
    options = RGBMatrixOptions()
    if RUNNING_ON_HARDWARE:
        options.rows = 48
        options.cols = 96
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "regular"
        options.gpio_slowdown = 4
        options.drop_privileges = False
        options.pwm_bits = 11
        options.brightness = 100
        options.scan_mode = 0

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

    if RUNNING_ON_HARDWARE:
        print(f"Running layout engine on HARDWARE in {mode_str} mode. Press Ctrl+C to stop.")
    else:
        print(f"🖥️  Running layout engine on LAPTOP in {mode_str} mode (Console Mock Output).\n")

    try:
        while True:
            canvas.Clear()

            current_y = 8
            row_padding = 0

            # ─── CONSOLE PRINT LOGIC FOR LAPTOP TESTING ───
            if not RUNNING_ON_HARDWARE:
                print("=" * 60)
                print(f" LAYOUT ENGINE MATRIX RENDERING REPORT (Canvas Width: {orientation_mgr.width}px)")
                print("=" * 60)

            for i, row in enumerate(rows):
                row_height = row.render(canvas, orientation_mgr, y_pos=current_y)

                if not RUNNING_ON_HARDWARE:
                    print(
                        f"Row {i + 1} | Status: {row.status:<8} | Country: {row.country:<4} | Category: {row.category:<5}")
                    print(f"      ↳ Rendered at Y-Position: {current_y} | Computed Row Height: {row_height}px")
                    print("-" * 60)

                current_y += row_height + row_padding

            if not RUNNING_ON_HARDWARE:
                print(f"Total canvas height used: {current_y}px / Max allowed: {orientation_mgr.height}px")
                print("=" * 60 + "\n")
                break  # Stops the infinite loop when testing locally on your laptop
            # ──────────────────────────────────────────────

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping text pattern. Clearing screen...")
        canvas.Clear()
        matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    run_text_pattern()
