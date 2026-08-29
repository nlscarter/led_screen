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
print(laps)

# Analytics
stints     = session.stints(car_class="HYPERCAR")
pace       = session.pace(car_class="HYPERCAR")
pit_window = session.pit_window(car="7")

# Plots
session.plot_stint_chart(car_class="HYPERCAR")
session.plot_gap_to_leader(car_class="HYPERCAR")
session.plot_lap_evolution(car="7")
