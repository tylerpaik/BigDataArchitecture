# import for development, hosting locally
from flask import Flask, jsonify
import pandas as pd
import schedule
import time
# from scipy import poisson

from config import redis_client

def clear_database(redis_client):
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

# def calc_probability(n_gas: int, df: pd.DataFrame) -> float:
#     if n_gas < 0:
#         raise ValueError("The number of goals/assists/scores can't be negative.")
#     # stats are always in the first column, extract as a list
#     data = df.iloc[:, 0].tolist()
#     # calculate the mean nr of goals (lambda)
#     mean_gas = sum(data) / len(data)
#     # def Poisson(lambda = mean_gas)
#     poisson_dist = poisson(mean_gas)
#     # store discrete pmf
#     n_gas_prob = poisson_dist.pmf(n_gas)
#     print("The probability of scoring ", n_gas, " units is ", n_gas_prob)
#     return n_gas_prob
# probability fc end

