## Model Evaluation

Ronan Kenny  
23404724

### Fold-level comparison

| Model | Test year | Train rows | Test rows | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Dummy baseline | 2025 | 4,204 | 1,033 | 0.560 | 0.000 | 0.000 | 0.000 | 0.500 |
| Dummy baseline | 2026 | 5,237 | 828 | 0.469 | 0.000 | 0.000 | 0.000 | 0.500 |
| Logistic regression | 2025 | 4,204 | 1,033 | 0.591 | 0.611 | 0.193 | 0.294 | 0.630 |
| Logistic regression | 2026 | 5,237 | 828 | 0.528 | 0.634 | 0.264 | 0.372 | 0.622 |
| Random forest | 2025 | 4,204 | 1,033 | 0.622 | 0.582 | 0.505 | 0.541 | 0.651 |
| Random forest | 2026 | 5,237 | 828 | 0.554 | 0.594 | 0.509 | 0.548 | 0.582 |
| Gradient boosting | 2025 | 4,204 | 1,033 | 0.629 | 0.624 | 0.398 | 0.486 | 0.678 |
| Gradient boosting | 2026 | 5,237 | 828 | 0.591 | 0.666 | 0.461 | 0.545 | 0.652 |

The 2026 test fold is partial-year data. Interpret comparisons involving that fold cautiously and report the fold results separately rather than relying only on an average.


### Model Settings and tuning 
For all models I used an imputer as some of my data was incomplete (I discussed this in my data audit) and I used  median. I added the imputer into the pipeline to avoid data leakage. I needed scaling for the logistic regression model -i used standard scaling. 

All models use the same walk-forward-validation folds. training rows were weighted by recency. 

I did not perform any tuning on the models parameters yet. I just used params I saw in examples online which will be my initial configurations. 

| Model | Settings |
|---|---|
| Dummy baseline | `strategy="prior"` |
| Logistic regression | `max_iter=1000`; other parameters use scikit-learn defaults |
| Random forest | `n_estimators=100`, `random_state=42`; other parameters use scikit-learn defaults |
| Gradient boosting | `n_estimators=100`, `learning_rate=0.1`, `max_depth=3`, `random_state=42`; other parameters use scikit-learn defaults |


### Error analysis 



### Conclusion 
