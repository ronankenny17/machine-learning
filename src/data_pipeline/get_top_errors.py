"""
module to filter through a results data and then find the top errors
then displays them for error analysis. 
"""

from IPython.display import display

def get_top_errors(results , fold_year, num_errors=10):
    """
    finds the top errors (based on the porbability of the prdicted label)
    args: 
    results
    fold_year 
    num_errorsS
    """
    
    fold_results = next(
    result for result in results
    if int(result["test_year"]) == fold_year
    )

    details = fold_results["prediction_details"]

    print(details["error_type"].value_counts())
    display(details.query("error_type != 'correct'").head(num_errors))