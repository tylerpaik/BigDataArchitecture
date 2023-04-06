import requests
import pandas as pd
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
sns.set()
ax = sns.barplot(data=gas_df, x='Stat Type', y ='Stats')
plt.show()
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



#testing seaborn html connection
html = mpld3.fig_to_html(ax.figure)