"""
Module to load team data from the rugbypy package and extract match statistics for all teams.
"""


import pandas as pd 
#from rugbypy.match import 
from rugbypy.team import fetch_all_teams, fetch_team_stats

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

def get_team_id(team):
    if isinstance(team, dict):
        return team.get("id") or team.get("team_id")

    return getattr(team, "id", None) or getattr(team, "team_id", None)


def fetch_all_team_data():
    """
    pulls and extracts match statistics for all teams in the rugbypy package

    returns {
    all_match_stats: pd.DataFrame,
    all_team_stats: list of pd.DataFrame,
    total_rows: int,
    successful_teams: int
    } 
    """
    all_teams = fetch_all_teams()# method from rugbypy.team to fetch all teams
    all_match_stats = pd.DataFrame()  # Initialize an empty DataFrame for all match stats


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
            if team_stats is not None and not team_stats.empty:
                all_team_stats.append(team_stats)
                row_count = len(team_stats)
                total_rows += row_count
                successful_teams += 1
                print(f"Team {team_id}: {row_count} rows")

        except Exception as error:
            print(f"Could not fetch team {team_id}: {error}")

    if all_team_stats:
        all_match_stats = pd.concat(all_team_stats, ignore_index=True)

    return {
        "all_match_stats": all_match_stats if all_team_stats else pd.DataFrame(),
        "all_team_stats": all_team_stats,
        "total_rows": total_rows,
        "successful_teams": successful_teams,
    }


