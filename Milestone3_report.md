## Milestone 3 Report

Ronan Kenny  
23404724

### Evaluation metrics

- two entries per model is because of the two folds (walk-forward-validation)

| Model | Test year | Train rows | Test rows | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Dummy baseline | 2025 | 4,204 | 1,033 | 0.560 | 0.000 | 0.000 | 0.000 | 0.500 |
| Dummy baseline | 2026 | 5,237 | 828 | 0.469 | 0.000 | 0.000 | 0.000 | 0.500 |
| Logistic regression | 2025 | 4,204 | 1,033 | 0.583 | 0.525 | 0.547 | 0.536 | 0.633 |
| Logistic regression | 2026 | 5,237 | 828 | 0.594 | 0.607 | 0.668 | 0.636 | 0.624 |
| Random forest | 2025 | 4,204 | 1,033 | 0.576 | 0.511 | 0.862 | 0.642 | 0.667 |
| Random forest | 2026 | 5,237 | 828 | 0.603 | 0.589 | 0.832 | 0.690 | 0.653 |
| Gradient boosting | 2025 | 4,204 | 1,033 | 0.582 | 0.515 | 0.857 | 0.644 | 0.681 |
| Gradient boosting | 2026 | 5,237 | 828 | 0.610 | 0.597 | 0.818 | 0.690 | 0.656 |


**Note: The 2026 test fold is partial-year data**


### Model Settings and tuning 
For all models I used an imputer as some of my data was incomplete (I discussed this in my data audit) and I used  median. I added the imputer into the pipeline to avoid data leakage. I needed scaling for the logistic regression model -i used standard scaling. 

All models use the same walk-forward-validation folds. training rows were weighted by recency. 

All models use the same walk-forward-validation folds. training rows were weighted by recency. 

| Model | Preprocessing | Estimator settings / search | Decision threshold |
|---|---|---|---:|
| Dummy baseline | Median imputation | `DummyClassifier(strategy="prior")` | 0.50 |
| Logistic regression | Median imputation; standard scaling | `max_iter=1000`, `C=1.0`, `class_weight={0: 1.0, 1: 1.5}` | 0.50 |
| Random forest | Median imputation; no scaling | Grid search over `n_estimators` = 50, 100, 200; `max_depth` = 5, 8, 10; `class_weight` = `"balanced"` or the four class-weight dictionaries in the notebook. `random_state=42` was fixed. | 0.45 |
| Histogram gradient boosting | Median imputation; no scaling | Grid search over `max_iter` = 100, 150, 200; `learning_rate` = 0.02, 0.03, 0.035; `max_depth` = 3, 4, 5; and `class_weight` = `"balanced"` or the three class-weight dictionaries in the notebook. `min_samples_leaf=25`, `l2_regularization=1.5`, and `random_state=42` were fixed. | 0.45 |

The random-forest and histogram-gradient-boosting searches use `GridSearchCV` with five `TimeSeriesSplit` folds and F1 scoring. The threshold is applied after fitting and is not part of the grid search. Recency sample weights use an exponential decay with a 365-day half-life.

#### Tuning
I setup automated tuning using grid search cross validation as part of sci-kit learn. This takes a dictionary of tuning parameters, options for their values and then a scoring metric to optimise for. it then tests out different combinations and returns the best performing model based on the chosen metric. 

I also lowered the decision boundary to 0.45 to capture more of the true positives. The default value is 0.5 so by setting it slightly below this will favor the positive case more. 

My models pre tuning in their base state were overly conservative in assinging the positive case (Highs_tries_scored==1 or tries>3 ), I had a high rate of false negatives. As such a lot of my tuning was to adjust for this. After tuning the models are now much better at correctly classifiying the right outcome, but at the cost that the opposite problem is now the  case where the models are classifiying more false positives. 

here is the tuning params I settled on: 
**Random forest classifier**
Fold 0: {'model__class_weight': 'balanced', 'model__max_depth': 5, 'model__n_estimators': 50} 
Fold 1:  {'model__class_weight': 'balanced', 'model__max_depth': 5, 'model__n_estimators': 50} 

**Gradient boosting classifier**
Fold 0:   {'model__class_weight': 'balanced', 'model__learning_rate': 0.035, 'model__max_depth': 3, 'model__max_iter': 200} 
Fold 1:  {'model__class_weight': 'balanced', 'model__learning_rate': 0.03, 'model__max_depth': 5, 'model__max_iter': 200} 


### Error analysis 

The tradeoff I found was that as the models became better at guessing if a team would score many tries in a given game, it predicted that was the case even when it was incorrect more often. Even with this caveat, after tuning the model is much better at the goal I am trying to achieve - predict if teams scored more than 3 tries in a game based on the stats. 

Many of the models errors were in games where the number of tries scored was exactly 3 which is right below the cutoff for high_tries_scored to be true. The majority of the false positives fell in this category.  However the in game statistics are similar to a game where teams could score more than that. 

Another source of error was with matches where teams had low possession and 22 entries but high kicks from hand (examples of teams following the newer tactical meta)
For example: 
**Team    team_vrs    tries   kicks_from_hand     Posession   actual_value    predicted**
Ireland   England	  5.0	    31.0	           0.48	9.0	    1	            0	
**probability result**
0.449858	false negative

This game from this years six nations is an example where Ireland had less position than their oppponents and not a high number of entries to the English 22 meter zone, which would be traditional indicators of a teams attack. However anyone who watched that game will tell you Ireland dominited, scoring 5 tries. This shows that based on the patterns the model learned on older data the model predicted that high_tries_scored would be false. 


### Conclusion 

One feature of the dataset that became apparent in the training folds was the rate of High_tries_scored across the first fold 2022-2025 compared to the second 2022-2026(ongoing). The base rate of High tries being true increased in the second fold which appeared in the change in  metrics across the two folds when evaluating the performance of the different models I tried out. This can be clearly seen in my error enalysis in my example of ireland vrs england. This is a real trend in the rugby world where teams are scoring more tries then before and many analysts attribute this to an increased kicking volume and a more 'aggressive' style of kicking teams today use. This is the relationship I wished to explore in this project this was expected and actually good to see. 

It would be interesting to see, as more statistics and data is collected under the newer kicking-oriented trends which are mainly only present in the 2026 fold, would the models performance improve as they would be better able to take into account the new trend. 

| Model | Test year | Train rows | Test rows | Accuracy | Precision | Recall | F1 | ROC-AUC |
	Random forest	2025	4204	1033	0.576	0.511	0.862	0.642	0.667
5	Random forest	2026	5237	828	0.603	0.589	0.832	0.690	0.653
6	Gradient boosting	2025	4204	1033	0.582	0.515	0.857	0.644	0.681
7	Gradient boosting	2026	5237	828	0.610	0.597	0.818	0.690	0.656


#### Best performing model 
Based on my testing results my best performing model was my gradient boosting classifier.  It matches or outperforms the next best model -random forest clasifier in its roc-auc and f1 scores across both folds. Random forest does have a better recall score but its accuray aand precision scores are lower. After tuning random fprest over adjusted for its early conservatism and is now over eager to predict a postive case (high recal lower accuracy). The gradient boosting classifier is more of a middle ground with still a good f1 score but fewer false positives. 