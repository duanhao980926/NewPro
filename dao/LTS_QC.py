import pandas as pd
import os
from pathlib import Path
import datetime
from dateutil.parser import parse
# '/ftp/gk/lts/daily'
# 'C:/Users/xiaofei.yu/Desktop/测试数据/daily'
today = datetime.datetime.now().strftime('%Y%m%d')
file_path = r'C:\Users\xiaofei.yu\Desktop\测试数据\LTS'
s_aim_file_path = file_path + '/LTS-销售日采集-' + today + '.csv'
p_aim_file_path = file_path + '/LTS-采购日采集-' + today + '.csv'
i_aim_file_path = file_path + '/LTS-库存日采集-' + today + '.csv'

def read_data(fh):
    try:
        df = pd.read_excel(fh)
    except Exception as e:
        try:
            df = pd.read_csv(fh,encoding='utf-8')
        except Exception as e :
            try:
                df = pd.read_csv(fh,encoding='gbk')
            except Exception as e:
                print(fh+'读取不了！'+str(e))
                df = pd.DataFrame()
    return df

def read_file(path,rule):
    for file_name in os.listdir(path):
        if Path(file_name).match(rule):
            file = os.path.join(path,file_name)
            df = read_data(file)
    return df

def getYearMoth(date):
    return date.strftime("%Y%m")


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass


def Check_S(df):
    df['销售日期'] = pd.to_datetime(df['销售日期'])
    df['年月'] = df['销售日期'].apply(lambda a:getYearMoth(a))
    df_month = df.drop_duplicates(subset=['经销商代码','经销商名称','年月'])[['经销商代码','经销商名称','年月']]
    def get_sum(df, code, ym):
        df = df[df['经销商代码'] == code]
        df = df[df['年月'] == ym]
        return df['销售数量'].sum()

    df_month['总数量'] = df_month.apply(lambda x:get_sum(df,x['经销商代码'],x['年月']),axis=1)
    df_month.to_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\LTS\LTS月份销量汇总-'+today+'.xlsx',index=False)

def Check_P(df):
    df['购入日期'] = pd.to_datetime(df['购入日期'])
    df['年月'] = df['购入日期'].apply(lambda a:getYearMoth(a))
    df_month = df.drop_duplicates(subset=['经销商代码','经销商名称','年月'])[['经销商代码','经销商名称','年月']]
    def get_sum(df, code, ym):
        df = df[df['经销商代码'] == code]
        df = df[df['年月'] == ym]
        return df['采购数量'].sum()

    df_month['总数量'] = df_month.apply(lambda x:get_sum(df,x['经销商代码'],x['年月']),axis=1)
    df_month.to_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\LTS\LTS月份采购汇总-'+today+'.xlsx',index=False)

def Check_I(df):
    df['统计日期'] = pd.to_datetime(df['统计日期'])
    df['年月'] = df['统计日期'].apply(lambda a:getYearMoth(a))
    df_month = df.drop_duplicates(subset=['经销商代码','经销商名称','年月'])[['经销商代码','经销商名称','年月']]
    def get_sum(df, code, ym):
        df = df[df['经销商代码'] == code]
        df = df[df['年月'] == ym]
        return df['数量'].sum()

    df_month['总数量'] = df_month.apply(lambda x:get_sum(df,x['经销商代码'],x['年月']),axis=1)
    df_month.to_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\LTS\LTS月份库存汇总-'+today+'.xlsx',index=False)

