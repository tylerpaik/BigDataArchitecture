import requests
import pandas as pd
import json

response = requests.get("https://zsr.octane.gg/players?tag=noly")
response = response.json()
keys = response.keys()
user = pd.DataFrame(response['players'])
u_id = user.iloc[0]['_id']
print(u_id)
playerStats_url = "https://zsr.octane.gg/stats/players?stat=goals&stat=assists&stat=saves&player=5f3d8fdd95f40596eae23d97"
# stats_api += "player="+ str(u_id)
# print(playerStats_url)
stats = requests.get(playerStats_url)
stats = stats.json()
stats_keys = stats.keys()
user_stats = pd.DataFrame(stats['stats'])

event_stat = user_stats.iloc[0]['events']
# print(event_stat)
event_df = pd.DataFrame(event_stat)
print(event_df)
# print(user_stats)
event_id10 = []
saves = []
assists = []
goals = []
e_id = event_df.iloc[0]['_id']
eventStats_url = "https://zsr.octane.gg/stats/players/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id) + "&player="+str(u_id)
eventStats = requests.get(eventStats_url)
eventStats = eventStats.json()
currEventStats_df = pd.DataFrame(eventStats['stats'])
print(currEventStats_df)
# currEvent_saves = currEventStats_df.iloc['stats']
# saves.append(currEvent_saves)
# print(saves)


# for i in range(10):
#     e_id = event_df.iloc[i]['_id']
#     eventStats_url = "https://zsr.octane.gg/stats/players/events?stat=goals&stat=assists&stat=saves&event=" + str(e_id)
#     eventStats = requests.get(eventStats_url)
#     eventStats = eventStats.json()
#     currEventStats_df = pd.DataFrame(eve)
#     saves.append(eventStats_url
