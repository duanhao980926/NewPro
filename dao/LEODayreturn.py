'''
 LEO日数据返回情况表
 1、读取总控表获取做直连经销商的名单
 2、对名单内的经销商进、销、存的返回情况进行记录
 3、对返回情况表进行统计汇总
'''

#****************导包区****************
import pandas as pd
from pathlib import Path
import os

#****************常量区****************
path = '/'

#****************方法区****************
def Read_dir_file(PathDir,root):
    for fileName in os.listdir(PathDir):
        if Path(fileName).match(root):
            file = os.path.join(PathDir,fileName)
            try:
                df = pd.read_csv(file,encoding='utf-8')
            except Exception as e :
                df = pd.read_csv(file, encoding='gbk')
            except Exception as e:
                df = pd.read_excel(file)
            except Exception as e:
                df = pd.DataFrame()

    return df

def LEODayRet():
    df_con = Read_dir_file(path,'控制总表*.xlsx')
    df_con = Read_dir_file(path, '返回情况表*.xlsx')
    df_con = Read_dir_file(path, '控制总表*.xlsx')
    df_con = Read_dir_file(path, '控制总表*.xlsx')
    df_con = Read_dir_file(path, '控制总表*.xlsx')
#****************mian区****************