#coding=utf-8
'''
Created on 2016年12月19日

@author: Administrator
'''
import numpy as np
import datetime

def is_convert_float(s):
    """
         判断一个字符串能否转换为float
    """
    try:
        float(s)
    except:
        return False
    
    return True

def get_sum(str_array):
    """
        返回字符串数组中数字的总和
    """
    # 去掉不能转换成数字的数据
    cleaned_data = filter(is_convert_float, str_array)
    
    # 转换数据类型
    float_array = np.array(cleaned_data, np.float)
    
    return np.sum(float_array)

def main():
    testFilename = './presidential_polls.csv'
    with open(testFilename) as f:
        col_names_str = f.readline()[:-1] # [:-1]表示不读取末尾的换行符'\n'
    # 将字符串拆分，并组成列表    
    col_names_list = col_names_str.split(',')
    # 使用的列名
    user_col_list = ['enddate', 'rawpoll_clinton', 'rawpoll_trump','adjpoll_clinton', 'adjpoll_trump']
    user_col_index_list = [col_names_list.index(use_col_name) for use_col_name in user_col_list]
    data_arr = np.loadtxt(testFilename, 
                          dtype = str, 
                          delimiter = ',', 
                          skiprows = 1, 
                          usecols = user_col_index_list)
    '''
                数据处理
    '''
    enddate_idx = user_col_list.index('enddate')
    enddate_lst = data_arr[:, enddate_idx].tolist() 
    enddate_lst = [enddate.replace('-', '/') for enddate in enddate_lst]
    date_list = [datetime.datetime.strptime(enddate, '%m/%d/%Y') for enddate in enddate_lst]
    month_list = ['%d-%02d' %(date_obj.year, date_obj.month) for date_obj in date_list]
    month_arr = np.array(month_list)
    months = np.unique(month_arr)
    
    raw_data_clt = data_arr[:, user_col_list.index('rawpoll_clinton')]
    adj_data_clt = data_arr[:, user_col_list.index('adjpoll_clinton')]
    raw_data_trump = data_arr[:, user_col_list.index('rawpoll_trump')]
    adj_data_trump = data_arr[:, user_col_list.index('adjpoll_trump')]
    
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
        
    print result    
        
    
if __name__ == "__main__" :
    main()    