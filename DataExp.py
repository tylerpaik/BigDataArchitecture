import requests
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timezone

def calcStats(gamerTag):
    uidURL = "https://zsr.octane.gg/players?tag=" + gamerTag
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
    print(event_df)
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

    averages = []
    averages.append(np.average(np.array(saves))) #taking averages of last 10 stats
    averages.append(np.average(np.array(goals)))
    averages.append(np.average(np.array(assists)))
    avg_df = pd.DataFrame({'Averages': averages, 'Stat Type': ['Saves Avg.', 'Goals Avg.', 'Assists Avg.']})

    fig, axes = plt.subplots(4)
    sns.lineplot(ax = axes[0], data=saves_df, x='Date', y ='Saves')  #line plot for saves 
    axes[0].set_title("Saves in the last 10 games")

    sns.lineplot(ax = axes[1], data=goals_df, x ='Date', y = 'Goals') #line plot for goals
    axes[1].set_title("Goals in the last 10 games")

    sns.lineplot(ax = axes[2], data=assists_df, x = 'Date', y = 'Assists') #line plot for assists
    axes[2].set_title("Assists in the last 10 games")

    sns.barplot(ax = axes[3], data=avg_df, x='Stat Type', y='Averages') #bar plot for averages
    axes[3].set_title("Average Stats for the last 10 games")

    fig.subplots_adjust(hspace=0.5)
    plt.show()


#------------CONTROLS--------------#
calcStats("Noly")

#testing seaborn html connection
html = mpld3.fig_to_html(ax.figure)