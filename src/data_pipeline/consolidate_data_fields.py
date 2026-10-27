"""

The data has different Keys for the same information
the dataset pulls data from different competitions sources which probably use 
different data key schemas eh the URC or The Top 14. 
These different schemes present themselves in the data through the duplicates of the 
same statistics under different names. eg metres_carried and metres_run or tackles_missed and missed_tackles. 
As such as part of pre-processing I will have to go through my data 
and consolidate the differing datatypes into a single entry before training.

This module is for consolidating the data fields into a single field for each statistic. 
"""
import pandas as pd 
import numpy as np

def consolidate_data_fields(df ):
    """
    Consolidates duplicate data fields in the DataFrame into a single field for each statistic.

    Args:
        df (pd.DataFrame): The input DataFrame containing match statistics.
    """
    df = df.copy()

    column_mappings={
        'conversion_goals': ['conversion_goals', 'conversions'],
        'kicks_from_hand': ['kicks_from_hand', 'kicks'],
        'carries': ['carries', 'runs'],
        'metres_carried': ['metres_carried', 'meters_run'],
        'offloads': ['offloads', 'offload'],
        'clean_breaks': ['clean_breaks', 'line_breaks'],
        'tackles_made': ['tackles_made', 'tackles'],
        'tackles_missed': ['tackles_missed', 'missed_tackles'],
        'turnovers_won': ['turnovers_won', 'turnovers'],
    }

    for consolidated_col, candidate_cols in column_mappings.items():
        # check which alternative cols names that are actually in the df
        available_cols = [col for col in candidate_cols if col in df.columns ]

        # only run if the entry has two versions of the same data 
        if len(available_cols) > 1:
            cols0_data = df[available_cols[0]]
            cols1_data = df[available_cols[1]]
            

            combined = np.where(cols0_data.isna() | (cols0_data ==0), cols1_data, cols0_data)
            df[consolidated_col] = combined

            # Drop the redundant secondary column if it differs from the canonical name
            cols_to_drop = [col for col in available_cols if col != consolidated_col]
            df = df.drop(columns=cols_to_drop)

        
        # if there was only one version of the data present rename to our chosen uniform name 
        elif len(available_cols) == 1:
            if available_cols[0] != consolidated_col:
                df = df.rename(columns={available_cols[0]: consolidated_col})

    return df