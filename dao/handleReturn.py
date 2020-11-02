'''
 对入口返回的经销商与处理吐出的经销商对比
 1、读取入口返回情况
 2、读取SM
 3、加一列‘处理返回状态’，并判断它的状态
 4、新建一张sheet表，里面记录厂商发
'''

#****************导包区*************
import pandas as pd
from pathlib import Path
import os
import datetime
import logging
#***************全局变量************
path_s = './'
mapping_path = path_s+'贝林编码与总控表的映射关系.xlsx'
config_path = path_s+'handleconfig.xlsx'
today = datetime.datetime.now().strftime('%Y%m%d')
return_path = path_s+'入口与处理返回情况'+today+'.xlsx'
logging.basicConfig(level=logging.DEBUG,filename='异常记录.log',filemode='w',format='%(message)s')
#**************方法功能区***********
def d(list , a,b):
 s = ''
 if a in list:
        s ='已返回'

 if b == '无销量':
        s ='无销量'

 if a not in list and b != '无销量':
        s = '未返回'
 return s






def key(lien):
    if lien == 'LTS':
        return 'Z_'
    else:
        return str(lien)[:1]+'_'


def get_BL_CODE_list(df):
    mapping_df = pd.read_excel(mapping_path)
    df = df.merge(mapping_df,left_on = '经销商代码' ,right_on='SALES B编码',how='left')
    list_code = df['国控编码'].tolist()
    return list_code

def Read_configfile(TFP_path):
    df = pd.read_excel(TFP_path)
    Valus = []
    for i in range(0,df.shape[0]) :
        if ('文件路径' in df.at[i,'参数']) | ('附件' in df.at[i,'参数']) :
            df.at[i, '值'] = df.at[i,'值'].split(',')
        Valus.append(df.at[i,'值'])
    return Valus


def Caerte_Table():
    Values = Read_configfile(config_path)
    df_rukou = pd.DataFrame()
    for file_name in os.listdir(path_s):
        if Path(file_name).match('入口返回情况与汇总*.xlsx'):
            file = os.path.join(path_s, file_name)
            df_rukou = pd.read_excel(file,sheet_name='返回情况')
    for file_name in os.listdir(path_s):
        if Path(file_name).match('SM_*.csv') or Path(file_name).match('*Sale*.xlsx'):
            file = os.path.join(path_s,file_name)
            try:
                df_chuli = pd.read_csv(file,encoding='gbk')
            except Exception:
                try:
                    df_chuli = pd.read_excel(file)
                except Exception:
                    df_chuli = pd.DataFrame()
            if df_chuli.shape[0] > 0 :
                try:
                    df_chuli.rename(columns = {'经销商编码':'经销商代码'},inplace= True)
                except Exception:
                    df_chuli.rename(columns={'CSL WS Code': '经销商代码'},inplace= True)
            list_code = []
            if Values[0] == 'BL':
                list_code = get_BL_CODE_list(df_chuli,)
            else:
                df_chuli['经销商代码'] =key(Values[0])+df_chuli['经销商代码']
                list_code = df_chuli['经销商代码'].tolist()
            df_rukou['处理返回状态'] = df_rukou.apply(lambda a : d(list_code,a['经销商代码'],a['B2_采集结果']),axis=1)
            for i in range(0,df_rukou.shape[0]):
                if str(df_rukou.at[i,'B2_采集结果']) == '无销量':
                    df_rukou.at[i, '入口返回状态'] = '无销量'
            df_rukou.to_excel(return_path,index=None)


try:
    Caerte_Table()
except Exception as e:
    logging.info(e)