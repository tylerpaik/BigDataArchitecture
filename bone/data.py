from flask import jsonify
import requests
import pandas as pd
import numpy as np
import msgpack
import pprint
from config import redis_client


def fetch_player(gamer_tag):
    uidURL = "https://zsr.octane.gg/players?tag=" + gamer_tag
    response = requests.get(uidURL)
    if response.status_code == 200:
        data = response.json()
        pprint.pprint(response)

        player_id = data['players'][0]['_id']

        if redis_client.hexists('player_data', player_id):
            print(f"Player ID {player_id} exists in the database!")
            return player_id
        else:
            saves, goals, assists, averages = extract_player_data(data, player_id)
            # store the dataframes in Redis under the player ID key
            player_data = {
                'saves': saves,
                'goals': goals,
                'assists': assists,
                'averages': averages
            }
            
            player_data_serialized = msgpack.packb(player_data)
            redis_client.hset('player_data', player_id, player_data_serialized)
            return player_id
            #jsonify({"message": "Success."}), 200
    else:
        print("Throw error here, no response from API")
        return LookupError
    
def extract_player_data(data, player_id):
    playerStats_url = "https://zsr.octane.gg/stats/players?stat=goals&stat=assists&stat=saves&player=" + str(player_id)
    stats = requests.get(playerStats_url)
    stats = stats.json()
    user_stats = pd.DataFrame(stats['stats'])
    user_stats.sort_values("events",inplace=True)
    event_stat = user_stats.iloc[0]['events']
    event_df = pd.DataFrame(event_stat)
    saves = []
    assists = []
    goals = []
    e_id = event_df.iloc[0]['_id']
    print("event id", e_id)
    dates = []
    game_count = []
    data_length = 11
    for i in range(data_length):
        e_id = event_df.iloc[i]['_id'] #taking last event id
        eventStats_url = "https://zsr.octane.gg/stats/players/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&player=" + str(player_id)
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
    temp1 = sorted(zip(dates, game_count, saves, goals, assists)) #sorting parallel lists
    temp2 = list(zip(*temp1)) #unzipping sorted data
    dates = np.array(temp2[0])
    game_count = np.array(temp2[1])
    saves = np.array(temp2[2])
    goals = np.array(temp2[3])
    assists = np.array(temp2[4])
    for dateIndex in range(len(dates)):
        yr = dates[dateIndex][2:4]
        month = dates[dateIndex][-2:]
        dates[dateIndex] = month + "-" + yr
    saves = np.divide(saves, game_count) #[stat]/game calculations
    goals = np.divide(goals, game_count)
    assists = np.divide(assists, game_count)
    saves_df = pd.DataFrame({'Saves': saves, 'Date': dates})#sorted data put into dataframe
    goals_df = pd.DataFrame({'Goals': goals, 'Date': dates})
    assists_df = pd.DataFrame({'Assists': assists, 'Date': dates})

    averages = []
    averages.append(np.average(np.array(saves))) #taking averages of last 10 stats
    averages.append(np.average(np.array(goals)))
    averages.append(np.average(np.array(assists)))
    avg_df = pd.DataFrame({'Averages': averages, 'Stat Type': ['Saves', 'Goals', 'Assists']})
    
    saves_serialized = msgpack.packb(saves_df.to_dict())
    goals_serialized = msgpack.packb(goals_df.to_dict())
    assists_serialized = msgpack.packb(assists_df.to_dict())
    avg_serialized = msgpack.packb(avg_df.to_dict())
    

    return saves_serialized, goals_serialized, assists_serialized, avg_serialized

def retrieve_player_dfs(player_tag, vis):
    try:
        player_id = fetch_player(player_tag)
    except:
        player_id = player_tag
    packed_data = redis_client.hget('player_data', player_id)
    unpacked_data = msgpack.unpackb(packed_data)

    packed_goals = unpacked_data['goals']
    packed_saves = unpacked_data['saves']
    packed_assists = unpacked_data['assists']
    packed_averages = unpacked_data['averages']

    unpacked_goals = msgpack.unpackb(packed_goals, strict_map_key=False)
    unpacked_saves = msgpack.unpackb(packed_saves, strict_map_key=False)
    unpacked_assists = msgpack.unpackb(packed_assists, strict_map_key=False)
    unpacked_averages = msgpack.unpackb(packed_averages, strict_map_key=False)
    
    goals_df = pd.DataFrame.from_dict(unpacked_goals)
    saves_df = pd.DataFrame.from_dict(unpacked_saves)
    assists_df = pd.DataFrame.from_dict(unpacked_assists)
    averages_df = pd.DataFrame.from_dict(unpacked_averages)

    all_df = goals_df.join(saves_df['Saves'])
    all_df = all_df.join(assists_df['Assists'])
    all_df = all_df.join(averages_df['Averages'])
    all_df = all_df.rename(columns = {"Averages": "averages", "Assists": "assists", "Saves": "saves", "Goals": "goals", "Date": "date"})

    # Convert the unpacked data back into a DataFrame
    if vis == 0:
        return all_df
    return goals_df, saves_df, assists_df, averages_df

