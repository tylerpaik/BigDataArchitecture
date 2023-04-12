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
    # response = requests.get("https://zsr.octane.gg/players?tag=noly")
    response = response.json()
    user = pd.DataFrame(response['players'])
    u_id = user.iloc[0]['_id']
    print(u_id)
    playerStats_url = "https://zsr.octane.gg/stats/players?stat=goals&stat=assists&stat=saves&player=" + str(u_id)
    stats = requests.get(playerStats_url)
    stats = stats.json()
    stats_keys = stats.keys()
    user_stats = pd.DataFrame(stats['stats'])
    user_stats.sort_values("events",inplace=True)
    event_stat = user_stats.iloc[0]['events']
    # print(event_stat)
    event_df = pd.DataFrame(event_stat)
    # print(event_df)
    # print(user_stats)
    # event_id10 = []
    saves = []
    assists = []
    goals = []
    e_id = event_df.iloc[0]['_id'] #changing every time???
    print(e_id)
    # eventStats_url = "https://zsr.octane.gg/stats/players/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&player="+str(u_id) + "&after" + "2021-01-01"
    # eventStats = requests.get(eventStats_url)
    # eventStats = eventStats.json()
    # currEventStats_df = pd.DataFrame(eventStats['stats'])
    # gas = currEventStats_df.iloc[0]['stats']
    # gas_df = pd.DataFrame(gas.items())
    # gas_df.rename(columns={0:'Stat Type', 1: 'Stats'}, inplace = True)
    # gas_df.sort_values('startDate')
    # sns.set()
    # ax = sns.barplot(data=gas_df, x='Stat Type', y ='Stats')
    # plt.show()
    # currEvent_saves = currEventStats_df.iloc['stats']
    # saves.append(currEvent_saves)
    # print(saves)
    # gas_df = pd.DataFrame()
    dates = []
    data_length = 11
    for i in range(data_length):
        e_id = event_df.iloc[i]['_id']
        eventStats_url = "https://zsr.octane.gg/stats/players/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&player=" + str(u_id)
        eventStats = requests.get(eventStats_url)
        eventStats = eventStats.json()
        currEventStats_df = pd.DataFrame(eventStats['stats'])
        currEventStats_df.sort_values(by="startDate", axis=0, inplace=True)
        gas = currEventStats_df.iloc[0]['stats']
        gas_df = pd.DataFrame(gas.items())
        gas_df["startDate"] = currEventStats_df.iloc[0]["startDate"] #adding dates for visualization 
        # gas_df.rename(columns={0:'Stat Type', 1: 'Stats'}, inplace = True)
        # print(gas_df)
        if gas_df.iloc[2][1] != None and gas_df.iloc[1][1] != None and gas_df.iloc[0][1] != None and gas_df.iloc[0]["startDate"] != None:
            saves.append(gas_df.iloc[2][1])
            goals.append(gas_df.iloc[1][1])
            assists.append(gas_df.iloc[0][1])
            dates.append(gas_df.iloc[0]["startDate"])
        else: 
            data_length +=1
    for j in range(len(dates)):
        dates[j] = dates[j][:7] #get only date from timestamp string (makes it more readable)
    temp1 = sorted(zip(dates, saves, goals, assists)) #sorting parallel lists
    temp2 = list(zip(*temp1))
    dates = list(temp2[0])
    saves = list(temp2[1])
    goals = list(temp2[2])
    assists = list(temp2[3])
    saves_df = pd.DataFrame({'Saves': saves, 'Date': dates})
    goals_df = pd.DataFrame({'Goals': goals, 'Date': dates})
    assists_df = pd.DataFrame({'Assists': assists, 'Date': dates})

    averages = []
    averages.append(np.average(np.array(saves)))
    averages.append(np.average(np.array(goals)))
    averages.append(np.average(np.array(assists)))
    avg_df = pd.DataFrame({'Averages': averages, 'Stat Type': ['Saves Avg.', 'Goals Avg.', 'Assists Avg.']})

    fig, axes = plt.subplots(4)
    sns.lineplot(ax = axes[0], data=saves_df, x='Date', y ='Saves')
    axes[0].set_title("Saves in the last 10 games")

    sns.lineplot(ax = axes[1], data=goals_df, x ='Date', y = 'Goals')
    axes[1].set_title("Goals in the last 10 games")

    sns.lineplot(ax = axes[2], data=assists_df, x = 'Date', y = 'Assists')
    axes[2].set_title("Assists in the last 10 games")

    sns.barplot(ax = axes[3], data=avg_df, x='Stat Type', y='Averages')
    axes[3].set_title("Average Stats for the last 10 games")

    fig.subplots_adjust(hspace=0.5)
    plt.show()

calcStats("noly")

#testing seaborn html connection
html = mpld3.fig_to_html(ax.figure)