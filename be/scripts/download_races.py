"""
01_download_races.py

Downloads historical Formula 1 race data using FastF1 and stores the
raw datasets for future feature engineering.

Project: F1 Strategist
Author: Manas Kohli
"""

from pathlib import Path

import fastf1
from fastf1.exceptions import RateLimitExceededError


# ==========================================================
# Project Paths
# ==========================================================

BACKEND_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BACKEND_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

CACHE_DIR = DATA_DIR / "cache"

REPORT_PATH = DATA_DIR / "download_report.csv"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# FastF1 Cache
# ==========================================================

fastf1.Cache.enable_cache(CACHE_DIR)


# ==========================================================
# Seasons
# ==========================================================

START_SEASON = 2024
END_SEASON = 2025

SEASONS = range(START_SEASON, END_SEASON + 1)


# ==========================================================
# Required Raw Datasets
# ==========================================================

REQUIRED_FILES = {
    "laps.csv",
    "weather.csv",
    "results.csv",
    "track_status.csv",
    "race_control.csv",
}


# ==========================================================
# Download Report
# ==========================================================

download_report = []


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
        Output CSV path.
    """

    if df is None:
        return

    df.to_csv(filepath, index=False)


def get_race_directory(season: int, event_name: str) -> Path:
    """
    Returns the directory where a race's raw data is stored.
    """

    safe_event_name = event_name.replace(" ", "_")

    return RAW_DATA_DIR / str(season) / safe_event_name


def race_already_downloaded(
    season: int,
    event_name: str
) -> bool:
    """
    Checks whether all required raw datasets already exist
    for a race.
    """

    race_dir = get_race_directory(
        season,
        event_name
    )

    if not race_dir.exists():
        return False

    existing_files = {
        file.name
        for file in race_dir.iterdir()
        if file.is_file()
    }

    return REQUIRED_FILES.issubset(existing_files)


# ==========================================================
# Download Functions
# ==========================================================

def download_race(
    season: int,
    event_name: str
):
    """
    Downloads a single Formula 1 race session.

    Parameters
    ----------
    season : int
        F1 season.

    event_name : str
        Name of the race.

    Returns
    -------
    Session | None
    """

    print(
        f"\nDownloading {season} - {event_name}"
    )

    try:

        session = fastf1.get_session(
            season,
            event_name,
            "R"
        )

        session.load()

        print("✓ Download complete")

        return session

    except RateLimitExceededError:

        print(
            "\n⚠ FastF1 API rate limit reached."
        )

        print(
            "The download will stop safely."
        )

        print(
            "Wait for the rate limit to reset "
            "before running the script again."
        )

        raise

    except Exception as e:

        print(
            f"✗ Failed: {e}"
        )

        return None


def save_session_data(
    session,
    season: int,
    event
):
    """
    Saves the raw FastF1 datasets for one race.
    """

    event_name = event["EventName"]

    race_dir = get_race_directory(
        season,
        event_name
    )

    race_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    datasets = {
        "laps.csv": session.laps,
        "weather.csv": session.weather_data,
        "results.csv": session.results,
        "track_status.csv": session.track_status,
        "race_control.csv": session.race_control_messages,
    }

    print(
        f"Saving {event_name}..."
    )

    for filename, dataframe in datasets.items():

        try:

            save_dataframe(
                dataframe,
                race_dir / filename
            )

        except Exception as e:

            print(
                f"Could not save "
                f"{filename}: {e}"
            )

    print(
        f"✓ Saved {event_name}"
    )


def process_race(
    season: int,
    event
):
    """
    Downloads and saves one race.
    """

    event_name = event["EventName"]

    # ------------------------------------------------------
    # Skip already downloaded races
    # ------------------------------------------------------

    if race_already_downloaded(
        season,
        event_name
    ):

        print(
            f"✓ {season} {event_name} "
            f"already downloaded - skipping"
        )

        download_report.append({
            "season": season,
            "race": event_name,
            "status": "skipped",
        })

        return

    # ------------------------------------------------------
    # Download race
    # ------------------------------------------------------

    session = download_race(
        season,
        event_name
    )

    if session is None:

        download_report.append({
            "season": season,
            "race": event_name,
            "status": "failed",
        })

        return

    # ------------------------------------------------------
    # Save race
    # ------------------------------------------------------

    save_session_data(
        session,
        season,
        event
    )

    download_report.append({
        "season": season,
        "race": event_name,
        "status": "success",
    })


def download_season(
    season: int
):
    """
    Downloads every race in a Formula 1 season.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        f"Downloading {season} Season"
    )

    print(
        "=" * 60
    )

    try:

        schedule = fastf1.get_event_schedule(
            season
        )

    except RateLimitExceededError:

        print(
            "\n⚠ Rate limit reached "
            "while retrieving schedule."
        )

        raise
    for _, event in schedule.iterrows():

        # Skip testing events
        if event["EventFormat"] == "testing":
            continue

        # Skip events without a valid race session
        if event["Session5"] != "Race":
            continue

        try:

            process_race(
                season,
                event
            )

        except RateLimitExceededError:

            print(
                "\nStopping download."
            )

            raise

# ==========================================================
# Save Download Report
# ==========================================================

def save_download_report():
    """
    Saves the download status of every processed race.
    """

    if not download_report:
        return

    import pandas as pd

    report_df = pd.DataFrame(
        download_report
    )

    report_df.to_csv(
        REPORT_PATH,
        index=False
    )

    print(
        f"\nDownload report saved to:"
        f"\n{REPORT_PATH}"
    )


# ==========================================================
# Main
# ==========================================================

def main():

    try:

        for season in SEASONS:

            download_season(
                season
            )

    except RateLimitExceededError:

        print(
            "\nDownload stopped because "
            "the FastF1 API rate limit was reached."
        )

        print(
            "Your completed races are safe."
        )

        print(
            "Run the script again after "
            "the rate limit resets."
        )

    finally:

        save_download_report()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()