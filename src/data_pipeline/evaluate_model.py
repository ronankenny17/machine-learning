"""
Module to control how the model is evaluated. 

"""
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def evaluate_model(predicted_labels, y_test, predicted_probabilities):
    """
    Evaluates the model's performance using various metrics.
    
    Args:
        predictions (array-like): The predicted values from the model.
        y_test (array-like): The true values for the test set.
        predicted_probabilities (array-like): The predicted probabilities from the model.
        
    Returns:
        dict: A dictionary containing evaluation metrics.
    """
    
    evaluation_metrics = {
        'accuracy': accuracy_score(y_test, predicted_labels),
        'precision': precision_score(y_test, predicted_labels),
        'recall': recall_score(y_test, predicted_labels),
        'f1_score': f1_score(y_test, predicted_labels),
        'roc_auc': roc_auc_score(y_test, predicted_probabilities)
    }
    
    return evaluation_metrics
