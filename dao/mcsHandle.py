'''
MCS原始数据处理
1、对比两张表将不同的数据筛选，生成新xlsx表的一张新增sheet表与一张红冲sheet表
2 对新生成的
'''
#**************导包区***************
import pandas as pd
import os
from pathlib import Path
import arrow
import time
import logging
#***************变量区***************
logging.basicConfig(level=logging.DEBUG,filename='new.log',filemode='a',format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
path = './'
LMonth = arrow.now().shift(months = -1).strftime('%Y%m%d')
lMonth = arrow.now().shift(months = -1).strftime('%Y%m')
llMonth = arrow.now().shift(months = -2).strftime('%Y%m')
return_path = path+'/原始流向调整后的数据.xlsx'
#***************方法区**************
def readFileByDir(Dirpath,ma):
    for file_name in os.listdir(Dirpath):
        if Path(file_name).match(ma):
            print('正在读取',file_name)
            file = os.path.join(Dirpath,file_name)
            df = pd.read_excel(file,sheet_name='流向报告')
    return df

def key(df,list_key,colunm_name):
  df[colunm_name] = ''
  for key  in list_key:
    df[key] = df[key].astype(str)
    df[colunm_name] =df[colunm_name] + df[key]
  return df

def oppositeNumber(Num):
  return -Num

def contrast():

    df_now = readFileByDir(path,lMonth+'月初版报告*.xlsx')
    df_now_histroy = df_now.loc[df_now['销售月'].apply(lambda a : str(a) != LMonth[:6])]

    df_histroy = readFileByDir(path, llMonth+'月初版报告*.xlsx')

    colunms_ID = ['销售月','经销商编码','标准产品名','DDI_ID','数量(流向单)']
    df_now_histroy = key(df_now_histroy,colunms_ID,'标识')
    df_histroy = key(df_histroy, colunms_ID, '标识')

    df_now_histroy_keylist = df_now_histroy['标识'].tolist()
    df_histroy_keylist = df_histroy['标识'].tolist()

    df_add = df_now_histroy[df_now_histroy['标识'].apply(lambda a: a not in df_histroy_keylist)]

    df_offset = df_histroy[df_histroy['标识'].apply(lambda a: a not in df_now_histroy_keylist)]
    df_offset['数量(流向单)'] = df_offset['数量(流向单)'].apply(lambda a : oppositeNumber(float(a)))

    df_append = df_add.append(df_offset)
    df_append['数量(流向单)'] = df_append['数量(流向单)'].astype(float)
    df_new_group = df_append.groupby(['销售月','经销商编码','标准产品名'])['数量(流向单)'].sum().reset_index()
    df_new_group = df_new_group[df_new_group['数量(流向单)'] == 0]

    df_new_group = key(df_new_group, ['销售月', '经销商编码', '标准产品名'], '标识')
    df_new = key(df_append, ['销售月', '经销商编码', '标准产品名'], '标识')


    df_new = df_new[df_new['标识'].apply(lambda a: a not in df_new_group['标识'].tolist())]
    df_new.drop(['标识'], axis=1, inplace=True)
    df_new = df_new[['报告月','销售月','经销商编码','经销商名称','CustomerID','客户名称（流向）','标准客户名称','客户类型','电商平台','产品编码',
                     '标准产品名','商品名称','规格','开单日期','数量(流向单)','折算后的数量','Contract val','Contract price','单位','单价(流向单)',
                     '批号','DDI_ID','BRAND']]


    df_NonullCheck = df_new[['标准产品名','开单日期','客户名称（流向）','客户类型','数量(流向单)']].isnull().any().reset_index()
    df_NonullCheck.rename(columns={'index': '列名', 0: '是否为空'}, inplace=True)

    Writer = pd.ExcelWriter(return_path)
    df_new.to_excel(excel_writer=Writer, sheet_name='结果数据',index=False)
    df_NonullCheck.to_excel(excel_writer=Writer, sheet_name='关键列是否为空',index=False)
    df_add.to_excel(excel_writer=Writer,sheet_name='新增数据',index=False)
    df_offset.to_excel(excel_writer=Writer,sheet_name='红冲数据',index=False)
    df_append.to_excel(excel_writer=Writer,sheet_name='合并数据',index=False)
    Writer.save()




#***************主方法**************
if __name__ == '__main__':
    try:
        contrast()
    except Exception as e:
        logging.info(e)


