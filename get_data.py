import openwec


#/sessions/{id}/race-control
#/sessions/{id}/laps/{car}


# Load a specific session (e.g., Le Mans 2026 Race)
# The syntax mimics FastF1 (year, event/circuit, session type)
session = openwec.Session("WEC", 2026, "Le Mans", "Race")
print(session)
openwec.configure(api_key="owec_e8N1kbg-lER2ZccDr6lgX1WmFmN_Gt6y")

laps = session.laps(car="7")
#t = session.stints("7")

# Results (public, no API key needed)
results = session.results()
print(results.head())

# Main execution loop mimicking a live hardware driver
#if __name__ == "__main__":
#    print("Starting live LED stream script. Press Ctrl+C to stop.")
#    while True:
#        live_df = fetch_live_dataframe()
#        update_led_display(live_df)

        # Standard live timing boards poll every 1 to 2 seconds
        #time.sleep(1.5)
