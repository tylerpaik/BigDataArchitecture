# import for development, hosting locally
from flask import Flask, jsonify, render_template, request
import requests
import schedule
import threading
import pandas as pd
#from scipy.stats import poisson

from config import redis_client
from utils import clear_database, scheduler_loop, calc_probability
from data import fetch_player, fetch_team, retrieve_player_dfs
from visualization import visualize_player, visualize_team

# create a Flask app instance, default dir
app = Flask(__name__, static_folder = "static")
# get the unique team names for select dropdown purpose, use it?
# store them locally to avoid multiple api calls

# Schedule the 'clear_database' function to run every hour
schedule.every(1).hours.do(clear_database)

# Start the scheduling loop in a separate thread
scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
scheduler_thread.start()

# assign routes within Flask
@app.route('/')
def index():
    return render_template('rlBetting.html')

@app.route('/teams')
def teams():
    unique_team_names = pd.Series(get_team_names())
    return jsonify(team_names=unique_team_names.tolist())

def get_team_names():
    url = "https://zsr.octane.gg/teams"
    response = requests.get(url)
    response_data = response.json()
    teams_df = pd.DataFrame(response_data['teams'])
    unique_team_names = teams_df['name'].unique()
    return unique_team_names

@app.route('/players')
def get_player_tags():
    url = "https://zsr.octane.gg/players"
    response = requests.get(url)
    response_data = response.json()
    players_df = pd.DataFrame(response_data['players'])
    unique_player_tags = players_df['tag'].unique()
    return jsonify(player_tags = unique_player_tags.tolist())

# Gets all the data we need from the api, update as needed
@app.route('/fetch_player_data_route', methods=['POST'])
def fetch_player_data_route():
    gamer_tag = request.form.get('player_name')
    print(gamer_tag)
    player_id = fetch_player(gamer_tag)
    return visualize_player(player_id)

@app.route('/fetch_team_data_route', methods=['POST'])
def fetch_team_data_route():
    team1 = request.form.get('team1')
    team2 = request.form.get('team2')
    team_id = fetch_team(team1)
    return visualize_team(team_id)

#@app.route('/visualize_player', methods=['POST'])
#def visualize_player_route():
#    return 0

# prob., modify
@app.route('/predict', methods=['POST'])
def predict():
    player_tag = request.form['playerTag']
    line = int(request.form['line'])
    stat = request.form['stat']

    dataframes = retrieve_player_dfs(player_tag, 0)
    print(dataframes)
    probability = calc_probability(line, dataframes[stat])
    probability = round(probability, 3)
    return {'probability': probability}

# add visualize_team() separately if needed | create a different button w unique id if doing so

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
    redis_client.close()
