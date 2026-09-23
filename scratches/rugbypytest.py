
import rugbypy as rp
import pandas as pd 
from rugbypy.match import *
from rugbypy.team import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

team_stats = fetch_team_stats(team_id="165b36e5")
#print(team_stats)
fetch_all_teams()

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


print_field(team_stats)