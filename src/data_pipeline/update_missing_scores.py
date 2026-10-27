"""
Module for correcting missing scores in match data using component calculations
tries to fill in the missing value for the teams score by simply adding the tries, penalties and conversions together.

"""
import pandas as pd
from rugbypy.match import fetch_all_matches

def update_missing_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing 'score' and 'team_vs_score' values using:
    1. Component calculation (tries * 5 + conversions * 2 + penalties * 3 + drops * 3)
    2. Bulk match table lookup via fetch_all_matches()
    """
    df = df.copy()

    # try to calulate the score by adding the tries, penalties and conversions together
    convs = df['conversion_goals'].fillna(df.get('conversions', 0)).fillna(0)
    tries = df['tries'].fillna(0)
    penalties = df['penalty_goals'].fillna(0)
    drops = df['drop_goals'].fillna(0)
    pen_tries = df['penalty_tries'].fillna(0)

    
    calculated_score = (tries * 5) + (convs * 2) + (penalties * 3) + (drops * 3) + (pen_tries * 7)

    df['score'] = df['score'].fillna(calculated_score)

    return df