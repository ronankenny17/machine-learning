# walk forward validation split training loop
import numpy as np
from sklearn import pipeline
from sklearn.metrics import roc_auc_score , confusion_matrix

from data_pipeline.evaluate_model import evaluate_model

# will run loop incrementing the next year to be used for validation / testing 
#mimicks how data is collected irl over time and improved upon 

def walk_forward_validation(filtered_dataset, feature_cols, min_train_years=3, pipeline = None):
    """
    Module for componentising the walk forward validation loop.
    takes in the filtered dataset, the feature columns, the minimum number of years to train on, and the pipeline to be used for training and testing.
    """
    if pipeline is None:
        raise ValueError("Pipeline must be provided for walk forward validation.")
    results =[]

    years = sorted(filtered_dataset['year'].unique())
    for i in range(min_train_years, len(years)):
        train_years = years[:i]   
        test_year = years[i]      
        
        #split the dataframe based on the years
        train_df = filtered_dataset[filtered_dataset['year'].isin(train_years)]
        test_df = filtered_dataset[filtered_dataset['year'] == test_year]
        
        # Separate the features from the target answers 
        X_train = train_df[feature_cols]
        y_train = train_df['high_tries_scored']
        X_test = test_df[feature_cols]
        y_test = test_df['high_tries_scored']
        
        print(f"\n FOLD: Train {train_years} -> Test {test_year}")
        print(f"  Train: {len(train_df)} rows | Test: {len(test_df)} rows")

        # find most recent date in the current loop iterations training data
        anchor_date = train_df['game_date'].max()

        # recency based weighting 
        
        # calculate how many days ago each game was played
        days_ago = (anchor_date - train_df['game_date']).dt.days
        
        # create the weights - games from a year ago get half the weight
        weights = np.exp(-(np.log(2) / 365) * days_ago)


        # training 

        # fit model model 
        pipeline.fit(X_train, y_train, model__sample_weight=weights)

        predicted_labels = pipeline.predict(X_test)# how confident the model was in its class assignment
        predicted_probabilities = pipeline.predict_proba(X_test)[:, 1]# 0 or 1 high scoring or no
        evanluation_metrics = evaluate_model(predicted_labels, y_test, predicted_probabilities)
        confusion = confusion_matrix(y_test, predicted_labels, labels=[0, 1])

        results.append({
            'train_years': train_years,
            'test_year': test_year,
            'train_size': len(train_df),
            'test_size': len(test_df),
            'evaluation_metrics': evanluation_metrics,
            'confusion_matrix': confusion
        }
        )
        #print(results)
    return results 
