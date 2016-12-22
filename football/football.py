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
import mpl_toolkits.basemap as bm
import matplotlib.pyplot as plt
import numpy as np
from bokeh.charts.attributes import color

def get_player_to_csv(cur):
    max_player_to_analyze = 20
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

def view_player(player_data_file):
    country_rating = player_data_file.groupby('country')['rating'].mean() # [u'England' 16.78754907790622]
    country_rating = country_rating.reset_index()
    min_rating = country_rating['rating'].min()
    
    country_coef = map(lambda x: x - min_rating + 5, country_rating['rating'])
    country_rating['rating'] = country_coef
    
    final_rating = {item[0] : item[1] for item in country_rating.values}
    
     # 初始化地图信息
    countries = {}
    # [横坐标, 纵坐标, 点大小]
    countries["England"] = [-0.12, 51.5, 20.0]
    countries["Belgium"] = [4.34, 50.85, 20.0]
    countries["France"] = [2.34, 48.86, 20.0]
    countries["Germany"] = [13.4, 52.52, 20.0]
    countries["Italy"] = [12.49, 41.89, 20.0]
    countries["Netherlands"] =[4.89, 52.37, 20.0]
    countries["Poland"] = [21.01, 52.23, 20.0]
    countries["Portugal"] = [-9.14, 38.73, 20.0]
    countries["Scotland"] = [-4.25, 55.86, 20.0]
    countries["Spain"] = [-3.70, 40.41, 20.0]
    countries["Switzerland"] = [6.14, 46.2, 20.0]
    
    for country in final_rating.keys():
        countries[country][2] = 3 * final_rating[country]
    plt.figure(figsize=(12, 12))
    
    m = bm.Basemap(projection='cyl', llcrnrlat = 35, urcrnrlat = 58, llcrnrlon = -10, urcrnrlon = 22, resolution='f')
    m.drawcounties(linewidth = 0.2)
    m.fillcontinents(color = 'lavender', lake_color= '#907099')
    m.drawmapboundary(linewidth = 0.2, fill_color = '#000040')
    m.drawparallels(np.arange(-90, 90, 30), labels=[0, 0, 0, 0], color = 'white', linewidth = 0.5)
    m.drawmeridians(np.arange(0, 360, 30), labels=[0, 0, 0, 0], color = 'white', linewidth = 0.5)
    
    for counrty in final_rating.keys():
        m.plot(countries[counrty][0], countries[counrty][1], 'bo', markersize = countries[counrty][2], color = 'r')
    # 添加国家名称
    for label, xpt, ypt in zip(list(countries.keys()), np.array(list(countries.values()))[:,0],\
                               np.array(list(countries.values()))[:,1]):
        plt.text(xpt - 0.85, ypt, label, fontsize = 20, color="black")
    plt.show()
    
    # 保存数据的可视化
    plt.savefig('./files/country_rank.png')
    
    
def main():
    # 解压缩文件
    file_path = './files'
    file_name = 'soccer.zip'
    zip_file_path = os.path.join(file_path, file_name)
    data_file_name = get_dataset_file_name(zip_file_path)
    unzip(zip_file_path, file_path)
    database_path = os.path.join(file_path, data_file_name)
    conn, cur = sqlite_tools.connect_sqlite(database_path)
    
    player_data_file = get_player_to_csv(cur)
    view_player(player_data_file)
    
    sqlite_tools.close_connect(conn)
    if os.path.exists(database_path):
        os.remove(database_path)
    
if __name__ == '__main__':
    main()