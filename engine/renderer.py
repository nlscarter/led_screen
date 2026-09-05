import time

import config
from engine.drawing import OrientationManager
from engine.matrix import RGBMatrix, RUNNING_ON_HARDWARE
import engine.state as state


def draw_rows(rows_data, duration=None, matrix=None, canvas=None, orientation_mgr=None):
    """Renders rows to the matrix or dummy canvas for the specified duration (seconds)."""
    if duration is None:
        duration = config.DISPLAY_DURATION

    if matrix is None:
        options = config.get_matrix_options()
        matrix = RGBMatrix(options=options)
    if canvas is None:
        canvas = matrix.CreateFrameCanvas()
    if orientation_mgr is None:
        orientation_mgr = OrientationManager(matrix, portrait_mode=config.IS_PORTRAIT)

    start_time = time.time()
    while time.time() - start_time < duration:
        if state.DISPLAY_MODE != "LIVE" or state.SCREEN_BLANKED:
            return canvas

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

        time.sleep(0.95)

    return canvas
