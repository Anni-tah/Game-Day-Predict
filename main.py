import requests
import os
from datetime import date
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

class FootballAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS

    def get_todays_matches(self, league_id=None, season=None):
        today = date.today().strftime("%Y-%m-%d")
        url = f"{self.base_url}/fixtures"
        params = {"date": today}
        if league_id:
            params["league"] = league_id
        if season:
            params["season"]= season

        print("Requesting:", url)
        print("Params:", params)

        response = requests.get(url, headers=self.headers, params=params)
        print("Status code:", response.status_code)

        if response.status_code != 200:
            print("❌ Failed to fetch matches:", response.status_code)
            return []

        data = response.json()
        

        return data.get("response", [])

def display_matches_grouped_by_league(matches):
    if not matches:
        print('⚠️ No matches found today.')
        return

    grouped = defaultdict(list)

    for m in matches:
        league_name = m['league']['name']
        grouped[league_name].append(m)

    today = date.today().strftime("%Y-%m-%d")
    print(f"\n⚽ Today's Matches ({today}):\n")

    for league_name, league_matches in grouped.items():
        country = league_matches[0]['league']['country']
        print(f"*** {league_name} - {country} ***")
        for match in league_matches:
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            time = match['fixture']['date'][11:16]
            print(f"{time} - {home} vs {away}")
        print()

if __name__ == "__main__":
    # First try fetching all today's matches (no league filter)
    print("*** Testing with no league filter ***")
    api = FootballAPI()
    matches = api.get_todays_matches()
    display_matches_grouped_by_league(matches)

    # Now fetch matches filtered by specific leagues and seasons
    print("***Testing with league filter ***")
    leagues = [
        {"id": 164, "name": "Kenya Premier League", "season": 2024},
        {"id": 39, "name": "English Premier League", "season": 2024},
        {"id": 140, "name": "La Liga", "season": 2024},
        {"id": 78, "name": "Bundesliga", "season": 2024},
    ]
