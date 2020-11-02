'''
  制作LTS日数据返回情况表
  1、定表头
  2、读数据，给表赋值
  3、生成表格
'''

#**********导包区*****************
import pandas as pd
import datetime
from pathlib import Path
import sys
import time
#**********控制在哪个时间段运行*************
hour = sys.argv[1]

now = time.strftime("%H")
if hour != now:
    print('时机不对， 我先走了')
    sys.exit()
else:
    # time.sleep(300)
    pass
#**********全局变量区*************
table_head = ['经销商代码','经销商名称','收集方式','采集产品','打单公司','销售返回状态','采购返回状态','库存返回状态']
rename_data = {'ftpuser':'经销商代码','username':'经销商名称','matching':'收集方式'}
lst_path = r'./lts_property.xlsx'
today = datetime.datetime.now().strftime('%Y%m%d')
file_path = '/ftp/gk/lts/daily'
s_aim_file_path = file_path + '/LTS-销售日采集-' + today + '.csv'
p_aim_file_path = file_path + '/LTS-采购日采集-' + today + '.csv'
i_aim_file_path = file_path + '/LTS-库存日采集-' + today + '.csv'
DReturn_aim_file_path = file_path + '/LTS-日数据返回情况表-' + today + '.xlsx'

list_aim_file_path = [s_aim_file_path,p_aim_file_path,i_aim_file_path]
#*************方法区*************
#对返回情况进行判断
def log(code,list_code):
    if code in list_code:
        return '已返回-已交付'
    else:
        return '未返回-待修复'
#制作表格，并对返回情况进行判断，后生成表格
def CreateTable(lst_path,table_head,list_aim_file_path):
    print('开始制作表格')
    df = pd.read_excel(lst_path)
    df.rename(columns = rename_data,inplace = True)
    df['采集产品'] = '雷替斯'
    df['打单公司'] = '阙天'
    for file_path in list_aim_file_path :
        if Path(file_path).parts[-1][4:6] == '销售':
            S_list = pd.read_csv(file_path)['经销商代码'].tolist()
        elif Path(file_path).parts[-1][4:6] == '采购':
            P_list = pd.read_csv(file_path)['经销商代码'].tolist()
        elif Path(file_path).parts[-1][4:6] == '库存':
            I_list = pd.read_csv(file_path)['经销商代码'].tolist()
    df['销售返回状态'] = df['经销商代码'].apply(lambda a :log(a,S_list))
    df['采购返回状态'] = df['经销商代码'].apply(lambda a :log(a,P_list))
    df['库存返回状态'] = df['经销商代码'].apply(lambda a :log(a,I_list))
    df_table = df[table_head]
    df_table.to_excel(DReturn_aim_file_path,index=None)
    print('表格制作完成')


#************mian/调用区****************

CreateTable(lst_path,table_head,list_aim_file_path)