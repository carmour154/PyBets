import pandas as pd 
import json 
from IPython.display import display
import datetime

def load_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_dataframe(data):
    df = pd.DataFrame(data)
    return df






def extract_moneyline_odds(main_df, bookmaker_key):
    # Prepare lists to hold extracted data
    sport_list = []
    game_id_list = []
    book_list = []
    home_team_list = []
    away_team_list = []
    home_team_odds_list = []
    away_team_odds_list = []

    # Iterate through each row in the DataFrame
    for index, row in main_df.iterrows():
        current_sport = row['sport_title']
        current_game_id = row['id']
        current_home_team = row['home_team']
        current_away_team = row['away_team']
        bookmakers_data = row['bookmakers']

        # Append basic info
        sport_list.append(current_sport)
        game_id_list.append(current_game_id)
        book_list.append(bookmaker_key)
        home_team_list.append(current_home_team)
        away_team_list.append(current_away_team)

        # Default odds
        home_odds = None
        away_odds = None

        # Search the bookmaker list for the specified key
        for bookmaker in bookmakers_data:
            if bookmaker.get("key") == bookmaker_key:
                markets = bookmaker.get("markets", [])
                for market in markets:
                    if market.get("key") == "h2h":
                        for outcome in market.get("outcomes", []):
                            if outcome.get("name") == current_home_team:
                                home_odds = outcome.get("price")
                            elif outcome.get("name") == current_away_team:
                                away_odds = outcome.get("price")
                break  # Stop after finding the desired bookmaker

        home_team_odds_list.append(home_odds)
        away_team_odds_list.append(away_odds)

    # Construct a DataFrame with the extracted fields
    extracted_odds = {
        'sport': sport_list,
        'game_id': game_id_list,
        'book': book_list,
        'home_team': home_team_list,
        'away_team': away_team_list,
        'home_team_odds': home_team_odds_list,
        'away_team_odds': away_team_odds_list
    }

    extracted_odds_df = pd.DataFrame(extracted_odds)
    return extracted_odds_df

def all_moneyline_odds(main_df,list_of_bookmakers):
    all_odds = []
    for bookmaker in list_of_bookmakers:
        odds = extract_moneyline_odds(main_df, bookmaker)
        all_odds.append(odds)
    return pd.concat(all_odds)

def ml_csv_all_time(dataframe):
    # Add date and time column
    current_datetime = datetime.datetime.now()
    dataframe['date_time'] = current_datetime

    # Append data to CSV file
    dataframe.to_csv('/Users/clayarmour/Desktop/SportsModel/all_time_moneyline.csv', mode='a', header=False, index=False)

def ml_csv_daily(dataframe):
    dataframe.to_csv('/Users/clayarmour/Desktop/SportsModel/daily_moneyline.csv', mode='w', header=True, index=False)


    


