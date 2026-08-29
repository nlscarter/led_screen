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