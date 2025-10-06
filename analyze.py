# scripts/analyze.py
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB = DATA_DIR / "movies.db"
OUT = DATA_DIR / "outputs"
OUT.mkdir(exist_ok=True)

def run_queries():
    conn = sqlite3.connect(DB)
    
    print("\n== Top 10 movies by revenue ==")
    q1 = "SELECT title, revenue FROM movies ORDER BY revenue DESC LIMIT 10"
    print(pd.read_sql(q1, conn))
    
    print("\n== Average rating by genre ==")
    q2 = "SELECT main_genre, AVG(vote_average) as avg_rating FROM movies GROUP BY main_genre ORDER BY avg_rating DESC"
    print(pd.read_sql(q2, conn))
    
    df = pd.read_sql("SELECT * FROM movies", conn)
    conn.close()
    return df

def make_plots(df):
    sns.set(style="whitegrid")

    # Trend of avg rating by year
    plt.figure(figsize=(8,4))
    sns.lineplot(x="year", y="vote_average", data=df, ci=None)
    plt.title("Average Movie Rating by Year")
    plt.savefig(OUT/"rating_trend.png")
    plt.close()

    # Distribution of ROI
    plt.figure(figsize=(6,4))
    sns.histplot(df["roi"].dropna(), bins=50, log_scale=True)
    plt.title("ROI Distribution")
    plt.savefig(OUT/"roi_distribution.png")
    plt.close()

    print("Plots saved in", OUT)

if __name__ == "__main__":
    df = run_queries()
    make_plots(df)
