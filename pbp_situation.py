# Extract essential data from specific plays 
# Testing using pbp_2024_0.csv file right now

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

'''
x variables include:
1. Game Situation Variables (Critical)
down - Current down (1st, 2nd, 3rd, 4th)
ydstogo - Yards to go for first down
yardline_100 - Distance to opponent's end zone (field position)
goal_to_go - Binary flag if in goal-to-go situation
quarter_seconds_remaining - Time left in current quarter
game_seconds_remaining - Total time left in game
game_half - Half1 or Half2

2. Score and Win Probability Variables (Critical)
score_differential - Current point differential (positive = leading)
wp - Win probability (0-1)
vegas_wp - Vegas-adjusted win probability
ep - Expected points for current situation
posteam_timeouts_remaining - Timeouts left for offensive team
defteam_timeouts_remaining - Timeouts left for defensive team

3. Team and Matchup Variables (Important)
posteam - Possession team (offensive team)
defteam - Defensive team
posteam_type - Home or away team on offense
div_game - Divisional game flag

4. Formation and Personnel Variables (Important)
shotgun - Binary flag for shotgun formation
no_huddle - Binary flag for no-huddle offense
qb_dropback - Binary flag indicating QB dropped back

5. Environmental Variables (Moderately Important)
roof - Stadium type (outdoors, dome, retractable)
surface - Field surface (grass, turf)
temp - Temperature in Fahrenheit
wind - Wind speed in mph
weather - Weather description

6. Drive Context Variables (Moderately Important)
drive_play_count - Number of plays in current drive
drive_time_of_possession - Time of possession for current drive
drive_start_yard_line - Starting field position of drive
ydsnet - Net yards gained on current drive

7. Historical Performance Variables (Advanced)
total_home_rush_epa / total_away_rush_epa - Cumulative rushing EPA
total_home_pass_epa / total_away_pass_epa - Cumulative passing EPA
series_success - Success rate in current series
cp - Completion probability (for pass plays)
cpoe - Completion percentage over expected

8. Coaching and Personnel Variables (Useful)
home_coach / away_coach - Head coaches
passer_player_name - Starting QB
season_type - Regular season, playoffs, etc.
week - Week of the season

9. Betting Market Variables (Contextual)
spread_line - Point spread
total_line - Over/under total
vegas_home_wp - Vegas home team win probability
'''

'''
y variables include:
play_type, run_location, pass_length, pass_type
'''

def successful_play(situation): 
    ''' Determines if a play was successful based on the outcome of the play '''

    is_successful = 0










    return is_successful


