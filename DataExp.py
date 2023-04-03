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