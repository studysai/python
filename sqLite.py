#coding=utf-8
'''
Created on 2016年12月21日

@author: Administrator
'''
import sqlite3
def main():
    db_path = './files/test.sqlite'
    # 获取链接
    conn = sqlite3.connect(db_path)
    # 获取游标
    cur = conn.cursor()
    # 处理中文
    conn.text_factory = str
    
    cur.execute('select sqlite_version()')
    print 'sqlite 版本为 :%s' %str(cur.fetchone()[0])  
    
    cur.execute('drop table if exists book')
    cur.execute('create table book(id int, name txt, price double)')
    books = (
        (9, '人间草木', 30.00),
        (10,'你的善良必须有点锋芒', 20.50),
        (11, '这么慢,那么美', 24.80),
        (12, '考拉小巫的英语学习日记:写给为梦想而奋斗的人(全新修订版)', 23.90)
    )
    cur.executemany("INSERT INTO book VALUES(?, ?, ?)", books)
    conn.commit()
    # 索引访问
    cur.execute('select * from book')
    book_list = cur.fetchall()
    for book in book_list:
        print '%i-%s-%.2f' %(book[0], book[1], book[2])
    
    # 列名访问    
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('select * from book')
    book_list = cur.fetchall()
    for book in book_list:
        print '%i-%s-%.2f' %(book['id'], book['name'], book['price'])
    conn.close()
if __name__ == '__main__' :
    main() 
