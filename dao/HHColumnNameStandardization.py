'''
 HH名列标准化
 1、解析文件》》
 2、列名匹配，标准化,补充模板
 3、对关键列进行判断，做异常记录
'''

# *****************导包区**********************
import pandas as pd
from pathlib import Path
import os
from dao.hh_nameList import *
import arrow

# *****************常量区**********************
original_pathDir = r'C:\Users\xiaofei.yu\Desktop\测试数据\HH\源文件'
standard_pathDir = r'C:\Users\xiaofei.yu\Desktop\测试数据\HH\标准后'
optimize_pathDir = r'C:\Users\xiaofei.yu\Desktop\测试数据\HH\需要单家优化'
exception_pathDir = r'C:\Users\xiaofei.yu\Desktop\测试数据\HH\异常需手工'
month = arrow.now().shift(months =-1).strftime('%Y%m')
# *****************方法区**********************

def Read_dirfile(pathDir, root):
    list_file = []
    for fileName in os.listdir(pathDir):
        if Path(fileName).match(root):
            file = os.path.join(pathDir, fileName)
            list_file.append(file)
    return list_file


def Read_Data(file):
    try:
        df = pd.read_excel(file)
    except:
        try:
            df = pd.read_csv(file, encoding='utf-8')
        except:
            try:
                df = pd.read_csv(file, encoding='gbk')
            except:

                df = pd.DataFrame()

    return df


def pty_columns(original_columns,list_rules):
    a = 0
    for column in original_columns:
        if column in list_rules[5]:
            a += 1
    return a



def normal(file,standard_pathDir,optimize_pathDir,exception_pathDir,list_rules):
    exception = False
    rule_columns = []
    standard_file_name = Path(file).parts[-1].split('_')[1] + '.xlsx'
    original_df = Read_Data(file)
    original_columns = original_df.columns.tolist()
    if pty_columns(original_columns,list_rules) >=2:
        original_df.to_excel(optimize_pathDir + '/' + '原始文件有多个列匹配到数量列' +standard_file_name, index=None)
    else:
        for list_rule in list_rules:
            flag = False
            rule_columns.append(list_rule[0])
            for original_column in original_columns:
                if original_column in list_rule:
                    flag = True
                    if list_rule[0] not in original_df.columns.tolist():
                        original_df.rename(columns={original_column: list_rule[0]}, inplace=True)

            if flag == False:
                original_df[list_rule[0]] = ''
                if list_rule[0] in ['产品名称', '产品编号', '产品规格', '批号', '销售数量', '客户名称']:
                    exception = True

        if exception == False:
            original_df_count = original_df['销售数量'].sum()
            # if original_df_count
            original_df[rule_columns].to_excel(standard_pathDir + '/' + standard_file_name, index=None)
        else:
            original_df[rule_columns].to_excel(optimize_pathDir + '/' + '关键列为空'+standard_file_name, index=None)



def columnsName_x(original_pathDir, standard_pathDir,optimize_pathDir, exception_pathDir, list_rules):

    flie_list = Read_dirfile(original_pathDir, '202009_*.*')
    for file in flie_list:
        standard_file_name = Path(file).parts[-1].split('_')[1] + '.xlsx'
        if Path(file).match('*.csv'):
            normal(file,standard_pathDir,optimize_pathDir,exception_pathDir,list_rules)
        else:
            df = pd.io.excel.ExcelFile(file)
            if df.sheet_names.__len__() == 1:
                normal(file, standard_pathDir, optimize_pathDir,exception_pathDir, list_rules)
            else:
                exception_file = pd.read_excel(file)
                exception_file.to_excel(exception_pathDir + '/' + '源文件含多个sheet'+standard_file_name, index=None)




# *****************main区**********************
if __name__ == '__main__':
    columnsName_x(original_pathDir, standard_pathDir, optimize_pathDir,exception_pathDir, s_namelist)
