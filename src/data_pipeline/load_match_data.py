"""
module to get the high level match data from the rugbypy lib
this data contains the follwoing columns:
['match_id', 'date', 'kickoff_time', 'season', 'competition_id', 
'competition', 'venue_id', 'venue', 'city_played', 'home_team', 
'away_team', 'home_team_id', 'away_team_id', 'home_score', 'away_score', 
'completed', 'is_tournament', 'played_on_grass', 
'attendance', 'home_team_form', 'away_team_form', 'referee']
"""


import pandas as pd
from rugbypy.match import fetch_all_matches, fetch_match_details

pd.set_option('display.max_columns', None)


def load_match_data(match_id: str = None) -> pd.DataFrame:
    """
    Load match data from the rugbypy library.

    Parameters:
    match_id (str, optional): The ID of the specific match to fetch details for.

    Returns:
    pd.DataFrame: A DataFrame containing the match data.
    """
    try:
        match_detail = fetch_match_details(match_id=match_id)
        if isinstance(match_detail, pd.DataFrame):
            return match_detail

    except Exception as e:
        print(f"Error fetching match details for match_id {match_id}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    
    return pd.DataFrame()  # Return an empty DataFrame if no match_id is provided
    
