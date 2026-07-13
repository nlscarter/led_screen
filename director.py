import os
import time
import random
import threading
import requests
from bs4 import BeautifulSoup

# Simulator targeted dimensions - STRICTLY 128x128
# Note: Ensure your terminal window is widened/zoomed out to fit 128 columns and 64 rows!
WIDTH = 128
HEIGHT = 128

# Shared global variable for your scraped text string
scraped_text = "Loading..."


def scrape_worker():
    """Background thread that pulls text cleanly from the quotes sandbox page."""
    global scraped_text
    # FIXED: Corrected domain endpoint to find quotes data
    url = "https://quotes.toscrape.com"
    headers = {"User-Agent": "Mozilla/5.0"}

    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                quote_element = soup.select_one("span.text")
                if quote_element:
                    scraped_text = quote_element.get_text().strip().replace('"', '')
        except Exception:
            pass  # Keep old text if connection drops momentarily
        time.sleep(60)


def generate_mock_rgb_frame():
    """Simulates a 128x128 matrix frame buffer filled with colors."""
    frame = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # Subtle moving color gradient adjusted for 128 scale
            r = int((x / WIDTH) * 5)
            g = int((y / HEIGHT) * 5)
            b = random.randint(0, 2)
            row.append((r, g, b))
        frame.append(row)
    return frame


def draw_console_led_screen(matrix):
    """Renders a 128x128 color matrix into a compact 128x64 character footprint."""
    output = []
    # Smoothly jumps cursor to top-left of terminal to prevent flickering
    output.append("\033[H")

    # Step through 2 pixel rows at a time (y changes by 2)
    for y in range(0, HEIGHT, 2):
        for x in range(WIDTH):
            top_pixel = matrix[y][x]
            bottom_pixel = matrix[y + 1][x]

            # FIXED: Restored indexing brackets, [1], [2] to prevent tuple multiplication errors
            top_color = 16 + (top_pixel[0] * 36) + (top_pixel[1] * 6) + top_pixel[2]
            bot_color = 16 + (bottom_pixel[0] * 36) + (bottom_pixel[1] * 6) + bottom_pixel[2]

            # \033[48;5;m sets background, \033[38;5;m sets foreground (text color)
            output.append(f"\033[48;5;{top_color}m\033[38;5;{bot_color}m▄")

        # Reset color code modifiers at the end of every row
        output.append("\033[0m\n")

    print("".join(output), end="", flush=True)


if __name__ == "__main__":
    # Clear screen once at launch
    os.system('clear' if os.name != 'nt' else 'cls')

    # Spin up our web-scraping worker thread
    t = threading.Thread(target=scrape_worker)
    t.daemon = True
    t.start()

    print("Starting 128x128 LED Terminal Matrix...", flush=True)
    print("TIP: Zoom out your terminal font if the matrix grid looks distorted!", flush=True)
    time.sleep(2)

    while True:
        # 1. Fetch current frame graphics
        frame_data = generate_mock_rgb_frame()

        # 2. Render frame data directly to terminal monitor
        draw_console_led_screen(frame_data)

        # 3. Print the live scraped text status block just underneath the display
        # Added \033[K to prevent text trailing artifacts when names shift size
        print(f"\033[0mScraped Text: {scraped_text[:120]}...\033[K", flush=True)

        # Frame limit cap (approx 1 frame per second as configured)
        time.sleep(5)
