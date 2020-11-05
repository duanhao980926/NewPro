'''
 营销的月数据返回情况
 1 、 确定经销商 打单名单+总控表
 2、  确定经销商返回情况与具体描述（考虑第二次增量交付）
 3、  第二次重复交付经销商的几率
'''

#****************导包区*****************
import pandas as pd
import os
import arrow
from pathlib import Path
import logging

#****************常量区*****************
path = 'D:/质检相关文件/需要质检的数据/营销'
lastMothly = arrow.now().shift(months = -1).strftime('%Y%m')
today = arrow.now().strftime('%Y/%m/%d')
dtoday = arrow.now().strftime('%Y%m%d%H%M%S')
logging.basicConfig(level=logging.DEBUG,filename='异常经销商.log',filemode='w',format='%(message)s')
path_df = path+'/GF_'+lastMothly+'_'+dtoday+'.csv'
pathT_df = path+'/Test_'+lastMothly+'_'+dtoday+'.csv'
pathT_df1 = path+'/Test1_'+lastMothly+'_'+dtoday+'.csv'
colmuns = ['年月','客户编码','客户名称','省份','城市','商业级别','区域','补采要求','采集产品','打单公司','返回状态','未返回分类','具体描述','交付日期','q收集方式','q收集标记','q手工标记','B2_采集结果','q最近沟通记录']
#****************功能区*****************

def read_CSV_data(fp):
    try:
        td = pd.read_excel(fp,sheet_name='detail')
    except Exception as err1:
        try:
            td = pd.read_csv(fp, encoding='GBK', error_bad_lines=False, warn_bad_lines=False, sep=',')
        except Exception as err2:
            try:
                td = pd.read_csv(fp, encoding='utf-8', error_bad_lines=False, warn_bad_lines=False, sep=',')
            except Exception as err3:
                try:
                    td = pd.read_csv(open(fp, 'rb'))
                except Exception as e1:
                    try:
                        td = pd.read_csv(open(fp, "r", encoding='gb2312', errors='ignore'))
                    except Exception as e:
                        print('读取不了')
                        td = pd.DataFrame()
                        print(e)
    monthlyDF = td
    return monthlyDF

#TODO 确定返回情况的列与行
def Carete_mode(path):
    df_da = pd.DataFrame()
    df_con = pd.DataFrame()
    for file_name in os.listdir(path):
        if Path(file_name).match('_GF*.csv'):
            file = os.path.join(path, file_name)
            df_da = read_CSV_data(file)
        else:
            if Path(file_name).match('*打单名单*.xlsx'):
                file = os.path.join(path,file_name)
                df_da = pd.read_excel(file)
                df_da.rename(columns={'客户编号': '客户编码'}, inplace=True)

        if Path(file_name).match('控制总表*.xlsx'):
            file = os.path.join(path, file_name)
            df_con = pd.read_excel(file)
            df_con = df_con.loc[df_con['经销商代码'].apply(lambda a: str(a)[:2] == 'Y_')]
            df_con['q收集标记'].fillna('nan', inplace=True)
            df_con = df_con.loc[df_con['q收集标记'].apply(lambda a: str(a) != 'nan')]
            df_con = df_con.loc[df_con['q收集标记'].apply(lambda a: int(str(a)[:6]) >= int(lastMothly[:6]))]
    df_con['经销商代码'] = df_con['经销商代码'].astype(str).str[2:]
    df = df_da.merge(df_con,left_on='客户编码',right_on='经销商代码',how='left')
    return df

#TODO 确定经销商返回情况与具体描述（考虑第二次增量交付）

def d(type,code,list1):
    ss = ''
    if '无销量' == str(type):
        ss = '已返回-无销量'
    elif str(type) != 'nan' and '无销量' != str(type) :
        ss = '已返回-待交付'
    else:
        ss = '未返回'

    if code in list1:
        ss =  '已返回-已交付'

    return ss


def disposal_Tpye(df):
    code_list = []
    code_list_SM = []
    for file_name in os.listdir(path):
        if Path(file_name).match('SM*.csv'):
            file = os.path.join(path,file_name)
            df_SM = read_CSV_data(file)
            code_list_SM = df_SM['经销商编码'].tolist()
            code_list = code_list.__add__(code_list_SM)
        if Path(file_name).match('_GF*.csv'):
            file = os.path.join(path,file_name)
            df_last_SM = read_CSV_data(file)
            df_last_SM = df_last_SM.loc[df_last_SM['返回状态'].apply(lambda a :str(a)=='已返回-已交付')]
            code_last_list_SM = df_last_SM['客户编码'].tolist()
            code_list = code_list.__add__(code_last_list_SM)

    df['返回状态'] = df.apply(lambda a : d(a['B2_采集结果'],a['客户编码'],code_list),axis=1)
    df['交付日期'] = df['交付日期'].astype(object)
    df['具体描述'] = df['具体描述'].astype(str)

    for i in range(0,df.shape[0]) :
        if df.at[i, '客户编码'] in code_list_SM:
            df.at[i, '交付日期'] = today
        if str(df.at[i, '返回状态']) == '未返回':
            df.at[i, '具体描述'] = str(df.at[i, 'q最近沟通记录']).replace('；',';').split(';')[0]
    df['具体描述'] = df['具体描述'].astype(object)
    for i in range(0, df.shape[0]):
        if df.at[i,'具体描述'] == 'nan':
            df.at[i,'具体描述'] = ''
    return df

#TODO 异常记录
def c(list1,list2):
    set1 = set(list1)
    set2 = set(list2)
    set3 = set1 - set2
    set4 = set1 - set3
    list_s = list(set4)
    if list_s.__len__()>0:
        logging.info(list_s+'这些经销商第上次已交付过')

def Abnormal_record(path):
    code_last_list_SM = []
    code_list_SM = []
    for file_name in os.listdir(path):
        if Path(file_name).match('_GF*.csv'):
            file = os.path.join(path, file_name)
            df_last_SM = read_CSV_data(file)
            df_last_SM = df_last_SM.loc[df_last_SM['返回状态'].apply(lambda a: str(a) == '已返回-已交付')]
            code_last_list_SM = df_last_SM['客户编码'].tolist()

        if Path(file_name).match('SM*.csv'):
            file = os.path.join(path, file_name)
            df_SM = read_CSV_data(file)
            code_list_SM = code_list_SM.__add__(df_SM['经销商编码'].tolist())
    c(code_last_list_SM,code_list_SM)



#TODO 生成营销月数据返回情况
def Carete_Table(path,path_df):
    df = Carete_mode(path)
    df_Return = disposal_Tpye(df)
    Abnormal_record(path)
    df_Return[colmuns].to_csv(path_df,index=None)


#****************main区****************
if __name__ == '__main__':
    Carete_Table(path,path_df)