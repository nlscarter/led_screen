import openwec

# Load a specific session (e.g., Le Mans 2026 Race)
# The syntax mimics FastF1 (year, event/circuit, session type)
session = openwec.Session("WEC", 2026, "Le Mans", "Race")
print(session)
openwec.configure(api_key="owec_e8N1kbg-lER2ZccDr6lgX1WmFmN_Gt6y")

laps = session.laps(car="007")

# Results (public, no API key needed)
results = session.results()
print(results.head())
a=0

def stint(laps):
    df = laps.copy()
    name_changes = df['driver_name'] != df['driver_name'].shift()
    last_group_start = name_changes.to_numpy().nonzero()[0][-1]
    slice_for_latest_driver = df.iloc[last_group_start:]
    return slice_for_latest_driver

def strint_pixels(stint):
    df = stint.copy()
    return (~df['crossing_finish_in_pit']).astype(int).tolist()

pixels = strint_pixels(stint(session.laps(car="007")))
print(pixels)
a=0


