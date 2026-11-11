# walk forward validation split training loop
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV

from data_pipeline.evaluate_model import evaluate_model
from data_pipeline.collect_prediction_details import collect_prediction_details

# will run loop incrementing the next year to be used for validation / testing 
#mimicks how data is collected irl over time and improved upon 

def walk_forward_validation(filtered_dataset, feature_cols, min_train_years=3,custom_threshold = 0.5, tuning_params = {}, pipeline = None):
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


        # find most recent date in the current loop iterations training data
        anchor_date = train_df['game_date'].max()

        # recency based weighting 
        
        # calculate how many days ago each game was played
        days_ago = (anchor_date - train_df['game_date']).dt.days
        
        # create the weights - games from a year ago get half the weight
        weights = np.exp(-(np.log(2) / 365) * days_ago)

        # training 

        # use automated hyperparameter tuning if tuning parameters are provided
        if tuning_params:   
            tuner = GridSearchCV(
                pipeline, 
                param_grid=tuning_params,
                cv=TimeSeriesSplit(n_splits=5), 
                scoring='f1', 
                n_jobs=-1
                )
            
            tuner.fit(X_train, y_train, model__sample_weight=weights)

            # update pipelien to use the best found tuned model
            pipeline = tuner.best_estimator_


        # fit model model 
        pipeline.fit(X_train, y_train, model__sample_weight=weights)

        #predicted_labels = pipeline.predict(X_test)# how confident the model was in its class assignment
        predicted_probabilities = pipeline.predict_proba(X_test)[:, 1]# 0 or 1 high scoring or no
        predicted_labels = (predicted_probabilities >= custom_threshold).astype(int)

        # for error analysis, collect the prediction details for each test instance
        prediction_details = collect_prediction_details(y_test, predicted_labels, predicted_probabilities, test_df, feature_cols)

        
        evanluation_metrics = evaluate_model(predicted_labels, y_test, predicted_probabilities)
        confusion = confusion_matrix(y_test, predicted_labels, labels=[0, 1])

        results.append({
            'train_years': train_years,
            'test_year': test_year,
            'train_size': len(train_df),
            'test_size': len(test_df),
            'evaluation_metrics': evanluation_metrics,
            'confusion_matrix': confusion,
            'prediction_details': prediction_details,
            'tuned_params': tuner.best_params_ if tuning_params else None,
        }
        )
        #print(results)
    return results 
