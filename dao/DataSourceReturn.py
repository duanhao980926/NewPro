'''

实现入口数据返回情况的每天17:00更新
1、读取控制总表
2、拿取需要的列，与值
3、筛选出打单经销商
4、加一列入口返回状态，再做判断。

'''

#************导包区****************
import requests
import pandas as pd
import datetime
import arrow
#************全局变量区**************
table = "5997216"
list_columns = ['经销商代码','经销商名称','q收集方式','q手工标记','q最近沟通记录','B2_采集结果']
file_path = 'D:/Work/Project/NewPro/data'
lastMothly = arrow.now().shift(months = -1).strftime('%Y%m')
Today = datetime.datetime.now().strftime('%Y%m%d')
todays = datetime.datetime.now().strftime('%m/%d')
path_df =  file_path + '\入口返回情况与汇总'+Today+'.xlsx'
path_s = file_path + '\配置文件.xlsx'

#************方法功能区**************

# 获取token
def get_token():
    result = requests.post('http://services.kurite.cn/huoban/getToken',
                           data={'id': '12067898212', 'pwd': 'xjoijsdif2112'})
    return result.json()


# 根据当前token，获取对应表格的信息
def get_table(token):
    global data
    param = {'token': token, 'table': table}  # , 'name': ''
    try:
        result = requests.get('http://services.kurite.cn/huoban/getFields', params=param)
        if result.content:
            data = result.json()
        else:
            data = '暂未获取到数据'
    except Exception as e:
      print('获取token失败')
    return data


# 获取表格内容
def get_table_info(current_token):
    # 请求体必要信息
    detail_datas = []
    datas = {
        'token': current_token,
        'table': table
        , 'offset': 0
    }
    # 调用post请求，获取response
    detail_info = requests.post('http://services.kurite.cn/huoban/getTableInfo', data=datas)
    row_total = detail_info.json()['data']['total']
    offset_num = int(row_total / 500) + 1
    for offset in range(offset_num):
        datas = {
            'token': current_token,
            'table': table
            , 'offset': (offset * 500)
        }
        # 调用post请求，获取response
        detail_info = requests.post('http://services.kurite.cn/huoban/getTableInfo', data=datas)
        detail_datas.append(detail_info)
    return detail_datas


def create_ctr_table():
    res_json = get_token()
    # 获取response中的token
    current_token = res_json['data']['token']
    # 获取表格内容
    table_info = get_table_info(current_token)
    tb = pd.DataFrame()
    for i in range(len(table_info)):
        tab_json = table_info[i].json()
        zkb_data = tab_json['data']['tableInfo']
        df = pd.DataFrame(zkb_data)
        tb = pd.concat([tb, df])
    print('总控表导出成功')
    # tb.to_csv('111111111111.csv')
    return tb


def judge(a,b,c):
    if (a == 'ADI' or a == 'FTP') and str(b) == 'nan':
        return '已返回'
    elif ('手工' in a  or 'API' in a or str(b) != 'nan') and str(c) != 'nan':
        return '已返回'
    else:
        return '未返回'


def Read_configfile(TFP_path):
    df = pd.read_excel(TFP_path)
    Valus = []
    for i in range(0,df.shape[0]) :
        if ('文件路径' in df.at[i,'参数']) | ('附件' in df.at[i,'参数']) :
            df.at[i, '值'] = df.at[i,'值'].split(',')
        Valus.append(df.at[i,'值'])
    return Valus

def Create_ReturnTable():
    df = create_ctr_table()
    df['q收集标记'].fillna(0,inplace=True)
    df = df.loc[df['q收集标记'].apply(lambda a: int(str(a)[:6]) >= int(lastMothly))]
    df = df[list_columns]
    df['入口返回状态'] = df.apply(lambda a : judge(a['q收集方式'],a['q手工标记'],a['B2_采集结果']),axis = 1)
    df['处理返回状态'] = ''
    Values = Read_configfile(path_s)
    list_pro = Values[0].split(',')
    list_totl = []
    list_return = []
    list_disreturn = []
    list_lv = []
    for line in list_pro:
        if line == 'LTS' or line == 'lts':
            line = 'Z_'
        df_t = df.loc[df['经销商代码'].apply(lambda a : str(a)[:2] == line[:1]+'_')]
        totl = df_t.shape[0]
        returns = df_t.loc[df_t['入口返回状态'].apply(lambda a: str(a) == '已返回')].shape[0]
        disreturn = df_t.loc[df_t['入口返回状态'].apply(lambda a: str(a) == '未返回')].shape[0]
        lv = returns/totl
        list_totl.append(totl)
        list_return.append(returns)
        list_disreturn.append(disreturn)
        list_lv.append('{:.0%}'.format(lv))
    data = {'产线':list_pro,'家数':list_totl,'已返回':list_return,'未返回':list_disreturn,'返回占比':list_lv}
    df_f = pd.DataFrame(data=data)
    df_f['时间'] = todays

    Writer = pd.ExcelWriter(path=path_df)
    df_f.to_excel(excel_writer=Writer, sheet_name='汇总', index=None)
    df.to_excel(excel_writer=Writer,sheet_name='返回情况',index=None)
    Writer.save()
    return df

#************主方法区main************
if __name__ == '__main__':
    Create_ReturnTable()