def train_model(X, y):
    # Split the data between X and y
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Handle categorical columns for the X values (non-numeric data)
    # (E.g. posteam="KC" becomes posteam_KC=1, all other team columns = 0)
    categorical_cols = ['posteam', 'defteam']
    X_train_encoded = pd.get_dummies(X_train, columns=categorical_cols, drop_first=True) # Using pd.get_dummies (one-hot encoding)
    X_test_encoded = pd.get_dummies(X_test, columns=categorical_cols, drop_first=True)
    X_train_encoded, X_test_encoded = X_train_encoded.align(X_test_encoded, join='left', axis=1, fill_value=0) # Make sure train and test have same columns (important!)

    print(f"Training data shape before cleaning: {X_train_encoded.shape}")
    print(f"Test data shape before cleaning: {X_test_encoded.shape}")
    print()

    # Drop rows with missing values 
    train_complete_idx = X_train_encoded.dropna().index.intersection(y_train.dropna().index)
    X_train_clean = X_train_encoded.loc[train_complete_idx]
    y_train_clean = y_train.loc[train_complete_idx]
    test_complete_idx = X_test_encoded.dropna().index.intersection(y_test.dropna().index) # Do the same for test data
    X_test_clean = X_test_encoded.loc[test_complete_idx]
    y_test_clean = y_test.loc[test_complete_idx]

    print(f"Training data shape after cleaning: {X_train_clean.shape}")
    print(f"Test data shape after cleaning: {X_test_clean.shape}")
    print()

    # Create and train the model 
    model = RandomForestClassifier(n_estimators=100, random_state=42) # Initialize the classifier
    model.fit(X_train_clean, y_train_clean) # Train the model
    y_pred = model.predict(X_test_clean) # Make predictions on test set
    accuracy = accuracy_score(y_test_clean, y_pred) # Calculate accuracy
    
    # Print accuracy
    print(f"Model accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test_clean, y_pred))
    print()
    
    # Return the trained model for later use
    return model, X_train_clean.columns.tolist()  # Also return column names for later predictions


def predict_play(situation, trained_model, feature_columns):
    ''' Use the situation to determine the most optimal play type '''

    # Print the situation input (remove some print statements)
    # X = df_filtered[['down', 'ydstogo', 'yardline_100', 'goal_to_go', 'quarter_seconds_remaining',
    #         'half_seconds_remaining', 'game_seconds_remaining', 'score_differential', 'wp',
    #         'ep', 'posteam_timeouts_remaining', 'defteam_timeouts_remaining', 'posteam', 'defteam']]

    # Print the current situation
    print(f"Down: {situation[0]}")
    print(f"Yards to go: {situation[1]}")
    print(f"Distance to end zone: {situation[2]}")
    print(f"Goal to go: {situation[3]}")
    print(f"Quarter seconds remaining: {situation[4]}")
    print(f"Half seconds remaining: {situation[5]}")
    print(f"Game seconds remaining: {situation[6]}")
    print(f"Score differential: {situation[7]}")
    print(f"Win probability: {situation[8]}")
    print(f"Expected points: {situation[9]}")
    print(f"Offensive team timeouts remaining: {situation[10]}")
    print(f"Defensive team timeouts remaining: {situation[11]}")
    print(f"Offensive team: {situation[12]}")
    print(f"Defensive team: {situation[13]}")
    print()

    # Convert input to DataFrame with correct column names
    situation_df = pd.DataFrame([situation], columns=['down', 'ydstogo', 'yardline_100', 'goal_to_go', 'quarter_seconds_remaining', 
                                                      'half_seconds_remaining', 'game_seconds_remaining', 'score_differential', 'wp', 
                                                      'ep', 'posteam_timeouts_remaining', 'defteam_timeouts_remaining', 'posteam', 'defteam'])

    # Apply same categorical encoding as training
    categorical_cols = ['posteam', 'defteam']
    situation_encoded = pd.get_dummies(situation_df, columns=categorical_cols, drop_first=True)
    
    # Make sure it has all the same columns as training data
    for col in feature_columns:
        if col not in situation_encoded.columns:
            situation_encoded[col] = 0
    
    # Reorder columns to match training data
    situation_encoded = situation_encoded[feature_columns]

    # Predict the most optimal play type
    prediction = trained_model.predict(situation_encoded)
    prediction_proba = trained_model.predict_proba(situation_encoded)

    print("======================================")
    print(f"Predicted Play Type: {prediction}")
    print(f"Confidence {prediction_proba}")
    print()
    
    return prediction[0], prediction_proba[0]  # Return prediction and confidence


if __name__ == "__main__":
    ''' Eventually will replace 'if name == main' with a function that will be called via a Flask endpoint ''' 

    # Open the 2024 Play-by-Play CSV file (First Part)
    df = pd.read_csv("Data/pbp_2024_0.csv")
    print(df.columns.to_list())
    print(df.head())
    
    # Filter columns that only contain "run" or "pass" for play_type
    df_filtered = df[df['play_type'].isin(['run', 'pass'])]

    #TODO: Determine if a play was successful (for the y-variables)

    # (game situation) x variables using categories 1-3 for now
    X = df_filtered[['down', 'ydstogo', 'yardline_100', 'goal_to_go', 'quarter_seconds_remaining',
            'half_seconds_remaining', 'game_seconds_remaining', 'score_differential', 'wp',
            'ep', 'posteam_timeouts_remaining', 'defteam_timeouts_remaining', 'posteam', 'defteam']]
    print(X.head(10))

    # y variable, play type will be "run" or "pass" for now
    y = df_filtered['play_type']
    print(y.head(10))

    trained_model, feature_columns = train_model(X, y)
    print(feature_columns)
    print()

    # Test situations to predict play type - [down, ydstogo, yardline_100, goal_to_go, quarter_seconds_remaining, half_seconds_remaining, game_seconds_remaining, score_differential, wp, ep, posteam_timeouts_remaining, defteam_timeouts_remaining, posteam, defteam]
    
    # 2nd & 5 from opponent's 30-yard line, early 2nd quarter, tied game, balanced situation
    test_case_1 = [2, 5, 30, 0, 720, 1620, 2520, 0, 0.52, 1.8, 3, 3, 'KC', 'BUF']
    
    # 3rd & 8 from midfield, late 3rd quarter, down by 3, passing situation
    test_case_2 = [3, 8, 50, 0, 180, 1080, 1080, -3, 0.42, 0.8, 2, 3, 'GB', 'DAL'] 
    
    # 1st & 10 from own 25-yard line, early 1st quarter, ahead by 7, balanced situation
    test_case_3 = [1, 10, 75, 0, 480, 1380, 3180, 7, 0.62, -0.4, 3, 3, 'SF', 'SEA']
    
    # 1st & Goal from 8-yard line, late 4th quarter, down by 4, red zone situation  
    test_case_4 = [1, 8, 8, 1, 95, 95, 95, -4, 0.15, 4.2, 1, 2, 'PHI', 'NYG']
    
    # 4th & 2 from opponent's 35, late 4th quarter, down by 6, desperation situation
    test_case_5 = [4, 2, 35, 0, 45, 45, 45, -6, 0.05, 1.2, 0, 1, 'TB', 'DET']

    # 3rd & 1 from own 40, mid 2nd quarter, tied game, short yardage situation
    test_case_6 = [3, 1, 60, 0, 600, 1200, 1800, 0, 0.50, 0.5, 2, 2, 'MIA', 'NYJ']

    # Tush Push Situation for the Eagles
    test_case_7 = [1, 1, 1, 1, 600, 600, 2400, 0, 0.50, 0.5, 2, 2, 'PHI', 'SF']

    predict_play(test_case_1, trained_model, feature_columns)
    predict_play(test_case_2, trained_model, feature_columns)
    predict_play(test_case_3, trained_model, feature_columns)
    predict_play(test_case_4, trained_model, feature_columns)
    predict_play(test_case_5, trained_model, feature_columns)
    predict_play(test_case_6, trained_model, feature_columns)
    predict_play(test_case_7, trained_model, feature_columns)