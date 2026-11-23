"""

"""


import pandas as pd


def get_error_info(results, dataset ,model_name, n=10, error_type=None):
    """
    
    function ot get the info on the top errors from the results of a given model 
    args:
    results - the evaluation results for the model 
    dataset- the training data set 
    model_name - the model 
    n - the number of results you want retured
    error_type - false potisive false negative 
    
    """
    predictions = pd.concat(
        [
            fold["prediction_details"].assign(test_year=fold["test_year"])
            for fold in results
        ],
        ignore_index=True,
    )

    # Add kicking volume for context if this model did not use it.
    if "kicks_from_hand" not in predictions.columns:
        kicking_stats = dataset[
            ["match_id", "team_id", "kicks_from_hand"]
        ].drop_duplicates(subset=["match_id", "team_id"])

        predictions = predictions.merge(
            kicking_stats,
            on=["match_id", "team_id"],
            how="left",
            validate="many_to_one",
        )

    errors = predictions.loc[predictions["error_type"] != "correct"].copy()

    if error_type is not None:
        errors = errors.loc[errors["error_type"] == error_type].copy()

    if errors.empty:
        print(f"No errors found for {model_name}.")
        return errors

    # Confidence assigned to the wrong class:
    # false positive -> probability of high tries
    # false negative -> probability of low tries
    errors["wrong_class_probability"] = errors["probability_high_tries"].where(
        errors["error_type"] == "false positive",
        1 - errors["probability_high_tries"],
    )

    errors["actual_class"] = errors["actual"].map({0: "0 (Low)", 1: "1 (High)"})
    errors["predicted_class"] = errors["predicted"].map({0: "0 (Low)", 1: "1 (High)"})
    errors["model"] = model_name

    columns = [
        "model", "test_year", "game_date", "team", "team_vs", "tries",
        "kicks_from_hand", "possession", "22m_entries",
        "actual_class", "predicted_class", "probability_high_tries",
        "error_type", "wrong_class_probability",
    ]
    columns = [column for column in columns if column in errors.columns]

    return errors.sort_values(
        "wrong_class_probability", ascending=False
    )[columns].head(n)



