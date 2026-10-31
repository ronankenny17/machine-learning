## Ronan Kenny Machine Learning Project 
repository link: https://github.com/ronankenny17/machine-learning


## Project outline 
Does open play kicking volume and efficiency significantly increase the probability of a team scoring a lot of tries (>3) in their games? 


My aim is to train a model that can classify if based on given kicking statistics from a rugby match the model can predict if a team scored a High (>3)  or Low amount of tries in a game. This should count as being a binary Classification problem where the model will guess if the team scored greater than 3 tries in the game or not. 

I choose greater than 3 tries in a game for a team as in rugby typically when you score 4 tries you get rewarded with a bonus point for reaching that threshold in most rugby leagues regardless of if you win or not. As such this is the standard in professional rugby for a high scoring team in a game. 

### Project Setup

First you have to setup a python virtual environment to be able to run the jupyter notebook. 

Run the following commands in your terminal:
```

# setup venv and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```
The notebook is in the src directory. When running the notebook select the local env as the kernel to run it in. You should then be able to run it. 