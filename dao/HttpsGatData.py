# coding=utf-8
# !/usr/bin/python

# 接口请求示例为：http://open.api.tianyancha.com/services/open/ic/branch/2.0?id=22822&name=北京百度网讯科技有限公司&keyword=北京百度网讯科技有限公司&pageNum=1

# pip install requests
import requests
import time
import hashlib
import json
import pandas as pd


#  token可以从 数据中心 -> 我的接口 中获取
# token = "326bb4e8-5582-47bc-b175-5b160f98530d"
# encode = 'utf-8'
#
# def getData(Name):
#     data = {'id':'',
#             'name':Name,
#             'keyword':'',
#             'pageNum':''}
#     urldata  = urllib.parse.urlencode(data)
#     urlall= "http://open.api.tianyancha.com/services/open/ic/branch/2.0?%s"%urldata
#     headers = {'Authorization': token}
#     response = requests.get(urlall, headers=headers,timeout =6)
#     time.sleep(4)
#     df = pd.DataFrame()
#     if str(response.status_code) == '200':
#         d = json.loads(response.text)
#         # 结果打印
#         # print(response.status_code)
#         total = d['result']['total']
#         items = d['result']['items']
#         list_search = []
#         list_regStatus = []
#         list_name = []
#         list_alias = []
#         list_total = []
#         for item in items:
#             list_search.append(Name)
#             list_regStatus.append(item['regStatus'])
#             list_name.append(item['name'])
#             list_alias.append(item['alias'])
#             list_total.append(total)
#         Data = {'总公司': list_search, '分公司': list_name, '分公司状态': list_regStatus, '别名': list_alias, '总家数': list_total}
#         df = pd.DataFrame(data=Data)
#     else:
#         print('有问题:',response.status_code)
#         pass
#
#     return df

def  getData_QCC(name):

    #  请求参数
    appkey = "442ef021aaa54eca822cf2f9bda0607f"
    seckey = "BDEC35EA524DE167E19FFD379685B123"
    encode = 'utf-8'

    # Http请求头设置
    timespan = str(int(time.time()))
    token = appkey + timespan + seckey;
    hl = hashlib.md5()
    hl.update(token.encode(encoding=encode))
    token = hl.hexdigest().upper();
    # print('MD5加密后为 ：' + token)

    # 设置请求Url-请自行设置Url
    reqInterNme = "http://api.qichacha.com/ECIBranch/GetList"
    paramStr = "searchKey="+name+"&pageSize=20"
    url = reqInterNme + "?key=" + appkey + "&" + paramStr;
    headers = {'Token': token, 'Timespan': timespan}
    response = requests.get(url, headers=headers,timeout =6)
    # 结果返回处理
    df = pd.DataFrame()
    if str(response.status_code) == '200':
        resultJson = json.loads(response.text)
        # print(resultJson)
        TotalRecords = resultJson['Paging']['TotalRecords']
        list_search = []
        list_Status = []
        list_name = []
        list_TotalRecords = []
        for itme in resultJson['Result'] :
            list_search.append(name)
            list_Status.append(itme['Status'])
            list_name.append(itme['Name'])
            list_TotalRecords.append(TotalRecords)
        Data = {'总公司':list_search,'分公司':list_name,'分公司状态':list_Status,'总家数':list_TotalRecords}
        df = pd.DataFrame(data=Data)
    else:
        print('有问题:', response.status_code)
        pass

    return df



def a(name1,name2):
    if name1 == name2 :
        return 'T'




def carete_Table():
    df = pd.read_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\连锁药店总部-待查分支机构数量.xlsx')
    df_data = pd.read_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\连锁药店总部-待查分支机构数量结果.xlsx')


    for i in range(0, df.shape[0]):
        try:
            if str(df.at[i, '是否查询过']) == 'nan':
                df_a = getData_QCC(df.at[i,'标准客户名称'])
                if df_a.shape[0] >0 :
                    print('第'+ str(i+1) +'次获取成功！')
                    df_data = df_data.append(df_a)
                    df.at[i,'是否查询过'] = 'T'
                    df_data.to_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\连锁药店总部-待查分支机构数量结果.xlsx',index=None)
                    df.to_excel(r'C:\Users\xiaofei.yu\Desktop\测试数据\连锁药店总部-待查分支机构数量.xlsx',index=None)
                else:
                    print('第'+ (i+1) +'次获取失败！')
        except Exception as e:
            print("出现异常-->" + str(e))
            df.at[i, '是否查询过'] = e
            pass

carete_Table()

