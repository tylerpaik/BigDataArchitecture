import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import jsonify
from data import retrieve_player_dfs, retrieve_team_dfs

def visualize_player(player_id):
    plt.style.use('dark_background')
    # plt.figure(facecolor='blue')
    fig, axes = plt.subplots(2,2)
    fig.set_figheight(7)
    fig.set_figwidth(7)

    goals_df, saves_df, assists_df, avg_df = retrieve_player_dfs(player_id, 1)

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

def visualize_team(team_id):
    plt.style.use('dark_background') #making graphs darkmode
    fig, axes = plt.subplots(2,2)
    fig.set_figheight(7)
    fig.set_figwidth(7)

    goals_df, saves_df, assists_df, avg_df = retrieve_team_dfs(team_id) #, win_loss_df = retrieve_team_dfs(team_id)
    print(saves_df)

    sns.lineplot(ax = axes[0][0], data=saves_df, x='Date', y ='Saves')  #line plot for saves
    axes[0][0].set_title("Saves/game in the last 10 events")
    axes[0][0].tick_params(axis='x', rotation = 30)

    sns.lineplot(ax = axes[0][1], data=goals_df, x ='Date', y = 'Goals') #line plot for goals
    axes[0][1].set_title("Goals/game in the last 10 events")
    axes[0][1].tick_params(axis='x', rotation = 30)

    sns.lineplot(ax = axes[1][0], data=assists_df, x = 'Date', y = 'Assists') #line plot for assists
    axes[1][0].set_title("Assists/game in the last 10 events")
    axes[1][0].tick_params(axis='x', rotation = 30)

    sns.barplot(ax = axes[1][1], data=avg_df, x='Stat Type', y='Averages') #bar plot for averages
    axes[1][1].set_title("Average Stats for the last 10 events")
    axes[1][1].tick_params(axis='x', rotation = 30)


    #sns.lineplot(ax = axes[1][1], data=win_loss_df, x = 'Date', y='Wins/Total Games') #lineplot for win/total games for each event
    #axes[1][1].set_title("Wins/Total games for the last 10 events")
    #axes[1][1].tick_params(axis='x', rotation = 30)
    fig.subplots_adjust(hspace=0.5)
    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png') #returnable graphs
    fig_buffer.seek(0)
    fig_data_team = base64.b64encode(fig_buffer.getvalue()).decode()

    plt.close()
    return jsonify({'image_data': fig_data_team})