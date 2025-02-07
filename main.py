from call import get_odds, get_sports
from dataframe import load_file, create_dataframe, extract_moneyline_odds, all_moneyline_odds, ml_csv_all_time, ml_csv_daily
from manipulate import calculate_novig, create_pivot, calculate_averages, merge_data, calculate_edges, save_to_csv, best_bets
from dashboard import dashboard
import pandas as pd


us_bookmakers = ['betmgm','fliff', 'bovada', 'draftkings', 'fanduel', 'hardrockbet', 'betonlineag', 'espnbet', 'betus','betrivers','ballybet']
sports = ['basketball_nba','basketball_ncaab']




def moneyline():
    daily_df = pd.DataFrame()
    for sport in sports:
        
        get_odds(sport)
        data = load_file('odds_list.json')
        main = create_dataframe(data)
        empty_df = all_moneyline_odds(main, us_bookmakers)
        ml_csv_all_time(empty_df)
        daily_df = pd.concat([daily_df, empty_df])
        ml_csv_daily(daily_df)
        empty_df = []
    
    read = pd.read_csv('daily_moneyline.csv')
    novig = calculate_novig(read)
    pivot = create_pivot(novig)
    averages = calculate_averages(pivot)
    merge = merge_data(novig, averages)
    edge = calculate_edges(merge)
    save_to_csv(edge, 'novig.csv')
    bets = best_bets(edge, 50)
    
    dashboard()
    

    print('All done!')

moneyline()
