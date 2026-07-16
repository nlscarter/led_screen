import os
import time
import random
import threading
import requests
from bs4 import BeautifulSoup

#This is now from OLD LAPTOP

# Simulator targeted dimensions - STRICTLY 128x128
WIDTH = 128
HEIGHT = 128

# Shared global variable for your scraped text string
scraped_text = "Loading..."
scroll_position = 0  # Monitors horizontal text placement for marquee scrolling

# Simple 5x7 Font Bitmap representation for ASCII 32 (Space) through 126 (~)
# Columns are binary maps where 1 is an active pixel, 0 is blank space
FONT = {
    ' ':[],
'A': [0x7E, 0x11, 0x11, 0x11, 0x7E], 'B': [0x7F, 0x49, 0x49, 0x49, 0x36],
'C': [0x3E, 0x41, 0x41, 0x41, 0x22], 'D': [0x7F, 0x41, 0x41, 0x22, 0x1C],
'E': [0x7F, 0x49, 0x49, 0x49, 0x41], 'F': [0x7F, 0x09, 0x09, 0x09, 0x01],
'G': [0x3E, 0x41, 0x49, 0x49, 0x3A], 'H': [0x7F, 0x08, 0x08, 0x08, 0x7F],
'I': [0x00, 0x41, 0x7F, 0x41, 0x00], 'J': [0x20, 0x40, 0x41, 0x3F, 0x01],
'K': [0x7F, 0x08, 0x14, 0x22, 0x41], 'L': [0x7F, 0x40, 0x40, 0x40, 0x40],
'M': [0x7F, 0x02, 0x0C, 0x02, 0x7F], 'N': [0x7F, 0x04, 0x08, 0x10, 0x7F],
'O': [0x3E, 0x41, 0x41, 0x41, 0x3E], 'P': [0x7F, 0x09, 0x09, 0x09, 0x06],
'Q': [0x3E, 0x41, 0x51, 0x21, 0x5E], 'R': [0x7F, 0x09, 0x19, 0x29, 0x46],
'S': [0x46, 0x49, 0x49, 0x49, 0x31], 'T': [0x01, 0x01, 0x7F, 0x01, 0x01],
'U': [0x3F, 0x40, 0x40, 0x40, 0x3F], 'V': [0x1F, 0x20, 0x40, 0x20, 0x1F],
'W': [0x7F, 0x20, 0x18, 0x20, 0x7F], 'X': [0x63, 0x14, 0x08, 0x14, 0x63],
'Y': [0x07, 0x08, 0x70, 0x08, 0x07], 'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
'.': [0x00, 0x60, 0x60, 0x00, 0x00], ',': [0x00, 0x50, 0x30, 0x00, 0x00],
'!': [0x00, 0x00, 0x5F, 0x00, 0x00], '?': [0x02, 0x01, 0x51, 0x09, 0x06],
':': [0x00, 0x36, 0x36, 0x00, 0x00], '-': [0x08, 0x08, 0x08, 0x08, 0x08]
}

def scrape_worker():
    """Background thread that pulls text cleanly from the quotes sandbox page."""
    global scraped_text
    url = "https://quotes.toscrape.com"
    headers = {"User-Agent": "Mozilla/5.0"}

    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                quote_element = soup.select_one("span.text")
                if quote_element:
                    # Sanitize and keep uppercase to fit our bitmap character dictionary mapping safely
                    scraped_text = "   " + quote_element.get_text().strip().upper().replace('"', '') + "   "
        except Exception:
            pass
        time.sleep(60)


def generate_rgb_frame_with_text():
    """Simulates a 128x128 matrix frame buffer embedding live text canvas data."""
    global scroll_position

    # Initialize basic grid background array map
    frame = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # Subtle gradient lines background pattern
            r = int((x / WIDTH) * 2)
            g = int((y / HEIGHT) * 2)
            b = 0
            row.append([r, g, b])
        frame.append(row)

    # Convert the scraped text message string to an operational column pixel map array
    text_pixels = []
    for char in scraped_text:
        # Fallback to empty space block if an obscure char character is missing from our font map
        bitmap = FONT.get(char, FONT[' '])
        for col in bitmap:
            text_pixels.append(col)
        text_pixels.append(0)  # Standard 1px character tracking column gap

    # Determine vertical center target coordinates to center the 7px tall font layout (e.g. Row 60)
    start_y = (HEIGHT // 2) - 4

    # Plot mapped active text canvas columns over current active frame viewport coordinates
    for screen_x in range(WIDTH):
        # Calculate matching character array memory offset index from active scrolling position state loop
        text_data_idx = screen_x + scroll_position
        if 0 <= text_data_idx < len(text_pixels):
            column_byte = text_pixels[text_data_idx]
            # Unpack 7 vertical bits making up this font character column column slice array map
            for bit_y in range(7):
                if (column_byte >> bit_y) & 1:
                    target_y = start_y + bit_y
                    if 0 <= target_y < HEIGHT:
                        # Draw solid high-intensity white text color pixels onto our array canvas
                        frame[target_y][screen_x] = [5, 5, 5]

    # Shift scroll window forward. Return back to index 0 point loop when text fully passes viewport
    scroll_position += 1
    if scroll_position > len(text_pixels):
        scroll_position = -WIDTH

    return frame


def draw_console_led_screen(matrix):
    """Renders a 128x128 color matrix into a compact 128x64 character footprint."""
    output = ["\033[H"]

    for y in range(0, HEIGHT, 2):
        for x in range(WIDTH):
            top_pixel = matrix[y][x]
            bottom_pixel = matrix[y + 1][x]

            top_color = 16 + (top_pixel[0] * 36) + (top_pixel[1] * 6) + top_pixel[2]
            bot_color = 16 + (bottom_pixel[0] * 36) + (bottom_pixel[1] * 6) + bottom_pixel[2]

            output.append(f"\033[48;5;{top_color}m\033[38;5;{bot_color}m▄")
        output.append("\033[0m\n")

    print("".join(output), end="", flush=True)


if __name__ == "__main__":
    os.system('clear' if os.name != 'nt' else 'cls')

    t = threading.Thread(target=scrape_worker)
    t.daemon = True
    t.start()

    print("Starting 128x128 LED Terminal Matrix with scrolling text...", flush=True)
    time.sleep(2)

    while True:
        # 1. Fetch current frame graphics with text processed directly inside matrix coordinates
        frame_data = generate_rgb_frame_with_text()

        # 2. Render frame data directly to terminal monitor
        draw_console_led_screen(frame_data)

        # 3. Marquee ticker loop update pacing rate limit (0.05s translates to a snappy ~20 FPS)
        time.sleep(0.05)
