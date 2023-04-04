import requests
from octanegg import Octane
import pandas as pd

response = requests.get("https://zsr.octane.gg/players?tag=noly")
response = response.json()
keys = response.keys()
user = pd.DataFrame(response['players'])
print(user)
u_id = user.iloc[0]['_id']
print(u_id)

stats_api = " https://zsr.octane.gg/stats/players" #?player=5f3d8fdd95f40596eae240d3
# stats_api += "player="+ str(u_id)
print(stats_api)
stats = requests.get(stats_api)
print(stats.json)