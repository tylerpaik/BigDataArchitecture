from flask import jsonify
import requests
import pandas as pd
import numpy as np
import msgpack
import pprint
from config import redis_client


def fetch_data_and_store(gamer_tag):
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
            saves, goals, assists, averages = extract_data(data)
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
            #return player_id
    else:
        print("Throw error here, no response from API")
        return LookupError
    
def extract_data(data):
    user = pd.DataFrame(data['players'])
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
    e_id = event_df.iloc[0]['_id']
    print("event id", e_id)
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
    for dateIndex in range(len(dates)):
        yr = dates[dateIndex][2:4]
        month = dates[dateIndex][-2:]
        dates[dateIndex] = month + "-" + yr
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

def retrieve_gsaa_dfs(player_id):
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

    # Convert the unpacked data back into a DataFrame
    return goals_df, saves_df, assists_df, averages_df