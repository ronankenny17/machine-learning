


def filter_rows_with_required_data(df, required_columns):
    """
    helper function to filter out the rows in the dataset that dont have the neccessary columns 
    example required columns 
        required_columns = [
    "kicks_from_hand",
    "tries",
    "kick_percent_success",
    "territory",
    "possession",
    "22m_entries",
    ]
    """

    complete_rows = df.dropna(subset=required_columns).copy()
    return complete_rows