#筛选筛选出重复流向经销商
def Check_RepeatS(df):
    print('正在处理经销商本身的重复...')
    print(df.shape[0])

    df.groupby(['经销商代码'])['销售数量'].count().to_excel("cf_all.xlsx")
    df1 = df.duplicated()
    print(df1.shape[0])
    df_cf = df.drop_duplicates(subset=['销售日期', '经销商代码', '购入客户名称', '产品名称', '销售数量'])
    print(df_cf.shape[0])

    df_cf.groupby(['经销商代码'])['购入客户名称'].count().to_excel("cf_after.xlsx")
    #
    df_cf1 = df.drop_duplicates(subset=['销售日期', '经销商代码', '购入客户名称', '产品名称', '销售数量'], keep=False)
    df_cf1 = df_cf1.append(df_cf).drop_duplicates(subset=['销售日期', '经销商代码', '购入客户名称', '产品名称', '销售数量'], keep=False)
    cf3 = df_cf1.groupby(['经销商代码'])['销售数量'].count().reset_index()
    # cf3.to_excel('cf_lvvvv.xlsx')
    #
    cf1 = pd.read_excel('cf_after.xlsx')

    cf2 = pd.read_excel('cf_all.xlsx')

    cf_lv = cf1.merge(cf2, how='left', on='经销商代码')

    for i in range(cf_lv.shape[0]):
        cf_lv.at[i, '重复率'] = float(cf_lv.loc[i, '销售数量']) / float(cf_lv.loc[i, '购入客户名称'])

    # cf_lv.to_excel('cf_lv.xlsx')

    cf_bl = cf3.merge(cf1, how='left', on='经销商代码')

    for i in range(cf_bl.shape[0]):
        cf_bl.at[i, '重复比例'] = float(cf_bl.loc[i, '销售数量']) / float(cf_bl.loc[i, '购入客户名称'])
    # cf_bl.to_excel('cf_bl.xlsx')

    z_cf = cf_bl.merge(cf_lv, how='left', on='经销商代码')

    z_cf = z_cf.loc[z_cf['重复比例'].apply(lambda a: a >= 0.9)]
    z_cf = z_cf.loc[z_cf['重复率'].apply(lambda a: a >= 2)]

    z_cf[u'重复比例'] = z_cf[u'重复比例'].apply(lambda x: format(x, '.2%'))
    z_cf[u'重复率'] = z_cf[u'重复率'].apply(lambda x: format(x, '.2%'))

    z_cf.to_excel('cf_z.xlsx')
    df_repeat = pd.read_excel('cf_z.xlsx', usecols=['经销商代码', '重复比例', '重复率'])

    df_repeat.to_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\LTS\LTS销售疑似重复流向经销商-20201225.xlsx',index=None)

    return df_repeat



def Check_RepeatP(df):
    print('正在处理经销商本身的重复...')
    print(df.shape[0])

    df.groupby(['经销商代码'])['采购数量'].count().to_excel("cf_all.xlsx")
    df1 = df.duplicated()
    print(df1.shape[0])
    df_cf = df.drop_duplicates(subset=['购入日期', '经销商代码', '供应商', '产品名称', '采购数量'])
    print(df_cf.shape[0])

    df_cf.groupby(['经销商代码'])['供应商'].count().to_excel("cf_after.xlsx")
    #
    df_cf1 = df.drop_duplicates(subset=['购入日期', '经销商代码', '供应商', '产品名称', '采购数量'], keep=False)
    df_cf1 = df_cf1.append(df_cf).drop_duplicates(subset=['购入日期', '经销商代码', '供应商', '产品名称', '采购数量'], keep=False)
    cf3 = df_cf1.groupby(['经销商代码'])['采购数量'].count().reset_index()
    # cf3.to_excel('cf_lvvvv.xlsx')
    #
    cf1 = pd.read_excel('cf_after.xlsx')

    cf2 = pd.read_excel('cf_all.xlsx')

    cf_lv = cf1.merge(cf2, how='left', on='经销商代码')

    for i in range(cf_lv.shape[0]):
        cf_lv.at[i, '重复率'] = float(cf_lv.loc[i, '采购数量']) / float(cf_lv.loc[i, '供应商'])

    # cf_lv.to_excel('cf_lv.xlsx')

    cf_bl = cf3.merge(cf1, how='left', on='经销商代码')

    for i in range(cf_bl.shape[0]):
        cf_bl.at[i, '重复比例'] = float(cf_bl.loc[i, '采购数量']) / float(cf_bl.loc[i, '供应商'])
    # cf_bl.to_excel('cf_bl.xlsx')

    z_cf = cf_bl.merge(cf_lv, how='left', on='经销商代码')

    z_cf = z_cf.loc[z_cf['重复比例'].apply(lambda a: a >= 0.9)]
    z_cf = z_cf.loc[z_cf['重复率'].apply(lambda a: a >= 2)]

    z_cf[u'重复比例'] = z_cf[u'重复比例'].apply(lambda x: format(x, '.2%'))
    z_cf[u'重复率'] = z_cf[u'重复率'].apply(lambda x: format(x, '.2%'))

    z_cf.to_excel('cf_z.xlsx')

    df_repeat = pd.read_excel('cf_z.xlsx', usecols=['经销商代码', '重复比例', '重复率'])

    df_repeat.to_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\LTS\LTS采购疑似重复流向经销商-20201225.xlsx',index=None)

    return df_repeat



if __name__ == '__main__':
    dfs = read_data(s_aim_file_path)
    dfp = read_data(p_aim_file_path)
    dfi = read_data(i_aim_file_path)

    Check_RepeatS(dfs)
    Check_RepeatP(dfp)