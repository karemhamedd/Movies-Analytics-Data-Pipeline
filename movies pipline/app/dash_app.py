import pandas as pd
import sqlite3
import ast
from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px

# -------------------------
# Load Data from SQLite
# -------------------------
conn = sqlite3.connect("data/movies.db")  # adjust path if needed
df = pd.read_sql("SELECT * FROM movies", conn)

# -------------------------
# Extract Main Genre
# -------------------------
def extract_main_genre(genre_str):
    try:
        genres = ast.literal_eval(genre_str)  # convert string repr into Python list
        if isinstance(genres, list) and len(genres) > 0:
            return genres[0]["name"].strip()  # take the first genre name
    except Exception as e:
        print("Genre parse error:", e, "->", genre_str)
        return None
    return None

df["main_genre"] = df["genres"].apply(extract_main_genre)

# --- Clean genres ---
df["main_genre"] = df["main_genre"].astype(str).str.strip()
df = df[df["main_genre"].notna() & (df["main_genre"] != "None")]

# Print unique genres for debugging
print("✅ Unique genres in dataset:", df["main_genre"].unique())

# Only show selected columns in the dashboard
columns_to_show = ["title", "main_genre", "budget", "revenue", "vote_average", "popularity", "year", "roi"]

# -------------------------
# Create Dash App
# -------------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("🎬 Movies Analytics Dashboard", style={"textAlign": "center"}),

    # Dropdown filter
    html.Div([
        html.Label("Select Genre:"),
        dcc.Dropdown(
            id="genre_filter",
            options=[{"label": g, "value": g} for g in sorted(df["main_genre"].unique())],
            value=None,
            placeholder="Choose a genre..."
        )
    ], style={"width": "40%", "margin": "auto"}),

    html.Br(),

    # Row counter (NEW)
    html.Div(id="row_count", style={"textAlign": "center", "fontWeight": "bold", "margin": "10px"}),

    # Data Table
    dash_table.DataTable(
        id="movies_table",
        columns=[{"name": col, "id": col} for col in columns_to_show],
        data=df[columns_to_show].to_dict("records"),
        page_size=20,  # show 20 rows per page for clarity
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "5px"},
        style_header={"backgroundColor": "black", "color": "white"}
    ),

    html.Br(),

    # Graphs
    html.Div([
        dcc.Graph(id="revenue_by_genre"),
        dcc.Graph(id="rating_vs_popularity")
    ])
])

# -------------------------
# Callbacks
# -------------------------
@app.callback(
    [Output("movies_table", "data"),
     Output("revenue_by_genre", "figure"),
     Output("rating_vs_popularity", "figure"),
     Output("row_count", "children")],
    [Input("genre_filter", "value")]
)
def update_dashboard(selected_genre):
    if selected_genre:
        dff = df[df["main_genre"] == selected_genre]
    else:
        dff = df.copy()

    row_text = f"📊 Showing {len(dff)} movies"

    if dff.empty:
        empty_fig = px.scatter(title="No data available for this selection")
        return [], empty_fig, empty_fig, row_text

    # Bar chart: Revenue by Genre
    revenue_by_genre = dff.groupby("main_genre", as_index=False)["revenue"].mean()
    fig1 = px.bar(
        revenue_by_genre,
        x="main_genre",
        y="revenue",
        title="Average Revenue by Genre",
        color="main_genre"
    )

    # Scatter plot: Rating vs Popularity
    fig2 = px.scatter(
        dff, x="vote_average", y="popularity",
        size="revenue", color="main_genre",
        hover_data=["title"],
        title="Rating vs Popularity (Bubble = Revenue)"
    )

    return dff[columns_to_show].to_dict("records"), fig1, fig2, row_text


# -------------------------
# Run the App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
