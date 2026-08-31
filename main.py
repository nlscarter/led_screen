import openwec

from assets.html import HTML_TEMPLATE
from config import api_key, get_matrix_options, class_colours, IS_PORTRAIT, DISPLAY_DURATION, MAX_CARS
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

CATEGORIES = list(class_colours.keys())

def build_rows_for_category(session, top_rows, current_lap):
    """Pulls laps data for top cars from openwec and builds render objects."""
    rows = [RenderTitle(flag='ROLEX', lap=current_lap)]
    for index, car_row in top_rows.iterrows():
        car_num = str(car_row['car_number'])
        try:
            car_laps = session.laps(car_num)
        except Exception as e:
            print(f"Warning: Failed to fetch laps for car {car_num}: {e}")
            car_laps = None
        rows.append(RenderRow(car_data=car_row, car_laps=car_laps, current_lap=current_lap))
    return rows

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

        time.sleep(1)


import threading
import time
from flask import Flask, request, render_template_string

# --- Global Configurations (Changed Dynamically) ---
MAX_CARS = 3
DISPLAY_DURATION = 10

# --- Initialize Flask App ---
app = Flask(__name__)

@app.route('/')
def index():
    global MAX_CARS, DISPLAY_DURATION
    return render_template_string(HTML_TEMPLATE, max_cars=MAX_CARS, display_duration=DISPLAY_DURATION)


@app.route('/update', methods=['POST'])
def update_config():
    global MAX_CARS, DISPLAY_DURATION
    try:
        MAX_CARS = int(request.form.get('max_cars', MAX_CARS))
        DISPLAY_DURATION = int(request.form.get('display_duration', DISPLAY_DURATION))
        print(f"[*] Configuration Updated -> MAX_CARS: {MAX_CARS}, DURATION: {DISPLAY_DURATION}")
    except ValueError:
        pass
    return render_template_string(HTML_TEMPLATE, max_cars=MAX_CARS, display_duration=DISPLAY_DURATION)


def run_flask_server():
    # Runs the web server on port 5000 accessible to anyone on the local network
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


# --- Your Original Logic Wrapped into a Thread Loop ---
def matrix_display_loop():
    options = get_matrix_options()
    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()

    #if RUNNING_ON_HARDWARE:
    #    canvas = matrix.SwapOnVSync(canvas)
    #    canvas.Clear()

    orientation_mgr = OrientationManager(matrix, portrait_mode=IS_PORTRAIT)
    openwec.configure(api_key=api_key)

    try:
        while True:
            # Notice the references to global variables now execute dynamically inside the loop
            global MAX_CARS, DISPLAY_DURATION

            timestamp = time.strftime('%H:%M:%S')
            print(f"[{timestamp}] Fetching latest WEC session data (3-minute cycle)...")

            session = openwec.Session("WEC", 2026, "Le Mans", "Race")
            results = session.results()
            current_lap = results['laps_completed'].iloc[
                0] if not results.empty and 'laps_completed' in results.columns else 0

            for cat_name in CATEGORIES:
                filtered_df = results[results['car_class'] == cat_name]

                # Dynamic MAX_CARS applied here instantly on the next loop iteration
                top_rows = filtered_df[:MAX_CARS]
                car_numbers = top_rows['car_number'].dropna().astype(str).tolist()

                print(f"[{time.strftime('%H:%M:%S')}] Fetching laps & displaying {cat_name}... {car_numbers}")

                rows_data = build_rows_for_category(session=session, top_rows=top_rows, current_lap=current_lap)

                # Dynamic DISPLAY_DURATION applied here
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


def main():
    # 1. Start the Flask server in the background
    server_thread = threading.Thread(target=run_flask_server, daemon=True)
    server_thread.start()

    # 2. Run the main matrix engine in the foreground
    matrix_display_loop()


if __name__ == "__main__":
    main()
