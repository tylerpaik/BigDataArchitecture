# import for development, hosting locally
from flask import Flask, jsonify
import pandas as pd
import schedule
import time
from data import retrieve_player_dfs
import numpy as np
from scipy.stats import poisson

from config import redis_client

def clear_database():
    redis_client.flushdb()
    print("Database cleared")

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

# def get_team_names():
#     url = "https://zsr.octane.gg/teams"
#     response = requests.get(url)
#     response_data = response.json()
#     teams_df = pd.DataFrame(response_data['teams'])
#     unique_team_names = teams_df['name'].unique()
#     return unique_team_names

# def teams():
#     unique_team_names = pd.Series(get_team_names())
#     return jsonify(team_names=unique_team_names.tolist())

#Pred is for number of goals user wants probability for
def calc_probability(n, stat):
    num_stat = np.sum(stat)

    # if n_gas < 0:
    #     raise ValueError("The number of goals/assists/scores can't be negative.")
    # # stats are always in the first column, extract as a list
    # data = df.iloc[:, 0].tolist()

    # calculate the mean nr of goals (lambda)
    mean_stat = num_stat / stat.shape[0]
    # def Poisson(lambda = mean_gas)
    # store discrete pmf
    num_goals_prob = poisson.cdf(n, mean_stat)
    print(num_goals_prob)
    return 1-num_goals_prob
# probability fc end

