#coding=utf-8
'''
Created on 2016年12月19日

@author: Administrator
'''
import numpy as np
import datetime

def main():
    testFilename = './presidential_polls.csv'
    with open(testFilename) as f:
        col_names_str = f.readline()[:-1] # [:-1]表示不读取末尾的换行符'\n'
    # 将字符串拆分，并组成列表    
    col_names_list = col_names_str.split(',')
    # 使用的列名
    user_col_list = ['enddate', 'rawpoll_clinton', 'rawpoll_trump','adjpoll_clinton', 'adjpoll_trump']
    user_col_index_list = [col_names_list.index(use_col_name) for use_col_name in user_col_list]
    print user_col_index_list 
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
    
    
    
    
if __name__ == "__main__" :
    main()    