import pandas as pd 
from IPython.display import display
import numpy as np



main = pd.read_csv('daily_moneyline.csv')



def implied_odds(odds):
    if odds > 0:
        return 100 / (odds + 100) * 100   
    else: 
        return -odds / (-odds + 100) * 100

def calculate_novig(main):
    main['home_break_even'] = main['home_team_odds'].apply(implied_odds).round(2)
    main['away_break_even'] = main['away_team_odds'].apply(implied_odds).round(2)
    main['home_novig'] = (main['home_break_even'] / (main['home_break_even'] + main['away_break_even']) * 100).round(2)
    main['away_novig'] = (main['away_break_even'] / (main['home_break_even'] + main['away_break_even']) * 100).round(2)
    return main

def create_pivot(main):
    novig_df = calculate_novig(main)
    novig_df.columns = novig_df.columns.str.strip()
    pivot_df = novig_df.pivot(index='game_id', columns='book', values=['home_novig', 'away_novig'])
    pivot_df.columns = [f'{i}_{j}' for i, j in pivot_df.columns]
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns=lambda x: x.replace('home_novig_', 'home_novig_').replace('away_novig_', 'away_novig_'), inplace=True)
    return pivot_df

def calculate_averages(pivot_df):
    pivot_df['home_novig_avg'] = pivot_df.filter(like='home_novig').mean(axis=1).round(2)
    pivot_df['away_novig_avg'] = pivot_df.filter(like='away_novig').mean(axis=1).round(2)
    return pivot_df

def merge_data(main, pivot_df):
    referall_odds = pivot_df[['game_id', 'home_novig_avg', 'away_novig_avg']]
    main = main.merge(referall_odds, on='game_id', how='left')
    return main

def calculate_edges(main):
    main['home_edge'] = (main['home_novig_avg'] - main['home_break_even']).round(2)
    main['away_edge'] = (main['away_novig_avg'] - main['away_break_even']).round(2)
    return main

def save_to_csv(main, filename):
    main.to_csv(filename, index=False, header=True, mode='w')

def best_bets(main, num_rows):
    best_bets = pd.DataFrame()
    best_bets['expected_value'] = []
    best_bets['book'] = main['book']
    best_bets['edge'] = np.where(main['home_edge'] > main['away_edge'], main['home_edge'], main['away_edge'])
    best_bets['team'] = np.where(best_bets['edge'] == main['home_edge'], main['home_team'], main['away_team'])
    best_bets['odds'] = np.where(best_bets['edge'] == main['home_edge'], main['home_team_odds'], main['away_team_odds'])
    best_bets['probability'] = np.where(best_bets['edge'] == main['home_edge'], main['home_novig_avg'], main['away_novig_avg'])
    best_bets['expected_value'] = np.where(best_bets['odds'] > 0, 
                                           ((best_bets['probability']/100) * (best_bets['odds']/100) - 1), 
                                           ((best_bets['probability']/100) * (100/abs(best_bets['odds'])) - 1))
    column_order = ['expected_value', 'book', 'team', 'odds', 'probability']
    best_bets = best_bets[column_order]  

    best_bets = best_bets.sort_values(by='expected_value', ascending=False)
    best_bets = best_bets.head(num_rows)

    best_bets.to_csv('best_bets.csv', index=False, header=True, mode='w')


