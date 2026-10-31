"""
Module for adding the target column to my dataset
this will be high_tries_scored which is a binary field 
it will be 1 if a team scored more than 3 tries in a given game 
otherwise it will be 0 ie when they did not score a 'high amount' of tries in the game
"""

def create_target_col(df):
    """
    function for adding the target column to my dataset
    this will be high_tries_scored which is a binary field 
    it will be 1 if a team scored more than 3 tries in a given game 
    otherwise it will be 0 ie when they did not score a 'high amount' of tries in the game

    """  

    if "tries" not in df.columns:
        raise KeyError("Required column 'tries' is missing")

    if df["tries"].isna().any():
        raise ValueError("Filter out rows with missing tries before creating target")
    
    result = df.copy()

    result["high_tries_scored"]  = (result['tries'] > 3).astype(int) 
    # set the boolean value of the check to an int 

    return result 
