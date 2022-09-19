import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from pathlib import Path
from git import Repo
from datetime import datetime
import socket

# Get HTML from FPP website
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246" }
response = requests.get("https://hp.fpp.pt/agenda1.php?epoca=2022", headers=headers)
html = response.text

# Convert games to structured format
soup = BeautifulSoup(html, "html.parser")
competitions = soup.select("#desktop > h4")
games = []
for i, competition in enumerate(competitions):

    game_rows = soup.select(f"#desktop .toca:nth-of-type({i+1}) > table > tr")

    for game_row in game_rows:
        game = {
            "date": game_row.select_one(".coluna-data > p").get_text(separator=" ")
            if game_row.select_one(".coluna-data > p")
            else None,
            "home_team": game_row.select_one(".visitada").get_text(separator=" ")
            if game_row.select_one(".visitada")
            else None,
            "away_team": game_row.select_one(".visitante").get_text(separator=" ")
            if game_row.select_one(".visitante")
            else None,
            "url": game_row.select_one(".coluna-opcoes > a")["href"]
            if game_row.select_one(".coluna-opcoes > a")
            else None,
            "competition": competition.get_text().strip(),
        }
        games.append(game)
print(games)

# DB connection
conn = sqlite3.connect("sh.db")
c = conn.cursor()

# Delete current games
c.execute("DELETE FROM Game")
# Insert new games
c.executemany(
    "INSERT INTO Game (date, home_team, away_team, url, competition) VALUES (:date, :home_team, :away_team, :url, :competition);",
    games,
)
conn.commit()

# Fetch games
data = {}

# Today games
c.execute("SELECT * FROM Game WHERE date(date) = date('now')")
rows = c.fetchall()
today = []

# extract column names
column_names = [d[0] for d in c.description]

for row in rows:
    info = dict(zip(column_names, row))
    today.append(info)

data["today"] = today

# Tomorrow games
c.execute("SELECT * FROM Game WHERE date(date) = date('now', '+1 day')")
rows = c.fetchall()
tomorrow = []

for row in rows:
    info = dict(zip(column_names, row))
    tomorrow.append(info)

data["tomorrow"] = tomorrow

# Generate JSON
with open("../app/src/data.json", "w") as f:
    json.dump(data, f)

# Add games file to repo
home_path = Path.home()
repo_path = home_path / "projects/super_hoquei"
repo = Repo(str(repo_path))

repo.git.add(update=True)
today = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
repo.index.commit(f"[Bot: {socket.gethostname()}] Update games file ({today})")
origin = repo.remote(name="origin")
origin.push()
