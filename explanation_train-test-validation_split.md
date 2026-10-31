## Explanation for training validation split method
Ronan kenny
23404724

**Chosen split method:** walk forward validation split 

I was worried a standard time based split (eg training is one year and validation is the next year ) would not be able to handle the changing 'tactical metas' of the game ie concept drift.
The meaning of a high kicking score in 2020 could be very different to what it means in 2025.
so I decided to go with a walk forward validation split 
instead of standard k fold validation which samples at random and doesnt take this into account 

this split method mimicks how actually training data wouldve been integrated into the pipeline over time so the model is trained as if it wouldve been from the beginning of the dataset. It should be better at taking into account modern shifts in trends that may appear in the data. 

Fold 1: Train [2020-2022] ──► Test [2023]
Fold 2: Train [2020-2023] ──► Test [2024]
Fold 3: Train [2020-2024] ──► Test [2025]
Fold 4: Train [2020-2025] ──► Test [2026]

I also added recency based weighting where more recent years (more relevant tactically) will be weighted higher than older years. 

The goal is to make my model better at taking into account the changing trends in the rugbypy dataset which develop over time with a bias towards most up to date trends. 

references: 
https://medium.com/@ahmedfahad04/understanding-walk-forward-validation-in-time-series-analysis-a-practical-guide-ea3814015abf
