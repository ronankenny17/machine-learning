"""
Module to collect prediction error data from model predictions for analysis 

"""
import numpy as np

def collect_prediction_details(y_test, predicted_labels, predicted_probabilities, test_df, feature_cols):

    prediction_details = test_df[
        ["game_date", "match_id", "team", "team_id", "team_vs", "tries", *feature_cols]
    ].copy()

    prediction_details["actual"] = y_test.to_numpy()
    prediction_details["predicted"] = predicted_labels
    prediction_details["probability_high_tries"] = predicted_probabilities
    prediction_details["error_type"] = np.select(
        [
            (prediction_details["actual"] == 0) & (prediction_details["predicted"] == 1),
            (prediction_details["actual"] == 1) & (prediction_details["predicted"] == 0),
        ],
        ["false positive", "false negative"],
        default="correct",
    )
    return prediction_details

