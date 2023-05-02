import requests
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import pprint
import matplotlib.gridspec as gridspec


def getID(gamerTag):
    team1URL = "https://zsr.octane.gg/teams?name=" + gamerTag #api call
    response = requests.get(team1URL)
    if response.status_code == 200:
        data = response.json()
        pprint.pprint(data)
    team_id = data['teams'][0]['_id']
    print(team_id)

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
    # user_stats.sort_values("events",inplace=True)
    event_stat = user_stats.iloc[0]['events']
    event_df = pd.DataFrame(event_stat)
    saves = []
    assists = []
    goals = []
    e_id = event_df.iloc[0]['_id'] #changing every time???
    #print(event_df)
    dates = []
    game_count = []
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
        games = currEventStats_df.iloc[0]["games"] #adding matches for averages
        game_counts_df = pd.DataFrame(games.items())
        gas_df["startDate"] = currEventStats_df.iloc[0]["startDate"] #adding dates for visualization
        gas_df["games"] = game_counts_df.iloc[0][1]
        # print(gas_df)
        if gas_df.iloc[2][1] != None and gas_df.iloc[1][1] != None and gas_df.iloc[0][1] != None and gas_df.iloc[0]["startDate"] != None: #making sure we aren't adding nan values
            saves.append(gas_df.iloc[2][1]) #adding stats to lists with dates
            goals.append(gas_df.iloc[1][1])
            assists.append(gas_df.iloc[0][1])
            dates.append(gas_df.iloc[0]["startDate"])
            game_count.append(gas_df.iloc[0]['games'])
        else: 
            data_length +=1 
    for j in range(len(dates)):
        dates[j] = dates[j][:7] #get only date from timestamp string (makes it more readable)
    temp1 = sorted(zip(game_count, dates, saves, goals, assists)) #sorting parallel lists
    temp2 = list(zip(*temp1)) #unzipping sorted data
    game_count = np.array(list(temp2[0]))
    dates = np.array(list(temp2[1]))
    saves = np.array(list(temp2[2]))
    goals = np.array(list(temp2[3]))
    assists = np.array(list(temp2[4]))
    saves = np.divide(saves, game_count)
    goals = np.divide(goals, game_count)
    assists = np.divide(assists, game_count)
    # print(saves)

    saves_df = pd.DataFrame({'Saves': saves, 'Date': dates})#sorted data put into dataframe
    goals_df = pd.DataFrame({'Goals': goals, 'Date': dates})
    assists_df = pd.DataFrame({'Assists': assists, 'Date': dates})



    averages = []
    averages.append(np.average(np.array(saves))) #taking averages of last 10 stats
    averages.append(np.average(np.array(goals)))
    averages.append(np.average(np.array(assists)))
    avg_df = pd.DataFrame({'Averages': averages, 'Stat Type': ['Saves Avg.', 'Goals Avg.', 'Assists Avg.']})

    fig, axes = plt.subplots(2,2)
    fig.set_figheight(7)
    fig.set_figwidth(7)

    sns.lineplot(ax = axes[0][0], data=saves_df, x='Date', y ='Saves', errorbar=None)  #line plot for saves
    axes[0][0].set_title("Saves/game in the last 10 events")
    axes[0][0].tick_params(axis='x', rotation = 30)
    # plt.setp(plt.xticks()[0][0], rotation=30, horizontalalignment='right')

    sns.lineplot(ax = axes[0][1], data=goals_df, x ='Date', y = 'Goals', errorbar=None) #line plot for goals
    axes[0][1].set_title("Goals/game in the last 10 events")
    axes[0][1].tick_params(axis='x', rotation = 30)


    sns.lineplot(ax = axes[1][0], data=assists_df, x = 'Date', y = 'Assists', errorbar=None) #line plot for assists
    axes[1][0].set_title("Assists/game in the last 10 events")
    axes[1][0].tick_params(axis='x', rotation = 30)


    sns.barplot(ax = axes[1][1], data=avg_df, x='Stat Type', y='Averages', errorbar=None) #bar plot for averages
    axes[1][1].set_title("Average Stats/game in last 10 events")
    axes[1][1].tick_params(axis='x', rotation = 30)
    
    # fig.subplots_adjust(right= 0.8, left=1,  hspace = .5)
    fig.tight_layout(pad=0.5)
    plt.show()


