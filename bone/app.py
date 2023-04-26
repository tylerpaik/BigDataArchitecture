# import for development, hosting locally
from flask import Flask, render_template, request, jsonify, send_file
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
import redis as r
import schedule
import time
import threading

# create a Flask app instance, default dir
app = Flask(__name__, static_folder = "static")
# get the unique team names for select dropdown purpose, use it?
# store them locally to avoid multiple api calls

#Instantiate redis db
redis_client = r.Redis(host='localhost', port=6379, decode_responses=True)

def clear_database():
    redis_client.flushdb()
    print("Database cleared")

# Schedule the 'clear_database' function to run every hour
schedule.every(1).hours.do(clear_database)

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduling loop in a separate thread
scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
scheduler_thread.start()

# Gets all the data we need from the api, update as needed
@app.route('/fetch_data_and_store/<string:gamer_tag>', methods=['POST'])
def fetch_data_and_store(gamer_tag):
    uidURL = "https://zsr.octane.gg/players?tag=" + gamer_tag
    response = requests.get(uidURL)
    
    playerStats_url = "https://zsr.octane.gg/stats/players?stat=goals&stat=assists&stat=saves&player=" + str(u_id)
    stats = requests.get(playerStats_url)
    
    # Notes: We can check if user_id is in db, if not calculate stats here and store. 
    if response.status_code == 200:
        data = response.json()
        #(name of hash set, field name, data)
        redis_client.hset("player_data", "user_id", data['players'][0]['_id'])
        redis_client.hset("player_data", "gamer_tag", data['players'][0]['tag'])
        redis_client.hset("player_data", "team_id", data['players'][0]['team']['_id'])
        redis_client.hset("player_data", "team_name", data['players'][0]['team']['name'])
        
        return jsonify({"message": "Data fetched and stored."}), 200

    


# This would be where we do some visualizations, returns image files
@app.route('/perform_actions', methods=['GET'])
def perform_actions():
    user_id = request.args.get('user_id')

    # Retrieve data from Redis, stored in hash table
    field1 = r.hget(user_id, 'name').decode('utf-8')
    field2 = int(r.hget(user_id, 'age'))
    field3 = r.hget(user_id, 'city').decode('utf-8')

    # Generate a Seaborn plot
    plot_data = {'field1': [field1], 'field2': [field2], 'field3': [field3]}
    sns.barplot(x='field1', y='field2', data=plot_data)

    # Save the plot as an image and return it as a response
    img_io = BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    plt.close()
    return send_file(img_io, mimetype='image/png')
    
def get_team_names():
    url = "https://zsr.octane.gg/teams"
    response = requests.get(url)
    response_data = response.json()
    teams_df = pd.DataFrame(response_data['teams'])
    unique_team_names = teams_df['name'].unique()
    return unique_team_names

# take from Data Exp. generalize for different players
# create more plots and tables here for a given player
#@app.route('/calc_stats', methods=['POST'])
def calc_stats(gamerTag):
    uidURL = "https://zsr.octane.gg/players?tag=" + gamerTag
    response = requests.get(uidURL)
    response = response.json()
    user = pd.DataFrame(response['players'])
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
    e_id = event_df.iloc[0]['_id'] #changing every time???
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

    plt.style.use('dark_background')
    # plt.figure(facecolor='blue')
    fig, axes = plt.subplots(2,2)
    fig.set_figheight(7)
    fig.set_figwidth(7)

    sns.lineplot(ax = axes[0][0], data=saves_df, x='Date', y ='Saves', errorbar=None)  #line plot for saves
    axes[0][0].set_title("Saves in the last 10 events")
    axes[0][0].tick_params(axis='x', rotation = 30)
    # plt.setp(plt.xticks()[0][0], rotation=30, horizontalalignment='right')

    sns.lineplot(ax = axes[0][1], data=goals_df, x ='Date', y = 'Goals', errorbar=None) #line plot for goals
    axes[0][1].set_title("Goals in last 10 events")
    axes[0][1].tick_params(axis='x', rotation = 30)


    sns.lineplot(ax = axes[1][0], data=assists_df, x = 'Date', y = 'Assists', errorbar=None) #line plot for assists
    axes[1][0].set_title("Assists in last 10 events")
    axes[1][0].tick_params(axis='x', rotation = 30)


    sns.barplot(ax = axes[1][1], data=avg_df, x='Stat Type', y='Averages', errorbar=None) #bar plot for averages
    axes[1][1].set_title("Average Stats in last 10 events")
    axes[1][1].tick_params(axis='x', rotation = 30)
    
    fig.subplots_adjust(hspace = .5)
    # replace plt.show() here
    # save the plots as a figure
    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png')
    fig_buffer.seek(0)
    fig_data = base64.b64encode(fig_buffer.getvalue()).decode()

    plt.close()
    return u_id, fig_data

# assign routes within Flask
@app.route('/')
def index():
    return render_template('rlBetting.html')

@app.route('/teams')
def teams():
    unique_team_names = pd.Series(get_team_names())
    return jsonify(team_names=unique_team_names.tolist())

@app.route('/visualize_player', methods=['POST'])
def visualize_player():
    player_name = request.form.get('player_name')
    if player_name:
        u_id, fig_data = calc_stats(player_name)
        redis_client.set(player_name, u_id)
        return jsonify({'image_data': fig_data})
    else:
        return "Error: Player name is missing.", 400


# add visualize_team() separately if needed | create a different button w unique id if doing so

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
    redis_client.close()
