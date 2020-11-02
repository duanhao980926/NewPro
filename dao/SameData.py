'''

'''

import pandas as pd
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG,filename='Exception.log',filemode='a',format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
path = './'
config_path = path+'SameDateConfig.xlsx'
return_path = path+'疑似相同的数据.csv'

# 读取配置文件
def Read_configfile(TFP_path):
    df = pd.read_excel(TFP_path)
    Valus = []
    for i in range(0,df.shape[0]) :
        if ('文件路径' in df.at[i,'参数']) | ('附件' in df.at[i,'参数']) :
            df.at[i, '值'] = df.at[i,'值'].split(',')
        Valus.append(df.at[i,'值'])
    return Valus

def read_data(path):
    try:
        df = pd.read_csv(path,encoding='utf-8')
    except:
        df = pd.read_csv(path,encoding='gbk')

    return df

def key(df, list_key, colunm_name):
    df[colunm_name] = ''
    for key in list_key:
        df[key] = df[key].astype(str)
        df[colunm_name] = df[colunm_name] + df[key]
    return df

def carete_Date(path,config_path):
    Values = Read_configfile(config_path)
    df = pd.DataFrame()
    for file_name in os.listdir(path):
        if Path(file_name).match('SM*.csv'):
            file = os.path.join(path,file_name)
            df_data = read_data(file)
            df = df.append(df_data)

    if df.shape[0]>0:
        line = Values[0]
        if line == 'YX':
            df_same = df.groupby(['销售日期', '客户名称', '批号', '数量'])['经销商编码'].size().reset_index()
            df_same = df_same[df_same['经销商编码'] > 1]
            df_same = key(df_same, ['销售日期', '客户名称', '批号', '数量'], 'key')
            df = key(df, ['销售日期', '客户名称', '批号', '数量'], 'key')
            df = df[df['key'].apply(lambda a: a in df_same['key'].tolist())]
            df['数量'] = df['数量'].astype(int)
            df.drop(['key'], axis=1, inplace=True)
        if line == 'LEO':
            df_same = df.groupby(['交易日期', '客户名称', '产品代码', '销售数量'])['经销商代码'].size().reset_index()
            df_same = df_same[df_same['经销商代码'] > 1]
            df_same = key(df_same, ['交易日期', '客户名称', '产品代码', '销售数量'], 'key')
            df = key(df, ['交易日期', '客户名称', '产品代码', '销售数量'], 'key')
            df = df[df['key'].apply(lambda a: a in df_same['key'].tolist())]
            df['销售数量'] = df['销售数量'].astype(int)
            df.drop(['key'], axis=1, inplace=True)

        return df

if __name__ == '__main__':
    try:
        df = carete_Date(path,config_path)
        df.to_csv(return_path,encoding='gbk',index=None)
    except Exception as e:
        logging.info(e)