## Data Audit 
Initial Observations of the data:

### Dataset shape and unit of observation

**For processed data**:
Rows with all required fields: 6065
Current data shape: (6065, 58)


**Variable types**
dtypes: float64(51), object(7)


**Target distribution**
 target distribution : high_tries_scored
0    0.592 - less than or equal to 3 tries scored in the game = low 
1    0.408 - greater than 3 tries scored in the game = high 
Name: proportion, dtype: float64


**Duplicate Assessment**
there are entries with duplicate match id values in my dataset. For every single match played there is two entries. One entry per team who played which contains the data for that team only and then the overall score and some high level info about the opposition. 
output of a coded duplicate check

Exact duplicate rows: 0
Duplicate match_id + team_id groups: 0
Rows in those groups: 0
Matches with other than 2 rows: 146
Rows missing match_id: 0
Rows missing team_id: 0
tries: min=0.0, median=3.0, max=16.0, negative values=0, IQR outlier flags=296
kicks_from_hand: min=0.0, median=24.0, max=58.0, negative values=0, IQR outlier flags=253
kick_percent_success: min=0.0, median=0.78, max=1.0, negative values=0, IQR outlier flags=110
territory: min=0.0, median=0.5, max=1.0, negative values=0, IQR outlier flags=93
possession: min=0.0, median=0.57, max=96.0, negative values=0, IQR outlier flags=0
22m_entries: min=0.0, median=9.0, max=25.0, negative values=0, IQR outlier flags=31
kick_percent_success: values outside 0-100 = 0
territory: values outside 0-100 = 0
possession: values outside 0-100 = 0

**Missingness**
Of the original dataset I filtered out rows that were missing values for my two neccessary features : kicks_from_hand and tries which left 6065 rows. 

output of a missingness check on the 6065 rows
Column						missing_count  missing_percent
kicks_from_hand                 0.0              0.0
kick_percent_success         2469.0             40.7
territory                    2469.0             40.7
possession                      0.0              0.0
22m_entries                   664.0             10.9

other features which were not were sometimes missing and so were imputed as part of the pipeline simpleImputer(strategy = 'median')

**Notes on Rugbypy Dataset**

1. **The structure of the match data**
	The data is structured so that first you have to get every team. Each team has their information about the games they played. There is no singular dataset/ table containing all the info of a given game. Instead, each team stores only their own info about the games they played. 
	
2. **The data has different Keys for the same information** 
	the dataset pulls data from different competitions sources which probably use different data key schemas eh the URC or The Top 14. These different schemes present themselves in the data through the duplicates of the same statistics under different names. 
	eg metres_carried and metres_run or tackles_missed and missed_tackles. 
	As such as part of pre-processing I will have to go through my data and consolidate the differing datatypes into a single entry before training.  
	
3. **Rows represent teams, not whole matches**
	Each row describes one team’s performance in one match. A match ID is therefore shared by the two teams’ rows.

4. **Handling possession percantage**
	different data sources store a teams percentage possesion as a float between 0-1 or as an int between 0-100 . i normalised them to both be values between 0-1

5. **Missing values and filtering**
	The combined dataset contains 13,677 team-match rows. The tries value is recorded for 7,122 rows and missing for 6,555 rows (47.9%). kicks_from_hand is recorded for 9,955 rows. The overlap—rows where both tries and kicks_from_hand are recorded is 6,065. These two columns are neccessary for my project as tries is what I will use for evaluating my model. Kicks_from_hand is the main feature my model will base its inference on. 

	other statistics are less present aswell such as kick_percent_success and territory are each recorded for 3,596 rows, while possession is recorded for 7,122 and 22m_entries for 9,291. Requiring all six fields (tries, kicks_from_hand, kick_percent_success, territory, possession, and 22m_entries) leaves 2,932 rows. Missing values indicate that the statistic is unavailable in the dataset; they are not assumed to mean zero. 

	As my main baseline dataset before my training / validation/ testing split I will just require values for the tries and kicks_from_hand columns so I will have a larger dataset to work with. Other statistics will be used for training when theyre present.


