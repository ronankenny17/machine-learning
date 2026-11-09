from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

def generate_confusion_matrix(result_confusion_matrix):
    """
    Generate a confusion matrix given true labels and predicted labels.

    Parameters:
    y_true (array-like): True labels.
    y_pred (array-like): Predicted labels.

    Returns:
    np.ndarray: Confusion matrix.
    """
    
    display = ConfusionMatrixDisplay(
        confusion_matrix=result_confusion_matrix,
        display_labels=["Low tries (0-3)", "High tries (>3)"],
    )

    display.plot(cmap="Blues", values_format="d")
    plt.title("Gradient Boosting Confusion Matrix - 2025 Test Fold")
    plt.show()