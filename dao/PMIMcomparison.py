import pandas as pd
import logging
import os
from pathlib import Path
import win32api,win32con

logging.basicConfig(level=logging.DEBUG,filename='err.log',filemode='a',format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

path = './'

def read_data(file):
    try:
        df = pd.read_excel(file)
    except :
        try:
            df = pd.read_csv(file,encoding='gbk')
        except:
            try:
                df = pd.read_csv(file, encoding='utf-8')
            except Exception as e:
                df = pd.DataFrame()
                print('读取不了')
                logging.info(e)
    return df

def read_dir(path,rule):
    df = pd.DataFrame()
    for file_name in os.listdir(path):
        if Path(file_name).match(rule):
            file = os.path.join(path,file_name)
            df = read_data(file)
            continue
    return df

def PMComparison(path):
    df_H = read_dir(path,'_PM*.csv')
    df_N = read_dir(path, 'PM*.csv')
    sum_H = df_H['数量'].sum()
    sum_N = df_N['数量'].sum()
    if df_H.shape[0] > 0 and df_N.shape[0] > 0:
        if df_H.shape[0] == df_N.shape[0] and sum_H == sum_N:
            win32api.MessageBox(0, "这两份PM文件条数与数量总和都一致！", "提醒", win32con.MB_OK)
        else:
            win32api.MessageBox(0, "这两份PM文件不一致！", "提醒", win32con.MB_OK)
    else:
        win32api.MessageBox(0, "这两份PM文件中有一份为空或无PM文件", "提醒", win32con.MB_OK)


def IMComparison(path):
    df_H = read_dir(path,'_IM*.csv')
    df_N = read_dir(path, 'IM*.csv')
    sum_H = df_H['数量'].sum()
    sum_N = df_N['数量'].sum()
    print()
    if df_H.shape[0] > 0 and df_N.shape[0] > 0:
        if df_H.shape[0] == df_N.shape[0] and sum_H == sum_N:
            win32api.MessageBox(0, "这两份IM文件条数与数量总和都一致！", "提醒", win32con.MB_OK)
        else:
            win32api.MessageBox(0, "这两份IM文件不一致！", "提醒", win32con.MB_OK)
    else:
        win32api.MessageBox(0, "这两份IM文件中有一份为空或无IM文件!", "提醒", win32con.MB_OK)

if __name__ == '__main__':
    PMComparison(path)
    IMComparison(path)


