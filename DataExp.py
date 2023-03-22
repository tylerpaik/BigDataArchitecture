import requests
from octanegg import Octane
import pandas as pd

response = requests.get("https://zsr.octane.gg/players?tag=noly")
response = response.json()
user = pd.read_json(response)
print(user.to_string())
# print(response.json())