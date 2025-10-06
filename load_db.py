# scripts/load_db.py
import pandas as pd
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CLEAN = DATA_DIR / "movies_clean.csv"
DB = DATA_DIR / "movies.db"

def run():
    df = pd.read_csv(CLEAN, parse_dates=["release_date"])
    conn = sqlite3.connect(DB)
    df.to_sql("movies", conn, if_exists="replace", index=False)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_genre ON movies(main_genre)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_year ON movies(year)")
    conn.commit()
    conn.close()
    print(f"Loaded into DB:{DB}")

if __name__ == "__main__":
    run()
