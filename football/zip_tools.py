# coding=utf-8
'''
Created on 2016年12月21日

@author: giuseppe
'''
import zipfile

def unzip(zip_file_path, dest_path):
    '''
                解压zip包
    '''
    with zipfile.ZipFile(zip_file_path) as zf:
        zf.extractall(path = dest_path)

def get_dataset_file_name(zip_file_path):
    '''
                获取数据库文件名
    '''
    with zipfile.ZipFile(zip_file_path) as zf:
        return zf.namelist()[0]
                