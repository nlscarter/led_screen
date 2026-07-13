import time
import threading
import requests
from bs4 import BeautifulSoup

# Shared global variable for your LED screen execution loop
current_display_text = "Loading Test Page..."


def scrape_test_worker():
    """Background task that pulls clean HTML from a scraper sandbox site."""
    global current_display_text

    # A standard, static sandbox URL that does not block automated requests
    url = "https://toscrape.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    while True:
        try:
            # Fetch the plain text HTML data
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Target the very first span element with the class name 'text'
                quote_element = soup.select_one("span.text")

                if quote_element:
                    # Strip out quote marks and whitespace for a clean LED layout string
                    raw_text = quote_element.get_text().strip().replace('"', '')
                    current_display_text = raw_text
                else:
                    current_display_text = "Error: Element class 'text' not found."
            else:
                current_display_text = f"HTTP Error: {response.status_code}"

        except Exception as e:
            current_display_text = f"Connection Error: {e}"

        # Wait 5 minutes (300 seconds) before parsing the test sandbox page again
        time.sleep(300)


def start_weather_thread():
    """Initialises and spins up the isolated background scraper thread."""
    test_thread = threading.Thread(target=scrape_test_worker)
    test_thread.daemon = True
    test_thread.start()


# --- Main LED execution driver ---
if __name__ == "__main__":
    # Start our background network scraping sequence
    start_weather_thread()

    print("Director script initialized successfully. Starting main loop...", flush=True)

    while True:
        # The flush=True forces the text directly into the console window instantly
        print(f"Console Output Display Text: {current_display_text}", flush=True)
        time.shape = time.sleep(2)
