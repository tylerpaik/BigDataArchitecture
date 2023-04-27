# import for development, hosting locally
from flask import Flask, request, jsonify
import requests
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib
# need to use this Matplotlib backend, otherwise the app keeps crushing
matplotlib.use('Agg') # in case plt is used
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import schedule
import time

from config import redis_client

def clear_database(redis_client):
    redis_client.flushdb()
    print("Database cleared")

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

def get_team_names():
    url = "https://zsr.octane.gg/teams"
    response = requests.get(url)
    response_data = response.json()
    teams_df = pd.DataFrame(response_data['teams'])
    unique_team_names = teams_df['name'].unique()
    return unique_team_names


def teams():
    unique_team_names = pd.Series(get_team_names())
    return jsonify(team_names=unique_team_names.tolist())

