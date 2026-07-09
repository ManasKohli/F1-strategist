from pathlib import Path
import fastf1

CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

fastf1.Cache.enable_cache(CACHE_DIR)

session = fastf1.get_session(2024, "Monaco Grand Prix", "R")
session.load()

print(session.results.head())
