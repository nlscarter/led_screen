import time
import openwec

from config import api_key, get_matrix_options
from engine.drawing import DummyCanvas, OrientationManager
from view.render_row import RenderRow
from view.render_title import RenderTitle

# ─── ENVIRONMENT DETECTOR & MOCK INTERFACE ───
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

    RUNNING_ON_HARDWARE = True
except ImportError:
    RUNNING_ON_HARDWARE = False

    class RGBMatrixOptions:
        pass

    class RGBMatrix:
        def __init__(self, options=None):
            pass

        def CreateFrameCanvas(self):
            return DummyCanvas()

        def SwapOnVSync(self, canvas):
            canvas.Show()
            return canvas
# ──────────────────────────────────────────────

IS_PORTRAIT = False  # Set to True for Portrait (48x96), False for Landscape (96x48)
DATA_FETCH_INTERVAL = 180  # Fetch fresh data every 3 minutes (180s)
CATEGORIES = ["HYPERCAR", "LMP2", "LMGT3"]
DISPLAY_DURATION = 5  # 60s per category
MAX_CARS = 4


def build_rows_for_category(session, car_numbers):
    """Builds the header and row objects for a specific race category."""
    rows = [RenderTitle(flag='ROLEX', session=session)]
    for car_num in car_numbers:
        rows.append(RenderRow(num=car_num, session=session))
    return rows


def main():
    options = get_matrix_options()
    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()

    if RUNNING_ON_HARDWARE:
        canvas = matrix.SwapOnVSync(canvas)
        canvas.Clear()

    orientation_mgr = OrientationManager(matrix, portrait_mode=IS_PORTRAIT)
    openwec.configure(api_key=api_key)

    try:
        while True:
            timestamp = time.strftime('%H:%M:%S')
            print(f"[{timestamp}] Fetching latest WEC session data (3-minute cycle)...")
            session = openwec.Session("WEC", 2026, "Le Mans", "Race")
            results = session.results()

            # Run pattern 3 times across the 3 categories
            for cat_name in CATEGORIES:
                filtered_df = results[results['car_class'] == cat_name]
                top_rows = filtered_df[:MAX_CARS]
                car_numbers = top_rows['car_number'].dropna().astype(str).tolist()

                print(f"[{time.strftime('%H:%M:%S')}] Displaying {cat_name}... {car_numbers}")
                
                rows_data = build_rows_for_category(session, car_numbers=car_numbers)
                
                run_text_pattern(
                    rows_data=rows_data,
                    duration=DISPLAY_DURATION,
                    matrix=matrix,
                    canvas=canvas,
                    orientation_mgr=orientation_mgr
                )

    except KeyboardInterrupt:
        print("\nStopping display loop. Clearing screen...")
        canvas.Clear()
        if RUNNING_ON_HARDWARE:
            matrix.SwapOnVSync(canvas)



def run_text_pattern(rows_data, duration=DISPLAY_DURATION, matrix=None, canvas=None, orientation_mgr=None):
    """Renders rows to the matrix or dummy canvas for the specified duration (seconds)."""
    if matrix is None:
        options = get_matrix_options()
        matrix = RGBMatrix(options=options)
    if canvas is None:
        canvas = matrix.CreateFrameCanvas()
    if orientation_mgr is None:
        orientation_mgr = OrientationManager(matrix, portrait_mode=IS_PORTRAIT)

    start_time = time.time()
    while time.time() - start_time < duration:
        canvas.Clear()

        current_y = 7
        row_padding = 0

        # Execute render logic across rows
        for row in rows_data:
            height_used = row.render(canvas, orientation_mgr, current_y)
            current_y += height_used + row_padding

        if not RUNNING_ON_HARDWARE:
            canvas.Show()
        else:
            canvas = matrix.SwapOnVSync(canvas)

        time.sleep(0.2)

if __name__ == "__main__":
    main()
