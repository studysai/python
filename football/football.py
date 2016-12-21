# coding=utf-8
'''
Created on 2016年12月21日

@author: giuseppe
'''
from zip_tools import unzip, get_dataset_file_name
import os
import sqlite_tools
import proc_tool
import pandas as pd

def get_player_to_csv(cur):
    max_player_to_analyze = 200
    sql = 'select * from player limit %i' %max_player_to_analyze
    players = cur.execute(sql).fetchall()
    
    name_list = [player['player_name'] for player in players]
    birthday_list = [player['birthday'] for player in players]
    weight_list = [player['weight'] for player in players]
    height_list = [player['height'] for player in players]
    age_list = map(proc_tool.get_age_for_football_players, birthday_list)
    rating_list = [proc_tool.get_overall_rating(cur, player['player_api_id']) for player in players]
    player_country_list = [proc_tool.get_current_team_and_country(cur, player['player_api_id']) for player in players]
    team_list, country_list, n_teams = zip(*player_country_list)
    
    name_se = pd.Series(name_list, name = 'name')
    birthday_se = pd.Series(birthday_list, name = 'birthday')
    weight_se = pd.Series(weight_list, name = 'weight')
    height_se = pd.Series(height_list, name = 'height')
    age_se = pd.Series(age_list, name = 'age')
    rating_se = pd.Series(rating_list, name = 'rating')
    team_se = pd.Series(team_list, name = 'team')
    country_se = pd.Series(country_list, name = 'country')
    n_teams_se = pd.Series(n_teams, name = '#teams')
    
    player_data_file = pd.concat([name_se, birthday_se, weight_se, height_se, age_se, 
                                  rating_se, team_se, country_se, n_teams_se], axis = 1)
    csv_file_path = './files/player.csv'
    player_data_file.to_csv(csv_file_path, indx = None, encoding = 'utf-8')
    return player_data_file
    
def main():
    # 解压缩文件
    file_path = './files'
    file_name = 'soccer.zip'
    zip_file_path = os.path.join(file_path, file_name)
    data_file_name = get_dataset_file_name(zip_file_path)
    unzip(zip_file_path, file_path)
    database_path = os.path.join(file_path, data_file_name)
    conn, cur = sqlite_tools.connect_sqlite(database_path)
    
    get_player_to_csv(cur)
    
    sqlite_tools.close_connect(conn)
    if os.path.exists(database_path):
        os.remove(database_path)
    
if __name__ == '__main__':
    main()