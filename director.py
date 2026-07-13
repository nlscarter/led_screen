import time
import threading
import requests
from bs4 import BeautifulSoup

# Global variable to store the shared temperature string
# Your LED rendering code will constantly read from this variable
current_temp_display = "Loading..."


def scrape_weather_worker():
    """Background task that runs forever, updating the temperature every 15 mins."""
    global current_temp_display

    url = "https://weather.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    while True:
        try:
            # 10 second timeout ensures a hung connection won't freeze the thread forever
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Dynamic substring matcher targets weather.com's dynamic class tags
                temp_element = soup.select_one("span[class*='CurrentConditions--tempValue--']")

                if temp_element:
                    # Update our global variable with clean data (e.g. "14°")
                    current_temp_display = temp_element.get_text().strip()
                else:
                    # Alternative testid anchor fallback check
                    fallback = soup.find("span", {"data-testid": "TemperatureValue"})
                    if fallback:
                        current_temp_display = fallback.get_text().strip()

        except Exception as e:
            # Silently log errors to prevent a network glitch from crashing your hardware pipeline
            print(f"Weather Fetch Error: {e}")

        # Wait 15 minutes (900 seconds) before hitting weather.com again
        time.sleep(900)


def start_weather_thread():
    """Initialises and spins up the isolated background scraper thread."""
    weather_thread = threading.Thread(target=scrape_weather_worker)
    # Daemon means the thread automatically exits when the main program stops
    weather_thread.daemon = True
    weather_thread.start()


# =========================================================================
# YOUR LED DISPLAY / INFRASTRUCTURE CODE
# =========================================================================
def main_led_loop():
    """Simulated placeholder for your existing Matrix / LED screen drawing loop."""
    print("Initialising LED screen hardware configurations...")

    # 1. Start the scraping worker before launching the layout loop
    start_weather_thread()

    # 2. Main hardware animation loop
    while True:
        # Access the global variable directly. Your display will always render
        # smoothly, reading the latest value fetched by the thread.
        print(f"[LED Matrix Output] Rendering Frame | Temp Data: {current_temp_display}")

        # Simulated frames-per-second delay for the LED matrix
        time.sleep(0.1)


if __name__ == "__main__":
    main_led_loop()
