import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from config import redis_client
from flask import jsonify
from data import retrieve_gsaa_dfs

def visualize_player(player_id):
    # player_name = request.form.get('player_name')
    # if player_name:
    #     u_id, fig_data = calc_stats(player_name)
    #     redis_client.set(player_name, u_id)
    #     return jsonify({'image_data': fig_data})
    # else:
    #     return "Error: Player name is missing.", 400

    plt.style.use('dark_background')
    # plt.figure(facecolor='blue')
    fig, axes = plt.subplots(2,2)
    fig.set_figheight(7)
    fig.set_figwidth(7)

    goals_df, saves_df, assists_df, avg_df = retrieve_gsaa_dfs(player_id)

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
    return jsonify({'image_data': fig_data})