🎬 Movies Analytics Data Pipeline
📌 Project Overview

This project is an end-to-end data engineering & analytics pipeline built using Python, SQL, and Dash.
It takes raw movie data from Kaggle (TMDB 5000 Movies dataset), processes it through an ETL pipeline, stores it in SQLite, and presents insights through an interactive dashboard.

The project demonstrates practical skills in:

ETL Pipelines with Python (pandas, numpy)

Data Cleaning & Transformation (ROI, genres extraction)

SQL Database Design with SQLite

Data Analysis & Visualization (matplotlib, seaborn, Plotly)

Interactive Dashboards using Dash

📂 Project Structure
movies-pipeline/
├── data/
│   ├── tmdb_5000_movies.csv   # raw dataset (Kaggle)
│   ├── movies.db              # SQLite database after ETL
├── scripts/
│   ├── etl.py                 # extract, transform, load pipeline
│   ├── load_db.py             # load transformed data into SQLite
│   ├── analyze.py             # offline analysis (pandas + seaborn)
├── app/
│   └── dash_app.py            # Dash interactive dashboard
├── requirements.txt           # dependencies
├── example_queries.sql        # sample SQL queries
└── README.md                  # project documentation

⚙️ Technologies Used

Python (pandas, numpy)

SQLite (SQL queries & storage)

Visualization: matplotlib, seaborn, Plotly

Dashboard: Dash (Plotly)

🚀 How It Works

Extract & Transform

Read raw tmdb_5000_movies.csv

Clean null values

Compute ROI = (revenue - budget) / budget

Extract main_genre from JSON-like genres column

Load into SQLite

Save the cleaned dataset into movies.db

Analyze (Offline)

Run exploratory analysis with pandas/seaborn

Example: most profitable genres, correlation between ratings & popularity

Interactive Dashboard

Built with Dash

Features:

Filter movies by genre

Movies table with budget, revenue, ROI, rating, popularity

Bar chart: Average revenue by genre

Scatter plot: Rating vs Popularity (bubble size = revenue)

Row counter showing number of filtered movies

📊 Example Insights

Action movies dominate in count but not always in ROI.

Animation & Family genres show high ROI compared to budget.

High-rated niche genres (e.g. Documentary, Foreign) often have low revenue but strong ratings.

📁 Dataset Access
Due to the large size of the datasets, both the movies and credits CSV files are hosted on Google Drive for convenient access and reproducibility.
You can download them here:
Google Drive Dataset Link ("https://drive.google.com/drive/folders/1aB2VU4vQBIKxu4PvFtOzePFleNO6HEy9?usp=sharing")
