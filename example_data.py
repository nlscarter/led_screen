import json
import pandas as pd

# Paste the raw string directly to simulate an offline loop environment
mock_json = {
  "session": {
    "name": "24 Hours of Le Mans - Race",
    "status": "Green",
    "time_remaining": "14:22:05",
    "lap_leader": 142,
    "track_condition": "Dry"
  },
  "cars": [
    {
      "position": 1,
      "class_position": 1,
      "car_number": "50",
      "class": "Hypercar",
      "team": "Ferrari AF Corse",
      "current_driver": "N. Nielsen",
      "last_lap": "3:29.412",
      "best_lap": "3:28.904",
      "gap_to_leader": "0.000",
      "interval": "0.000",
      "pit_stops": 12,
      "in_pit": False,
      "sectors": {"s1": "32.110", "s2": "1:18.402", "s3": "1:38.900"}
    },
    {
      "position": 2,
      "class_position": 2,
      "car_number": "7",
      "class": "Hypercar",
      "team": "Toyota Gazoo Racing",
      "current_driver": "K. Kobayashi",
      "last_lap": "3:29.980",
      "best_lap": "3:28.120",
      "gap_to_leader": "+1.420",
      "interval": "+1.420",
      "pit_stops": 12,
      "in_pit": False,
      "sectors": {"s1": "32.450", "s2": "1:18.510", "s3": "1:39.020"}
    },
    {
      "position": 3,
      "class_position": 1,
      "car_number": "91",
      "class": "LMGT3",
      "team": "Manthey EMA",
      "current_driver": "R. Lietz",
      "last_lap": "3:58.102",
      "best_lap": "3:56.550",
      "gap_to_leader": "3 Laps",
      "interval": "2 Laps",
      "pit_stops": 10,
      "in_pit": True,
      "sectors": {"s1": "36.210", "s2": "1:28.910", "s3": "1:52.982"}
    }
  ]
}