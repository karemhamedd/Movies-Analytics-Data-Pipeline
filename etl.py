# scripts/etl.py
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
RAW = DATA_DIR / "tmdb_5000_movies.csv"
CLEAN = DATA_DIR / "movies_clean.csv"

def run():
    df = pd.read_csv(RAW)
    print("Raw shape:", df.shape)

    # Keep useful columns
    df = df[["title","genres","budget","revenue","vote_average","vote_count","release_date","popularity","runtime"]]

    # Parse dates
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year

    # Handle missing / zeros
    df["budget"] = df["budget"].replace(0, np.nan)
    df["revenue"] = df["revenue"].replace(0, np.nan)

    # Derived column: ROI
    df["roi"] = df["revenue"] / df["budget"]

    # Clean genres (string → just first genre name)
    df["main_genre"] = df["genres"].str.extract(r"'name': '([^']+)'")

    df.to_csv(CLEAN, index=False)
    print("Cleaned file saved:", CLEAN, "rows:", len(df))

if __name__ == "__main__":
    run()
