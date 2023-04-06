import requests
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt

response = requests.get("https://zsr.octane.gg/players?tag=noly")
response = response.json()
keys = response.keys()
user = pd.DataFrame(response['players'])
u_id = user.iloc[0]['_id']
print(u_id)
playerStats_url = "https://zsr.octane.gg/stats/players?stat=goals&stat=assists&stat=saves&player=" + str(u_id)
# stats_api += "player="+ str(u_id)
# print(playerStats_url)
stats = requests.get(playerStats_url)
stats = stats.json()
stats_keys = stats.keys()
user_stats = pd.DataFrame(stats['stats'])
user_stats.sort_values("events",inplace=True)
event_stat = user_stats.iloc[0]['events']
# print(event_stat)
event_df = pd.DataFrame(event_stat)
print(event_df)
# print(user_stats)
event_id10 = []
saves = []
assists = []
goals = []
e_id = event_df.iloc[0]['_id'] #changing every time???
print(e_id)
eventStats_url = "https://zsr.octane.gg/stats/players/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&player="+str(u_id) + "&after" + "2021-01-01"
eventStats = requests.get(eventStats_url)
eventStats = eventStats.json()
currEventStats_df = pd.DataFrame(eventStats['stats'])
gas = currEventStats_df.iloc[0]['stats']
gas_df = pd.DataFrame(gas.items())
gas_df.rename(columns={0:'Stat Type', 1: 'Stats'}, inplace = True)
# gas_df.sort_values('startDate')
sns.set()
sns.barplot(data=gas_df, x='Stat Type', y ='Stats')
plt.show()
# currEvent_saves = currEventStats_df.iloc['stats']
# saves.append(currEvent_saves)
# print(saves)
gas_df = pd.DataFrame()
dates = []
for i in range(10):
    e_id = event_df.iloc[i]['_id']
    eventStats_url = "https://zsr.octane.gg/stats/players/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&player=" + str(u_id)
    eventStats = requests.get(eventStats_url)
    eventStats = eventStats.json()
    currEventStats_df = pd.DataFrame(eventStats['stats'])
    currEventStats_df.sort_values(by="startDate", axis=0, inplace=True)
    gas = currEventStats_df.iloc[0]['stats']
    gas_df = pd.DataFrame(gas.items())
    gas_df["startDate"] = currEventStats_df.iloc[0]["startDate"]
    # gas_df.rename(columns={0:'Stat Type', 1: 'Stats'}, inplace = True)
    print(gas_df)
    saves.append(gas_df.iloc[2][1])
    goals.append(gas_df.iloc[1][1])
    assists.append(gas_df.iloc[0][1])
    dates.append(gas_df.iloc[0]["startDate"]) 
saves = np.array(saves)
goals = np.array(goals)
assists = np.array(assists)
# saves_avg = np.average(saves)
# goals_avg = np.average(goals)
# assists_avg = np.average(assists)