def teams_calcStats(team1):
    team1URL = "https://zsr.octane.gg/teams?name=" + team1
    response_team1 = requests.get(team1URL)
    response_team1 = response_team1.json()
    team1_df = pd.DataFrame(response_team1['teams'])
    for index, col in team1_df.iterrows():
        if len(col) > 4:
            if col[5] == True:
                team1_id = col[0]
        else: 
            team1_id = col[0]
    team1EventsURL = "https://zsr.octane.gg/stats/teams?stat=goals&stat=assists&stat=saves&stat=score&team=" + team1_id
    t1eventResponse = requests.get(team1EventsURL)
    t1eventResponse = t1eventResponse.json()
    t1Event_df = pd.DataFrame(t1eventResponse['stats'])
    t1Event_df.sort_values(by="startDate", axis=0, inplace=True) #sorting dataframe based on start date
    t1Event_df = pd.DataFrame(t1Event_df.iloc[0]['events'])
    print(team1_id)
    saves = []
    goals = []
    assists = []
    dates = []
    wins_ratio = []
    game_count = []
    data_length = 11
    if (len(t1Event_df)) < 11:
        print("Not enough data on this team to be significant.")
    else: 
        for i in range(data_length):
            print(len(t1Event_df))
            e_id = t1Event_df.iloc[i]['_id'] #taking last event id
            t1eventStats_url = "https://zsr.octane.gg/stats/teams/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&team=" + str(team1_id)
            t1eventStats = requests.get(t1eventStats_url)
            t1eventStats = t1eventStats.json()
            t1currEventStats_df = pd.DataFrame(t1eventStats['stats']) #all event data into dataframe
            t1currEventStats_df.sort_values(by="startDate", axis=0, inplace=True) #sorting dataframe based on start date
            gas = t1currEventStats_df.iloc[0]['stats']
            gas_df = pd.DataFrame(gas.items()) #putting event stats into dataframe
            games = t1currEventStats_df.iloc[0]["games"] #adding matches for averages
            game_counts_df = pd.DataFrame(games.items())
            gas_df["startDate"] = t1currEventStats_df.iloc[0]["startDate"] #adding dates for visualization
            gas_df["games"] = game_counts_df[1][0]
            # print(gas_df.iloc[1][1])
            # print(gas_df)
            # print(game_counts_df)
            if gas_df.iloc[2][1] != None and gas_df.iloc[1][1] != None and gas_df.iloc[0][1] != None and gas_df.iloc[0]["startDate"] != None: #making sure we aren't adding nan values
                saves.append(gas_df.iloc[2][1]) #adding stats to lists with dates
                goals.append(gas_df.iloc[1][1])
                assists.append(gas_df.iloc[0][1])
                dates.append(gas_df.iloc[0]["startDate"])
                wins_ratio.append(game_counts_df.iloc[2][1]/game_counts_df.iloc[0][1])
                game_count.append(gas_df.iloc[0]['games'])
            else: 
                data_length +=1

        for j in range(len(dates)):
            dates[j] = dates[j][:7] #get only date from timestamp string (makes it more readable)
        temp1 = sorted(zip(dates, game_count, saves, goals, assists, wins_ratio)) #sorting parallel lists
        temp2 = list(zip(*temp1)) #unzipping sorted data
        dates = list(temp2[0])
        game_count = np.array(list(temp2[1]))
        saves = np.array(list(temp2[2]))
        goals = list(temp2[3])
        assists = list(temp2[4])
        wins_ratio = list(temp2[5])

        # print(saves)
        # print("game count", game_count)
        saves = saves/game_count
        goals = goals/game_count
        assists = assists/game_count

        saves_df = pd.DataFrame({'Saves': saves, 'Date': dates})#sorted data put into dataframe
        goals_df = pd.DataFrame({'Goals': goals, 'Date': dates})
        assists_df = pd.DataFrame({'Assists': assists, 'Date': dates})
        wins_ratio_df = pd.DataFrame({'Wins/Total Games': wins_ratio, 'Date': dates})

        averages = []
        averages.append(np.average(np.array(saves))) #taking averages of last 10 stats
        averages.append(np.average(np.array(goals)))
        averages.append(np.average(np.array(assists)))
        avg_df = pd.DataFrame({'Averages': averages, 'Stat Type': ['Saves Avg.', 'Goals Avg.', 'Assists Avg.']})

        plt.style.use('dark_background')
        fig, axes = plt.subplots(2,3)
        sns.lineplot(ax = axes[0][0], data=saves_df, x='Date', y ='Saves')  #line plot for saves 
        axes[0][0].set_title("Saves/game in the last 10 events")
        axes[0][0].tick_params(axis='x', rotation = 30)

        sns.lineplot(ax = axes[0][1], data=goals_df, x ='Date', y = 'Goals') #line plot for goals
        axes[0][1].set_title("Goals/game in the last 10 events")
        axes[0][1].tick_params(axis='x', rotation = 30)

        sns.lineplot(ax = axes[0][2], data=assists_df, x = 'Date', y = 'Assists') #line plot for assists
        axes[0][2].set_title("Assists/game in the last 10 events")
        axes[0][2].tick_params(axis='x', rotation = 30)

        sns.barplot(ax = axes[1][0], data=avg_df, x='Stat Type', y='Averages') #bar plot for averages
        axes[1][0].set_title("Average Stats for the last 10 events")
        axes[1][0].tick_params(axis='x', rotation = 30)

        sns.lineplot(ax = axes[1][1], data=wins_ratio_df, x = 'Date', y='Wins/Total Games') #lineplot for win/total games for each event
        axes[1][1].set_title("Wins/Total games for the last 10 events")
        axes[1][1].tick_params(axis='x', rotation = 30)

        fig.delaxes(axes[1][2]) #taking out unused plot
        fig.subplots_adjust(right= 0.8, hspace=0.5)
        plt.show()


#------------CONTROLS--------------#
calcStats("Noly")
# teams_calcStats("Lights Out!") #G2 Esports, Lights Out!
# getID("FaZe Clan")

#testing seaborn html connection
# html = mpld3.fig_to_html(ax.figure)