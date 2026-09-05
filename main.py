import os
import threading
import time
import openwec

import config
from engine.drawing import OrientationManager, draw_image
from engine.matrix import RGBMatrix, RUNNING_ON_HARDWARE
from engine.renderer import draw_rows
from engine.state import (
    DISPLAY_MODE,
    SCREEN_BLANKED,
    blank_screen,
    unblank_screen,
    show_pub_image,
    show_psc_image,
)
import engine.state as state
from server import app, run_flask_server
from services.wec_data import build_rows_for_category

CATEGORIES = list(config.class_colours.keys())


def matrix_display_loop():
    options = config.get_matrix_options()
    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()

    orientation_mgr = OrientationManager(matrix, portrait_mode=config.IS_PORTRAIT)
    openwec.configure(api_key=config.api_key)

    try:
        while True:
            if state.DISPLAY_MODE in ("PUB", "PSC", "pub", "psc"):
                mode = state.DISPLAY_MODE.upper()
                image_path = config.PUB_IMAGE_PATH if mode == "PUB" else config.PSC_IMAGE_PATH

                canvas.Clear()
                draw_image(canvas, orientation_mgr, image_path)
                if not RUNNING_ON_HARDWARE:
                    canvas.Show()
                else:
                    canvas = matrix.SwapOnVSync(canvas)

                last_mtime = os.path.getmtime(image_path) if os.path.exists(image_path) else None
                while state.DISPLAY_MODE.upper() == mode:
                    time.sleep(0.1)
                    if os.path.exists(image_path):
                        current_mtime = os.path.getmtime(image_path)
                        if current_mtime != last_mtime:
                            break
                continue

            if state.DISPLAY_MODE == "BLANK" or state.SCREEN_BLANKED:
                canvas.Clear()
                if not RUNNING_ON_HARDWARE:
                    canvas.Show()
                else:
                    canvas = matrix.SwapOnVSync(canvas)

                while state.DISPLAY_MODE == "BLANK" or state.SCREEN_BLANKED:
                    time.sleep(0.1)
                continue

            timestamp = time.strftime('%H:%M:%S')
            print(f"[{timestamp}] Fetching latest WEC session data (3-minute cycle)...")

            session = openwec.Session("WEC", 2026, "Le Mans", "Race")
            results = session.results()
            current_lap = results['laps_completed'].iloc[
                0] if not results.empty and 'laps_completed' in results.columns else 0

            for cat_name in CATEGORIES:
                if state.DISPLAY_MODE != "LIVE" or state.SCREEN_BLANKED:
                    break
                filtered_df = results[results['car_class'] == cat_name]

                top_rows = filtered_df[:config.MAX_CARS]
                car_numbers = top_rows['car_number'].dropna().astype(str).tolist()

                print(f"[{time.strftime('%H:%M:%S')}] Fetching laps & displaying {cat_name}... {car_numbers}")

                rows_data = build_rows_for_category(session=session, car_rows=top_rows, current_lap=current_lap)

                canvas = draw_rows(
                    rows_data=rows_data,
                    duration=config.DISPLAY_DURATION,
                    matrix=matrix,
                    canvas=canvas,
                    orientation_mgr=orientation_mgr
                )

            # Loop through the entire field 4 cars at a time without filtering on car_class
            for i in range(0, len(results), config.MAX_CARS):
                if state.DISPLAY_MODE != "LIVE" or state.SCREEN_BLANKED:
                    break
                field_rows = results.iloc[i:i + config.MAX_CARS]
                car_numbers = field_rows['car_number'].dropna().astype(str).tolist()

                print(f"[{time.strftime('%H:%M:%S')}] Fetching laps & displaying field ({i + 1}-{i + len(field_rows)})... {car_numbers}")

                rows_data = build_rows_for_category(session=session, car_rows=field_rows, current_lap=current_lap)

                canvas = draw_rows(
                    rows_data=rows_data,
                    duration=config.DISPLAY_DURATION,
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
