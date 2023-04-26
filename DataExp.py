import requests
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import pprint

def calcStats(gamerTag):
    uidURL = "https://zsr.octane.gg/players?tag=" + gamerTag
    response = requests.get(uidURL)
    response = response.json()
    pprint.pprint(response)
    user = pd.DataFrame(response['players'])
    u_id = user.iloc[0]['_id']
    print(u_id)
    playerStats_url = "https://zsr.octane.gg/stats/players?stat=goals&stat=assists&stat=saves&player=" + str(u_id)
    stats = requests.get(playerStats_url)
    stats = stats.json()
    #pprint.pprint(stats['stats'])
    user_stats = pd.DataFrame(stats['stats'])
    user_stats.sort_values("events",inplace=True)
    event_stat = user_stats.iloc[0]['events']
    event_df = pd.DataFrame(event_stat)
    saves = []
    assists = []
    goals = []
<<<<<<< Updated upstream
    e_id = event_df.iloc[0]['_id'] #changing every time?
    print(event_df)
=======
    e_id = event_df.iloc[0]['_id'] #changing every time???
    #print(event_df)
>>>>>>> Stashed changes
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
    #plt.show()


def teams_calcStats(team1):
    team1URL = "https://zsr.octane.gg/teams?name=" + team1
    response_team1 = requests.get(team1URL)
    response_team1 = response_team1.json()
    team1_df = pd.DataFrame(response_team1['teams'])
    for index, col in team1_df.iterrows():
        if col[5] == True:
            team1_id = col[0]
    team1EventsURL = "https://zsr.octane.gg/stats/teams?stat=goals&stat=assists&stat=saves&stat=score&team=" + team1_id
    t1eventResponse = requests.get(team1EventsURL)
    t1eventResponse = t1eventResponse.json()
    t1Event_df = pd.DataFrame(t1eventResponse['stats'])
    t1Event_df.sort_values(by="startDate", axis=0, inplace=True) #sorting dataframe based on start date
    t1Event_df = pd.DataFrame(t1Event_df.iloc[0]['events'])
    # print(t1eventStatResponse['stats'])
    # print(t1Event_df)
    print(team1_id)
    saves = []
    goals = []
    assists = []
    score = []
    dates = []
    wins_ratio = []
    data_length = 11
    for i in range(data_length):
        e_id = t1Event_df.iloc[i]['_id'] #taking last event id
        t1eventStats_url = "https://zsr.octane.gg/stats/teams/events?stat=goals&stat=assists&stat=saves&stat=score&event=" + str(e_id) + "&team=" + str(team1_id)
        t1eventStats = requests.get(t1eventStats_url)
        t1eventStats = t1eventStats.json()
        t1currEventStats_df = pd.DataFrame(t1eventStats['stats']) #all event data into dataframe
        # print(t1currEventStats_df)
        t1currEventStats_df.sort_values(by="startDate", axis=0, inplace=True) #sorting dataframe based on start date
        gas = t1currEventStats_df.iloc[0]['stats']
        match_data = t1currEventStats_df.iloc[0]['matches']
        gas_df = pd.DataFrame(gas.items()) #putting event stats into dataframe
        match_df = pd.DataFrame(match_data.items()) #putting match stats into dataframe
        gas_df["startDate"] = t1currEventStats_df.iloc[0]["startDate"] #adding dates for visualization
        # print(gas_df.iloc[1][1])
        # print(gas_df)
        # print(match_data)
        if gas_df.iloc[3][1] != None and gas_df.iloc[2][1] != None and gas_df.iloc[1][1] != None and gas_df.iloc[0][1] != None and gas_df.iloc[0]["startDate"] != None: #making sure we aren't adding nan values
            saves.append(gas_df.iloc[2][1]) #adding stats to lists with dates
            goals.append(gas_df.iloc[1][1])
            assists.append(gas_df.iloc[0][1])
            score.append(gas_df.iloc[3][1])
            dates.append(gas_df.iloc[0]["startDate"])
            wins_ratio.append(match_df.iloc[2][1]/match_df.iloc[0][1])
        else: 
            data_length +=1

    for j in range(len(dates)):
        dates[j] = dates[j][:7] #get only date from timestamp string (makes it more readable)
    temp1 = sorted(zip(dates, saves, goals, assists, score, wins_ratio)) #sorting parallel lists
    temp2 = list(zip(*temp1)) #unzipping sorted data
    dates = list(temp2[0])
    saves = list(temp2[1])
    goals = list(temp2[2])
    assists = list(temp2[3])
    score = list(temp2[4])
    wins_ratio = list(temp2[5])
    saves_df = pd.DataFrame({'Saves': saves, 'Date': dates})#sorted data put into dataframe
    goals_df = pd.DataFrame({'Goals': goals, 'Date': dates})
    assists_df = pd.DataFrame({'Assists': assists, 'Date': dates})
    score_df = pd.DataFrame({'Score': score, 'Date': dates})
    wins_ratio_df = pd.DataFrame({'Wins/Total Games': wins_ratio, 'Date': dates})

    averages = []
    averages.append(np.average(np.array(saves))) #taking averages of last 10 stats
    averages.append(np.average(np.array(goals)))
    averages.append(np.average(np.array(assists)))
    avg_df = pd.DataFrame({'Averages': averages, 'Stat Type': ['Saves Avg.', 'Goals Avg.', 'Assists Avg.']})

    fig, axes = plt.subplots(2,3)
    sns.lineplot(ax = axes[0][0], data=saves_df, x='Date', y ='Saves')  #line plot for saves 
    axes[0][0].set_title("Saves in the last 10 events")

    sns.lineplot(ax = axes[0][1], data=goals_df, x ='Date', y = 'Goals') #line plot for goals
    axes[0][1].set_title("Goals in the last 10 events")

    sns.lineplot(ax = axes[0][2], data=assists_df, x = 'Date', y = 'Assists') #line plot for assists
    axes[0][2].set_title("Assists in the last 10 events")

    sns.lineplot(ax = axes[1][0], data=score_df, x = 'Date', y = 'Score') #line plot for score
    axes[1][0].set_title("Score in the last 10 events")

    sns.barplot(ax = axes[1][1], data=avg_df, x='Stat Type', y='Averages') #bar plot for averages
    axes[1][1].set_title("Average Stats for the last 10 events")

    sns.lineplot(ax = axes[1][2], data=wins_ratio_df, x = 'Date', y='Wins/Total Games') #lineplot for win/total games for each event
    axes[1][2].set_title("Wins/Total games for the last 10 events")

    fig.subplots_adjust(hspace=0.5)
    plt.show()


#------------CONTROLS--------------#
calcStats("Noly")
#teams_calcStats("FaZe Clan", "G1")

#testing seaborn html connection
# html = mpld3.fig_to_html(ax.figure)