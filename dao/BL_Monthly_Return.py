'''
 制作贝林月数据返回情况表
 1、生成月数据返回情况模板
 2、读取月数据
 3、判断定返回状态
 4、填写未返回分类
 5、生成表格
'''

#*************导包区*****************
import pandas as pd
from pathlib import Path
import os
import sys
import logging
import arrow
#*************变量区*****************
path = './'
mode_name = ['SALES B编码','国控编码','SALES B名称','省份','大区']
return_name = ['SALES B编码','国控编码','SALES B名称','省份','大区','q收集方式','q最近沟通记录','B2_采集结果']
columns_name = ['SALES B编码','国控编码','SALES B名称','省份','大区','返回方式','贝林数据返回情况','未返回分类','具体描述']
logging.basicConfig(level=logging.DEBUG,filename='new.log',filemode='a',format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
WS_code_list = []
totl_code_list = []
mode_code_list = []
lastMothly = arrow.now().shift(months = -1).strftime('%Y%m')
today = arrow.now().strftime('%Y%m%d')
df_mode = pd.DataFrame()
df_con = pd.DataFrame()
classification = [
    ('合并', '已合并'),
    ('并购', '已合并'),
    ('取消打单', '取消打单'),
    ('无需采集', '确认无需采集'),
    ('不收集', '确认无需采集'),
    ('不用再收集', '确认无需采集'),
    ('不需要采集', '确认无需采集'),
    ('不用采集', '确认无需采集'),
    ('需协议', '需协议'),
    ('未签协议', '需协议'),
    ('流向费', '需流向费'),
    ('需收费', '需流向费'),
    ('联系方式', '无联系方式'),
    ('无法提供', '暂时无法提供'),
    ('不提供', '暂时无法提供'),
    ('下月', '下月补录'),
    ('补录', '下月补录'),
    ('次月补录', '下月补录'),
    ('不合作', '不合作'),
    ('未合作', '不合作'),
    ('无合作', '不合作')
]
#*************功能区*****************
def a(list1,list2):
    b = False
    set1 = set(list1)
    set2 = set(list2)
    list3 = []
    if set1.__len__()> set2.__len__() :
        b = True
        set3 = set1 - set2
        list3 = list(set3)
    return b,list3


def b(list1,a):
    if a in list1:
        return '已返回-已交付'

def c(a):
    if a == 'ADI' or a == 'FTP':
        return 'ADI'
    else:
        return '邮件'

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

def desc(status, description):
    if status in ['未返回']:
        return str(description).replace('；', ';').split(';')[0]
    else:
        return ''

def group(description):
    for d, g in classification:
        if description.find(d) != -1:
            return g
        else:
            pass

def Caerte_Mode():
    for file_name in os.listdir(path):
        if Path(file_name).match('*Sales*.xlsx'):
            file = os.path.join(path,file_name)
            df = pd.read_excel(file,sheet_name= 'detail')
            df = df.drop_duplicates('CSL WS Code')
            WS_code_list = df['CSL WS Code'].tolist()
        if Path(file_name).match('_贝林月数据*.xlsx'):
            file = os.path.join(path, file_name)
            df_mode_last = pd.read_excel(file)
            df_mode_last = df_mode_last[df_mode_last['贝林数据返回情况'] == '已返回-已交付']
            add_WS_code = df_mode_last['SALES B编码'].tolist()
            WS_code_list = WS_code_list.__add__(add_WS_code)
        if Path(file_name).match('控制总表*.xlsx'):
            file = os.path.join(path, file_name)
            df_con = pd.read_excel(file)
            df_con = df_con.loc[df_con['经销商代码'].apply(lambda a : str(a)[:2]=='B_')]
            df_con['q收集标记'].fillna('nan', inplace=True)
            df_con = df_con.loc[df_con['q收集标记'].apply(lambda a: str(a) !='nan')]
            df_con = df_con.loc[df_con['q收集标记'].apply(lambda a: int(str(a)[:6]) >= int(lastMothly))]
            totl_code_list = df_con['经销商代码'].tolist()
        if Path(file_name).match('贝林*模板.xlsx'):
            file = os.path.join(path, file_name)
            df_mode = pd.read_excel(file)
            mode_code_list = df_mode['国控编码'].tolist()

    j = a(totl_code_list, mode_code_list)
    print(totl_code_list)
    print(mode_code_list)
    if j[0] == True:
        logging.info('打名名单中出现了模板中没有的经销商--'+str(j[1])+'，需手动更新模板！')
        sys.exit()
    df_mode = df_mode[mode_name]
    df_return = df_mode.merge(df_con, left_on='国控编码', right_on='经销商代码', how='left')
    df_return = df_return[return_name]
    df_return['返回方式'] = df_return['q收集方式'].apply(lambda a : c(a))
    df_return['贝林数据返回情况'] = df_return.apply(lambda a :d(a['B2_采集结果'],a['SALES B编码'],WS_code_list),axis=1)
    df_return['具体描述'] = df_return.apply(lambda a : desc(a['贝林数据返回情况'],a['q最近沟通记录']),axis=1)
    df_return['未返回分类'] = df_return.apply(lambda x: group(x['具体描述']),axis=1)
    df_return = df_return[columns_name]
    df_return['SALES B编码'] = df_return['SALES B编码'].astype(str)

    df_return.to_excel('贝林月数据返回情况-'+today+'.xlsx',index=None)




#*************main（）***************
if __name__ == '__main__':
    Caerte_Mode()