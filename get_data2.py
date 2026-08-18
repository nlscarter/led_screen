import time
import requests
import pandas as pd

# OpenWEC public live timing endpoint
# (Replace with the active weekend session ID or live endpoint from openwec.com)
LIVE_TIMING_URL = "https://openwec.com"


def fetch_live_dataframe():
    try:
        response = requests.get(LIVE_TIMING_URL, timeout=2)
        if response.status_code == 200:
            data = response.json()
            # Expecting an array of car timing objects
            cars_list = data.get("cars", [])

            # Convert raw JSON directly into a structured DataFrame
            df = pd.DataFrame(cars_list)

            # Ensure proper data types and sorting by track position
            if not df.empty and "position" in df.columns:
                df["position"] = pd.to_numeric(df["position"])
                df = df.sort_values(by="position")
            return df
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None


def update_led_display(df):
    if df is None or df.empty:
        print("No live timing data available.")
        return

    # Isolate the top 3 entries for the LED crawl/display matrix
    top_3 = df.head(3)

    print("\n--- LIVE TIMING REFRESH ---")
    for _, row in top_3.iterrows():
        pos = row.get("position", "N/A")
        car_num = row.get("car_number", "??")
        gap = row.get("gap_to_leader", "0.000")

        # Format a clean string to push to your LED matrix hardware
        led_string = f"P{pos} | #{car_num} | Gap: {gap}"
        print(led_string)

        # TODO: Add your hardware SPI/I2C write commands here:
        # led_matrix.print_text(led_string)


# Main execution loop mimicking a live hardware driver
if __name__ == "__main__":
    print("Starting live LED stream script. Press Ctrl+C to stop.")
    while True:
        live_df = fetch_live_dataframe()
        update_led_display(live_df)

        # Standard live timing boards poll every 1 to 2 seconds
        time.sleep(1.5)
