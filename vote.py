#coding=utf-8
'''
Created on 2016年12月19日

@author: Administrator
'''
import numpy as np
import datetime
import matplotlib.pyplot as plt

"""
     判断一个字符串能否转换为float
"""
def is_convert_float(s):
    try:
        float(s)
    except:
        return False
    
    return True

"""
    返回字符串数组中数字的总和
"""
def get_sum(str_array):
    # 去掉不能转换成数字的数据, 过滤掉非数字
    cleaned_data = filter(is_convert_float, str_array)
    # 转换数据类型，将字符串转化为float
    float_array = np.array(cleaned_data, np.float)
    # 返回数组合
    return np.sum(float_array)

def main():
    '''
                数据读取
    '''
    testFilename = './presidential_polls.csv'
    with open(testFilename) as f:
        # 读取标题 
        col_names_str = f.readline()[:-1] # [:-1]表示不读取末尾的换行符'\n'
    # 将字符串拆分，并组成列表    
    col_names_list = col_names_str.split(',')
    # 使用到的列名
    user_col_list = ['enddate', 'rawpoll_clinton', 'rawpoll_trump','adjpoll_clinton', 'adjpoll_trump']
    # 使用列在原列中的列表
    user_col_index_list = [col_names_list.index(use_col_name) for use_col_name in user_col_list]
    # 获取需要
    data_arr = np.loadtxt(testFilename, 
                          dtype = str, 
                          delimiter = ',', 
                          skiprows = 1, 
                          usecols = user_col_index_list)
    '''
                数据处理
    '''
    # 日期处理
    enddate_idx = user_col_list.index('enddate')
    enddate_lst = data_arr[:, enddate_idx].tolist() 
    enddate_lst = [enddate.replace('-', '/') for enddate in enddate_lst]
    date_list = [datetime.datetime.strptime(enddate, '%m/%d/%Y') for enddate in enddate_lst]
    month_list = ['%d-%02d' %(date_obj.year, date_obj.month) for date_obj in date_list]
    month_arr = np.array(month_list)
    months = np.unique(month_arr)
    
    # 获取需要的列数据
    raw_data_clt = data_arr[:, user_col_list.index('rawpoll_clinton')]
    adj_data_clt = data_arr[:, user_col_list.index('adjpoll_clinton')]
    raw_data_trump = data_arr[:, user_col_list.index('rawpoll_trump')]
    adj_data_trump = data_arr[:, user_col_list.index('adjpoll_trump')]
    
    # 按月分组处理
    result = [] 
    for month in months:
        raw_data_clt_month = raw_data_clt[month_arr == month]
        raw_data_clt_month_sum = get_sum(raw_data_clt_month)
        adj_data_clt_month = adj_data_clt[month_arr == month]
        adj_data_clt_month_sum = get_sum(adj_data_clt_month)
        raw_data_trump_month = raw_data_trump[month_arr == month]
        raw_data_trump_month_sum = get_sum(raw_data_trump_month)
        adj_data_trump_month = adj_data_trump[month_arr == month]   
        adj_data_trump_month_sum = get_sum(adj_data_trump_month)
        result.append((month, raw_data_clt_month_sum, adj_data_clt_month_sum, raw_data_trump_month_sum, adj_data_trump_month_sum))
    
    months, raw_cliton_sum, adj_cliton_sum, raw_trump_sum, adj_trump_sum = zip(*result)
    
    #图像表示，两行两列四个图分别显示不同数据
    fig, subplot_arr = plt.subplots(2, 2, figsize = (15, 10))
    subplot_arr[0, 0].plot(raw_cliton_sum, color = 'r')
    subplot_arr[0, 0].plot(raw_trump_sum, color = 'g')
    
    width = 0.25
    x = np.arange(len(months))
    subplot_arr[0, 1].bar(x, raw_cliton_sum, width, color = 'r')
    subplot_arr[0, 1].bar(x + width, raw_trump_sum, width, color = 'g')
    subplot_arr[0, 1].set_xticks(x + width)
    subplot_arr[0, 1].set_xticklabels(months, rotation = 'vertical')
    
    subplot_arr[1, 0].plot(adj_cliton_sum, color = 'r')
    subplot_arr[1, 0].plot(adj_trump_sum, color = 'g')
    
    width = 0.25
    x = np.arange(len(months))
    subplot_arr[1, 1].bar(x, adj_cliton_sum, width, color = 'r')
    subplot_arr[1, 1].bar(x + width, adj_trump_sum, width, color = 'g')
    subplot_arr[1, 1].set_xticks(x + width)
    subplot_arr[1, 1].set_xticklabels(months, rotation = 'vertical')
    
    plt.subplots_adjust(wspace = 0.2)
    plt.show()
    
    
    
if __name__ == "__main__" :
    main()    