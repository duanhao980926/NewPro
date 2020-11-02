'''
读取文件的辅助工具py文件
'''

#导包区
import pandas as pd
import os
import re

FTP_path = r'D:\Work\Project\NewPro\data\FTP配置文件.xlsx'
# 读取配置文件
def Read_configfile(TFP_path):
    df = pd.read_excel(TFP_path)
    Valus = []
    for i in range(0,df.shape[0]) :
        if ('文件路径' in df.at[i,'参数']) | ('附件' in df.at[i,'参数']) :
            df.at[i, '值'] = df.at[i,'值'].split(',')
        Valus.append(df.at[i,'值'])
    return Valus

#在全路径中拿取文件名
def file_name(path):
    list = path.split('\\')
    index = list.__len__()
    return list[index-1]

#在某个目录下，找出某种格式（名称、尾缀）的文件
def find_file(path, rules):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:
            image_name = os.path.join(dirpath, filepath)  # 获取文件的全路径
            # image_name = filepath
            str1 = re.compile(rules + '''(.*?).xls''')
            match_obj = re.findall(str1, image_name)
            if match_obj:
                # print(image_name)
                file_list.append(image_name)
    print(file_list)
    return file_list

Valus = Read_configfile(r'D:\Work\Project\NewPro\data\邮箱自动推送配置文件.xlsx')
print(Valus)

