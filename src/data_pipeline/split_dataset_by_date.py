"""
module for splitting the dataset into training , validation and testing 
the split will be based on the year the game was played in. 

"""
import pandas as pd

def split_dataset_by_date(df, start_date, end_date):
    """
    module for splitting the dataset into training , validation and testing 
    the split will be based on the year the game was played in. 

    """
    result = df.copy()
    # parse string values such as "20250215" into dates
    dates = pd.to_datetime(
        result["game_date"].astype("string"),
        format="%Y%m%d",
        errors="coerce",
    )

    if dates.isna().any():
        raise ValueError("game_date value was NAN")

    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")


    return result.loc[dates.between(start_date, end_date)]

    

    