def fetch_team(team_name):
    teamURL = "https://zsr.octane.gg/teams?name=" + team_name
    response = requests.get(teamURL)
    if response.status_code == 200:
        data = response.json()
        pprint.pprint(response)

        team_id = data['teams'][0]['_id']

        if redis_client.hexists('team_data', team_id):
            print(f"Team ID {team_id} exists in the database!")
            return team_id
        else:
            saves, goals, assists, averages, win_loss = extract_team_data(data, team_id)
            # store the dataframes in Redis under the player ID key
            team_data = {
                'saves': saves,
                'goals': goals,
                'assists': assists,
                'averages': averages,
                'win_loss': win_loss
            }
            
            team_data_serialized = msgpack.packb(team_data)
            redis_client.hset('team_data', team_id, team_data_serialized)
            return team_id
            #jsonify({"message": "Success."}), 200
    else:
        print("Throw error here, no response from API")
        return LookupError

def extract_team_data(data, team_id):
    #api call    
    #team_df = pd.DataFrame(data['teams'])
    teamEventsURL = "https://zsr.octane.gg/stats/teams?stat=goals&stat=assists&stat=saves&stat=score&team=" + team_id
    teventResponse = requests.get(teamEventsURL)
    teventResponse = teventResponse.json()
    tEvent_df = pd.DataFrame(teventResponse['stats'])
    tEvent_df.sort_values(by="startDate", axis=0, inplace=True) #sorting dataframe based on start date
    tEvent_df = pd.DataFrame(tEvent_df.iloc[0]['events'])
    print(team_id)
    saves = []
    goals = []
    assists = []
    dates = []
    wins_ratio = []
    game_count = []
    data_length = 3
    for i in range(0, data_length - 1):
        e_id = tEvent_df.iloc[i]['_id'] #taking last event id
        t1eventStats_url = "https://zsr.octane.gg/stats/teams/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&team=" + str(team_id)
        t1eventStats = requests.get(t1eventStats_url)
        t1eventStats = t1eventStats.json()
        t1currEventStats_df = pd.DataFrame(t1eventStats['stats']) #all event data into dataframe
        t1currEventStats_df.sort_values(by="startDate", axis=0, inplace=True) #sorting dataframe based on start date
        gas = t1currEventStats_df.iloc[0]['stats']
        gas_df = pd.DataFrame(gas.items()) #putting event stats into dataframe
        games = t1currEventStats_df.iloc[0]["games"] #adding matches for averages
        game_counts_df = pd.DataFrame(games.items())
        gas_df["startDate"] = t1currEventStats_df.iloc[0]["startDate"] #adding dates for visualization
        gas_df["games"] = game_counts_df[1][0] #game count
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

    print(saves)
    print("game count", game_count)
    saves = saves/game_count
    goals = goals/game_count #[stat] per game calculation
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

    saves_serialized = msgpack.packb(saves_df.to_dict())
    goals_serialized = msgpack.packb(goals_df.to_dict())
    assists_serialized = msgpack.packb(assists_df.to_dict())
    avg_serialized = msgpack.packb(avg_df.to_dict())
    wins_ratio_serialized = msgpack.packb(wins_ratio_df.to_dict())

    return saves_serialized, goals_serialized, assists_serialized, avg_serialized, wins_ratio_serialized

def retrieve_team_dfs(team_tag):
    try:
        team_id = fetch_team(team_tag)
    except:
        team_id = team_tag
    packed_data = redis_client.hget('team_data', team_id)
    unpacked_data = msgpack.unpackb(packed_data)

    packed_goals = unpacked_data['goals']
    packed_saves = unpacked_data['saves']
    packed_assists = unpacked_data['assists']
    packed_averages = unpacked_data['averages']
    packed_win_loss = unpacked_data['win_loss']

    unpacked_goals = msgpack.unpackb(packed_goals, strict_map_key=False)
    unpacked_saves = msgpack.unpackb(packed_saves, strict_map_key=False)
    unpacked_assists = msgpack.unpackb(packed_assists, strict_map_key=False)
    unpacked_averages = msgpack.unpackb(packed_averages, strict_map_key=False)
    unpacked_win_loss = msgpack.unpackb(packed_win_loss, strict_map_key=False)
    
    goals_df = pd.DataFrame.from_dict(unpacked_goals)
    saves_df = pd.DataFrame.from_dict(unpacked_saves)
    assists_df = pd.DataFrame.from_dict(unpacked_assists)
    averages_df = pd.DataFrame.from_dict(unpacked_averages)
    #win_loss_df = pd.DataFrame.from_dict(unpacked_win_loss)
    #print(win_loss_df)

    # Convert the unpacked data back into a DataFrame
    return goals_df, saves_df, assists_df, averages_df #, win_loss_df
    