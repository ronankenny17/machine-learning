## Data Audit 
Initial Observations of the data:

### Dataset shape and unit of observation

**For processed data**:
Rows with all required fields: 6065
Current data shape: (6065, 58)


**Variable types**
dtypes: float64(51), object(7)


**Target distribution**
Create the proposed binary target, High_Tries_scored (1 if tries > 3, otherwise 0), then report the count and percentage in each class. This lets you see whether the classes are imbalanced. Do this for the dataset you actually plan to model, and make clear how rows with missing tries are handled.



**Notes on Rugbypy Dataset**

1. **The structure of the match data**
	The data is structured so that first you have to get every team. Each team has their information about the games they played. There is no singular dataset/ table containing all the info of a given game. Instead, each team stores only their own info about the games they played. 
	
2. **The data has different Keys for the same information** 
	the dataset pulls data from different competitions sources which probably use different data key schemas eh the URC or The Top 14. These different schemes present themselves in the data through the duplicates of the same statistics under different names. 
	eg metres_carried and metres_run or tackles_missed and missed_tackles. 
	As such as part of pre-processing I will have to go through my data and consolidate the differing datatypes into a single entry before training.  
	
3. **Rows represent teams, not whole matches**
	Each row describes one team’s performance in one match. A match ID is therefore shared by the two teams’ rows.

5. **Missing values and filtering**
	The combined dataset contains 13,677 team-match rows. The tries value is recorded for 7,122 rows and missing for 6,555 rows (47.9%). kicks_from_hand is recorded for 9,955 rows. The overlap—rows where both tries and kicks_from_hand are recorded is 6,065. These two columns are neccessary for my project as tries is what I will use for evaluating my model. Kicks_from_hand is the main feature my model will base its inference on. 

	other statistics are less present aswell such as kick_percent_success and territory are each recorded for 3,596 rows, while possession is recorded for 7,122 and 22m_entries for 9,291. Requiring all six fields (tries, kicks_from_hand, kick_percent_success, territory, possession, and 22m_entries) leaves 2,932 rows. Missing values indicate that the statistic is unavailable in the dataset; they are not assumed to mean zero. 

	As my main baseline dataset before my training / validation/ testing split I will just require values for the tries and kicks_from_hand columns so I will have a larger dataset to work with. Other statistics will be used for training when theyre present.


