import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()



REGIONS = 'us,us2' 
MARKETS = 'h2h' 
ODDS_FORMAT = 'american' 
DATE_FORMAT = 'iso' 
API_KEY = os.getenv('API_KEY')

if API_KEY is None:
    raise ValueError("API_KEY environment variable not set")

def get_sports():
    

    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports', 
        params={
            'api_key': API_KEY
        }
    )
    
    try:
        sports_list = sports_response.json()
        with open('sports_list.json', 'w') as file:
            json.dump(sports_list, file)
        print('List of in season sports has been saved to sports_list.json')
    except ValueError:
        print('Failed to parse sports_JSON response')
    
    return sports_response.json()

def get_odds(sport):
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )
    
    try:
        odds_list = odds_response.json()
        with open('odds_list.json', 'w') as file:
            json.dump(odds_list, file)
        print('List of odds has been saved to odds_list.json')
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])
    except ValueError:
        print('Failed to parse odds_JSON response')

    return odds_response.json()