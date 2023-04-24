from flask import Flask, render_template, request, jsonify, send_file
import requests
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

# take the following code from calc_stats() in app.py
# likely break calc_stats() before integration, use 2 extra functions for player stats plotting and probability - avoid more api calls
uidURL = "https://zsr.octane.gg/players?tag=noly"
response = requests.get(uidURL)
response = response.json()
user = pd.DataFrame(response['players'])
u_id = user.iloc[0]['_id']
print(u_id)
playerStats_url = "https://zsr.octane.gg/stats/players?stat=goals&stat=assists&stat=saves&player=" + str(u_id)
stats = requests.get(playerStats_url)
stats = stats.json()
user_stats = pd.DataFrame(stats['stats'])
user_stats.sort_values("events",inplace=True)
event_stat = user_stats.iloc[0]['events']
event_df = pd.DataFrame(event_stat)
saves = []
assists = []
goals = []
e_id = event_df.iloc[0]['_id'] #changing every time???
print(e_id)
dates = []
data_length = 11
for i in range(data_length):
    e_id = event_df.iloc[i]['_id'] #taking last event id
    eventStats_url = "https://zsr.octane.gg/stats/players/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&player=" + str(u_id)
    eventStats = requests.get(eventStats_url)
    eventStats = eventStats.json()
    currEventStats_df = pd.DataFrame(eventStats['stats']) #all event data into dataframe
    currEventStats_df.sort_values(by="startDate", axis=0, inplace=True) #sorting dataframe based on start date
    gas = currEventStats_df.iloc[0]['stats']
    gas_df = pd.DataFrame(gas.items()) #putting event stats into dataframe
    gas_df["startDate"] = currEventStats_df.iloc[0]["startDate"] #adding dates for visualization
    if gas_df.iloc[2][1] != None and gas_df.iloc[1][1] != None and gas_df.iloc[0][1] != None and gas_df.iloc[0]["startDate"] != None: #making sure we aren't adding nan values
        saves.append(gas_df.iloc[2][1]) #adding stats to lists with dates
        goals.append(gas_df.iloc[1][1])
        assists.append(gas_df.iloc[0][1])
        dates.append(gas_df.iloc[0]["startDate"])
    else:
        data_length +=1
for j in range(len(dates)):

    dates[j] = dates[j][:7] #get only date from timestamp string (makes it more readable)
    temp1 = sorted(zip(dates, saves, goals, assists)) #sorting parallel lists
    temp2 = list(zip(*temp1)) #unzipping sorted data
    dates = list(temp2[0])
    saves = list(temp2[1])
    goals = list(temp2[2])
    assists = list(temp2[3])
    saves_df = pd.DataFrame({'Saves': saves, 'Date': dates})#sorted data put into dataframe
    goals_df = pd.DataFrame({'Goals': goals, 'Date': dates})
    assists_df = pd.DataFrame({'Assists': assists, 'Date': dates})


# after getting the 3 data frames, compute probability
# integrate:

# Poisson is the best fit for this task, lacking data for binomial
from scipy.stats import poisson
# take Nr of goals/assists/saves (gas) and the desired df as an input
def calc_probability(n_gas: int, df: pd.DataFrame) -> float:
    if n_gas < 0:
        raise ValueError("The number of goals/assists/scores can't be negative.")
    # stats are always in the first column, extract as a list
    data = df.iloc[:, 0].tolist()
    # calculate the mean nr of goals (lambda)
    mean_gas = sum(data) / len(data)
    # def Poisson(lambda = mean_gas)
    poisson_dist = poisson(mean_gas)
    # store discrete pmf
    n_gas_prob = poisson_dist.pmf(n_gas)
    return n_gas_prob

# assign a dict to access desired df
dataframes = {
    'goals': goals_df,
    'assists': assists_df,
    'saves': saves_df
}

# keep getting input from user till input = quit
while True:
    gas_type = input("\nEnter the stats type you want to see (goals, assists, or saves) or type 'quit' to exit: ").lower()

    if gas_type == 'quit':
        print("Exiting the application.")
        break

    while gas_type not in dataframes:
        print("Invalid input. Choose from (goals, assists, saves)..")
        gas_type = input("Enter the input type again (goals, assists, or saves): ").lower()

    n_probability = int(input("Enter the number of goals/assists/saves: "))
    # calc prob, print
    probability = calc_probability(n_probability, dataframes[gas_type])
    type_map = {'goals': 'Goals', 'assists': 'Assists', 'saves': 'Saves'}
    print(f"The probability of {n_probability} {type_map[gas_type].lower()} is {probability:.6f}")


if __name__ == '__main__':
    input_and_compute_probability()
