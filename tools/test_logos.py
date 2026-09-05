#!/usr/bin/env python3
"""
Test script to render all LOGO_DATA logos on the LED matrix screen.
Supports hardware RGB matrix (Raspberry Pi) and simulation/debugger canvas (matplotlib).
"""

import os
import sys
import time
import argparse

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.path.dirname(__file__)) == "tools" else os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import config
from assets.graphics import LOGO_DATA
from engine.drawing import OrientationManager, draw_logo_, small_font, tiny_font
from engine.matrix import RGBMatrix, RUNNING_ON_HARDWARE


def get_grid_dimensions(orientation_mgr, total_logos=24):
    """
    Calculates the optimal grid (cols, rows) to fit up to 24 logos on screen.
    Landscape (96x48): 6 cols x 4 rows (16x12px cells) -> fits up to 24 logos.
    Portrait (48x96):  3 cols x 8 rows (16x12px cells) -> fits up to 24 logos.
    """
    if orientation_mgr.portrait_mode:
        cols = 3
        rows = 8
    else:
        cols = 6
        rows = 4
    return cols, rows


def render_all_logos_grid(canvas, orientation_mgr, logos_list=None, page=0, cols=None, rows=None):
    """
    Renders logos simultaneously on screen arranged in a high-density grid.
    Supports up to 24 logos on a single screen (6x4 in landscape, 3x8 in portrait).
    If there are more logos than fit on one page, supports pagination via the `page` argument.
    """
    if logos_list is None:
        logos_list = list(LOGO_DATA.keys())

    default_cols, default_rows = get_grid_dimensions(orientation_mgr, len(logos_list))
    if cols is None:
        cols = default_cols
    if rows is None:
        rows = default_rows

    per_page = cols * rows
    total_pages = max(1, (len(logos_list) + per_page - 1) // per_page)
    current_page = page % total_pages
    page_logos = logos_list[current_page * per_page:(current_page + 1) * per_page]

    canvas.Clear()

    cell_width = orientation_mgr.width // cols
    cell_height = orientation_mgr.height // rows

    for idx, logo_name in enumerate(page_logos):
        col_idx = idx % cols
        row_idx = idx // cols

        logo_raw = LOGO_DATA.get(logo_name, [])
        logo_width = len(logo_raw) if logo_raw else 10

        # Center horizontally within the cell, keeping inside screen boundaries
        if logo_width <= cell_width:
            start_x = col_idx * cell_width + (cell_width - logo_width) // 2
        else:
            start_x = col_idx * cell_width

        # Ensure start_x does not overflow canvas width
        start_x = max(0, min(start_x, orientation_mgr.width - min(logo_width, cell_width)))

        # Position vertically (10-pixel logo inside cell_height)
        start_y = row_idx * cell_height + min(cell_height - 1, 10)

        draw_logo_(canvas, orientation_mgr, logo_name, start_x=start_x, start_y=start_y)

    return total_pages


def render_logo_single(canvas, orientation_mgr, logo_name, index, total):
    """
    Renders a single logo enlarged / centered with its label and index information.
    """
    canvas.Clear()

    logo_raw = LOGO_DATA.get(logo_name, [])
    logo_width = len(logo_raw) if logo_raw else 10

    # Header with logo name and index
    title = f"[{index + 1}/{total}] {logo_name}"
    tiny_font(canvas, orientation_mgr, title, start_x=2, x_width=orientation_mgr.width - 4, start_y=6, colour=11)

    # Centered logo
    logo_x = max(0, (orientation_mgr.width - logo_width) // 2)
    draw_logo_(canvas, orientation_mgr, logo_name, start_x=logo_x, start_y=24)

    # Footer with width details
    dim_text = f"Width: {logo_width}px"
    tiny_font(canvas, orientation_mgr, dim_text, start_x=2, x_width=orientation_mgr.width - 4, start_y=38, colour=8)


def swap_canvas(matrix, canvas):
    """Refreshes the canvas on hardware or interactive simulation."""
    if not RUNNING_ON_HARDWARE:
        canvas.Show()
        return canvas
    return matrix.SwapOnVSync(canvas)


def run_logo_test(mode="grid", duration=3.0, cols=None, rows=None):
    """
    Main display loop for testing logos.
    
    Modes:
      - 'grid': Displays all logos in a high-density grid (up to 24 on a single screen, auto-paged if more).
      - 'cycle': Cycles through each logo individually with its name and dimensions.
      - 'both': Alternates between full grid view and individual logo showcase.
    """
    options = config.get_matrix_options()
    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()
    orientation_mgr = OrientationManager(matrix, portrait_mode=config.IS_PORTRAIT)

    all_logos = list(LOGO_DATA.keys())
    total_logos = len(all_logos)

    default_cols, default_rows = get_grid_dimensions(orientation_mgr, total_logos)
    active_cols = cols if cols is not None else default_cols
    active_rows = rows if rows is not None else default_rows
    logos_per_screen = active_cols * active_rows

    print("=" * 60)
    print(f"Rendering LOGO_DATA on LED Matrix ({orientation_mgr.width}x{orientation_mgr.height})")
    print(f"Total logos found ({total_logos}): {', '.join(all_logos)}")
    print(f"Grid layout: {active_cols} cols x {active_rows} rows ({logos_per_screen} logos/screen)")
    print(f"Mode: {mode}")
    print("Press Ctrl+C to stop.")
    print("=" * 60)

    try:
        if mode == "grid":
            current_page = 0
            last_switch = time.time()
            total_pages = render_all_logos_grid(canvas, orientation_mgr, all_logos, page=current_page, cols=active_cols, rows=active_rows)
            canvas = swap_canvas(matrix, canvas)

            while True:
                time.sleep(0.1)
                now = time.time()
                if total_pages > 1 and (now - last_switch >= duration):
                    current_page = (current_page + 1) % total_pages
                    last_switch = now
                    total_pages = render_all_logos_grid(canvas, orientation_mgr, all_logos, page=current_page, cols=active_cols, rows=active_rows)
                    canvas = swap_canvas(matrix, canvas)
                elif not RUNNING_ON_HARDWARE:
                    render_all_logos_grid(canvas, orientation_mgr, all_logos, page=current_page, cols=active_cols, rows=active_rows)
                    canvas = swap_canvas(matrix, canvas)

        elif mode == "cycle":
            curr_idx = 0
            while True:
                logo_name = all_logos[curr_idx]
                render_logo_single(canvas, orientation_mgr, logo_name, curr_idx, total_logos)
                canvas = swap_canvas(matrix, canvas)

                time.sleep(duration)
                curr_idx = (curr_idx + 1) % total_logos

        elif mode == "both":
            while True:
                # Show all logos in grid (cycling pages if multi-page)
                total_pages = max(1, (total_logos + logos_per_screen - 1) // logos_per_screen)
                for pg in range(total_pages):
                    print(f"Displaying logos grid (page {pg + 1}/{total_pages})...")
                    render_all_logos_grid(canvas, orientation_mgr, all_logos, page=pg, cols=active_cols, rows=active_rows)
                    canvas = swap_canvas(matrix, canvas)
                    time.sleep(duration * 2)

                # Cycle through each logo
                for idx, logo_name in enumerate(all_logos):
                    print(f"Displaying logo: {logo_name} ({idx + 1}/{total_logos})")
                    render_logo_single(canvas, orientation_mgr, logo_name, idx, total_logos)
                    canvas = swap_canvas(matrix, canvas)
                    time.sleep(duration)

    except KeyboardInterrupt:
        print("\nStopping logo test. Clearing screen...")
        canvas.Clear()
        swap_canvas(matrix, canvas)


def main():
    parser = argparse.ArgumentParser(description="Render all LOGO_DATA logos on LED matrix screen.")
    parser.add_argument(
        "--mode",
        choices=["grid", "cycle", "both"],
        default="grid",
        help="Display mode: 'grid' (all logos at once in high-density grid, default), 'cycle' (one by one), 'both' (alternate)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=3.0,
        help="Duration (seconds) per view in cycling modes (default: 3.0s)",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=None,
        help="Number of columns in grid (default: 6 for landscape, 3 for portrait)",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=None,
        help="Number of rows in grid (default: 4 for landscape, 8 for portrait)",
    )
    args = parser.parse_args()

    run_logo_test(mode=args.mode, duration=args.duration, cols=args.cols, rows=args.rows)


if __name__ == "__main__":
    main()
