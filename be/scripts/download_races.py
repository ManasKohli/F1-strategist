"""
01_download_races.py

Downloads historical Formula 1 race data using FastF1 and stores the
raw datasets for future feature engineering.

Project: F1 Strategist
Author: Manas Kohli
"""

from pathlib import Path

import fastf1

# ==========================================================
# Project Paths
# ==========================================================

BACKEND_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BACKEND_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

CACHE_DIR = DATA_DIR / "cache"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# FastF1 Cache
# ==========================================================

fastf1.Cache.enable_cache(CACHE_DIR)

# ==========================================================
# Seasons
# ==========================================================

START_SEASON = 2022
END_SEASON = 2025

SEASONS = range(START_SEASON, END_SEASON + 1)


# ==========================================================
# Helper Functions
# ==========================================================

def save_dataframe(df, filepath: Path):
    """
    Saves a dataframe to disk.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to save.
    filepath : Path
        Output csv path.
    """
    if df is None:
        return

    df.to_csv(filepath, index=False)


# ==========================================================
# Download Functions
# ==========================================================

def download_race(season: int, event_name: str):
    """
    Downloads a single Formula 1 race session.

    Parameters
    ----------
    season : int
    event_name : str

    Returns
    -------
    Session | None
    """

    print(f"\nDownloading {season} - {event_name}")

    try:

        session = fastf1.get_session(
            season,
            event_name,
            "R"
        )

        session.load()

        print("✓ Download complete")

        return session

    except Exception as e:

        print(f"✗ Failed: {e}")

        return None


def save_session_data(session, season: int, event):
    """
    Saves the raw FastF1 datasets for one race.
    """

    event_name = event["EventName"].replace(" ", "_")

    race_dir = RAW_DATA_DIR / str(season) / event_name

    race_dir.mkdir(parents=True, exist_ok=True)

    datasets = {
        "laps.csv": session.laps,
        "weather.csv": session.weather_data,
        "results.csv": session.results,
        "track_status.csv": session.track_status,
        "race_control.csv": session.race_control_messages,
    }

    print(f"Saving {event_name}...")

    for filename, dataframe in datasets.items():

        try:

            save_dataframe(
                dataframe,
                race_dir / filename
            )

        except Exception as e:

            print(f"Could not save {filename}: {e}")

    print(f"✓ Saved {event_name}")


def process_race(season: int, event):
    """
    Downloads and saves one race.
    """

    event_name = event["EventName"]

    session = download_race(
        season,
        event_name
    )

    if session is None:
        return

    save_session_data(
        session,
        season,
        event
    )


def download_season(season: int):
    """
    Downloads every race in a Formula 1 season.
    """

    print("\n" + "=" * 60)
    print(f"Downloading {season} Season")
    print("=" * 60)

    schedule = fastf1.get_event_schedule(season)

    for _, event in schedule.iterrows():

        # Skip testing events
        if event["EventFormat"] == "testing":
            continue

        process_race(
            season,
            event
        )


# ==========================================================
# Main
# ==========================================================

def main():

    for season in SEASONS:

        download_season(season)


if __name__ == "__main__":
    main()