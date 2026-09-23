

"""
Script to test out and explore the rugbypy package 
ronan kenny 
"""

#import rugbypy as rp
import pandas as pd 
from rugbypy.match import *
from rugbypy.team import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)


def get_team_id(team):
    if isinstance(team, dict):
        return team.get("id") or team.get("team_id")

    return getattr(team, "id", None) or getattr(team, "team_id", None)


all_teams = fetch_all_teams()
if isinstance(all_teams, pd.DataFrame):
    teams = all_teams.to_dict("records")
elif isinstance(all_teams, dict):
    teams = list(all_teams.values())
else:
    teams = list(all_teams)

all_team_stats = []
total_rows = 0
successful_teams = 0

for team in teams:
    team_id = get_team_id(team)
    if not team_id:
        print(f"Skipping team without an ID: {team}")
        continue

    try:
        team_stats = fetch_team_stats(team_id=team_id)
        all_team_stats.append(team_stats)
        row_count = len(team_stats)
        total_rows += row_count
        successful_teams += 1
        print(f"Team {team_id}: {row_count} rows")
    except Exception as error:
        print(f"Could not fetch team {team_id}: {error}")

print(f"\nTeams processed: {successful_teams}/{len(teams)}")
print(f"Total rows across all teams: {total_rows}")

if all_team_stats:
    all_match_stats = pd.concat(all_team_stats, ignore_index=True)
    possible_match_id_columns = {
        "match_id"
    }
    match_id_columns = [
        column for column in all_match_stats.columns
        if column in possible_match_id_columns
        or ("match" in column.lower() and "id" in column.lower())
        or ("fixture" in column.lower() and "id" in column.lower())
    ]

    if match_id_columns:
        match_id_column = match_id_columns[0]
        unique_matches = all_match_stats[match_id_column].nunique()
        print(f"Match ID column: {match_id_column}")
        print(f"Unique matches: {unique_matches}")
    else:
        print("Could not find a match ID column.")
        print("Available columns:", all_match_stats.columns.tolist())

def print_field(field):
    try:
        print("--- Fetching Match Summary Data ---")
        # Fetch team/match statistics table
        
        print(f"Match Stats Shape: {field.shape}")
        print("\nColumns available in Match details:")
        print(field.columns.tolist())
        
        # Check specifically for columns containing 'kick'
        kick_cols = [col for col in field.columns if 'kick' in col.lower()]
        print("\nColumns related to kicking in Match Stats:", kick_cols)

    except Exception as e:
        print(f"Could not fetch match stats directly: {e}")

