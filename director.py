import os
import time
import random
import threading
import requests
from bs4 import BeautifulSoup

# Simulator targeted dimensions
WIDTH = 128
HEIGHT = 64

# Shared global variable for your scraped text string
scraped_text = "Loading..."


def scrape_worker():
    """Background thread that pulls text cleanly from a sandbox page."""
    global scraped_text
    url = "https://toscrape.com"
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
    """Simulates a 64x32 matrix frame buffer filled with colors."""
    # Creates an array of 32 rows, each containing 64 items of (R, G, B) tuples.
    # Color scale values: 0 (dark) to 5 (brightest) for simple ANSI color matching.
    frame = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # Let's create a subtle moving color gradient for testing
            r = int((x / WIDTH) * 5)
            g = int((y / HEIGHT) * 5)
            b = random.randint(0, 2)
            row.append((r, g, b))
        frame.append(row)
    return frame


def draw_console_led_screen(matrix):
    """Renders a 64x32 color matrix into a compact 64x16 character footprint."""
    output = []
    # Smoothly jumps cursor to top-left of terminal to prevent flickering
    output.append("\033[H")

    # Step through 2 pixel rows at a time (y changes by 2)
    for y in range(0, HEIGHT, 2):
        for x in range(WIDTH):
            top_pixel = matrix[y][x]
            bottom_pixel = matrix[y + 1][x]

            # Map raw 0-5 RGB values into 256-color ANSI space
            # Formula: 16 + (R * 36) + (G * 6) + B
            top_color = 16 + (top_pixel[0] * 36) + (top_pixel[1] * 6) + top_pixel[2]
            bot_color = 16 + (bottom_pixel[0] * 36) + (bottom_pixel[1] * 6) + bottom_pixel[2]

            # \033[48;5;m sets background, \033[38;5;m sets foreground (text color)
            # '▄' fills the bottom half of the character square with the foreground color
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

    print("Starting 64x32 LED Terminal Matrix...", flush=True)
    time.sleep(1)

    while True:
        # 1. Fetch current frame graphics
        frame_data = generate_mock_rgb_frame()

        # 2. Render frame data directly to terminal monitor
        draw_console_led_screen(frame_data)

        # 3. Print the live scraped text status block just underneath the display
        print(f"\033[0mScraped Text: {scraped_text[:60]}...", flush=True)

        # Frame limit cap (approx 15 frames per second)
        time.sleep(1)
