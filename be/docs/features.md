# Feature Registry

## F1 Strategist

This document defines the features used by the F1 Strategist machine learning
pipeline.

Each training row represents one driver's race state at a specific lap.

The model uses only information that would have been available at that point
in the race.

---

## Target

| Feature | Type | Source | Description |
|---|---|---|---|
| laps_until_pit | numerical | derived | Number of laps until the driver's next pit stop |

---

## Race Features

| Feature | Type | Source | Description |
|---|---|---|---|
| season | numerical | session | F1 season |
| round | numerical | event schedule | Race round |
| circuit | categorical | session | Circuit name |
| lap_number | numerical | laps | Current lap |

---

## Driver / Team Features

| Feature | Type | Source | Description |
|---|---|---|---|
| driver | categorical | laps | Driver abbreviation |
| constructor | categorical | results | Constructor/team |
| grid_position | numerical | results | Starting grid position |

---

## Tire Features

| Feature | Type | Source | Description |
|---|---|---|---|
| compound | categorical | laps | Current tire compound |
| tyre_age | numerical | laps | Age of current tire set |
| stint_number | numerical | derived | Current tire stint |
| pit_stop_count | numerical | derived | Number of previous pit stops |

---

## Pace Features

| Feature | Type | Source | Description |
|---|---|---|---|
| previous_lap_time | numerical | laps | Previous completed lap time |
| avg_lap_time_3 | numerical | derived | Average lap time over previous 3 laps |
| avg_lap_time_5 | numerical | derived | Average lap time over previous 5 laps |
| fastest_lap_time | numerical | derived | Fastest lap completed so far |

---

## Position Features

| Feature | Type | Source | Description |
|---|---|---|---|
| position | numerical | laps | Current race position |
| gap_ahead | numerical | derived | Gap to car ahead |
| gap_behind | numerical | derived | Gap to car behind |

---

## Weather Features

| Feature | Type | Source | Description |
|---|---|---|---|
| air_temperature | numerical | weather | Air temperature |
| track_temperature | numerical | weather | Track temperature |
| humidity | numerical | weather | Humidity |
| rainfall | numerical | weather | Rainfall indicator |

---

## Race Status Features

| Feature | Type | Source | Description |
|---|---|---|---|
| track_status | categorical | track status | Current track status |
| safety_car_active | boolean | derived | Whether safety car is active |
| vsc_active | boolean | derived | Whether virtual safety car is active |
| yellow_flag | boolean | derived | Whether yellow flag conditions are active |

---

# Data Leakage Rules

Features must only contain information available at the current lap.

The following information must never be used as input features:

- Future lap times
- Future positions
- Final race position
- Future pit stops
- Future safety car events
- Future tire compounds
- Any information occurring after the prediction point

The target `laps_until_pit` is calculated using future information, but it is
used only as the target variable and never as an input feature.