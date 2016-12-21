# coding=utf-8
'''
Created on 2016年12月21日

@author: giuseppe
'''
import sqlite3

def connect_sqlite(database):
    '''
                连接数据库，返回conn和cur
    '''
    with sqlite3.connect(database) as conn :
        # 设置可以按列属性访问
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def close_connect(conn):
    '''
                关闭连接
    '''
    if conn:
        conn.close()

def get_rows(cursor, table_name, is_print = False):
    '''
                获取所有行
    '''
    cursor.execute('select * from %s' %table_name)
    rows = cursor.fetchall()        
    if is_print:
        print '\n Total rows : %i' %rows[0][0]
    return rows[0][0]

def get_table_col_info(cursor, table_name, is_print = False):
    '''
                获取表信息
    '''
    cursor.execute('select * from %s' %table_name)
    rows = cursor.fetchall()
    if is_print:
        for row in rows:
            print(row)
    return rows                