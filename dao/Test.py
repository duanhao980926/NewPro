import pandas as pd

def read_excel2(path):
  data_xls = pd.io.excel.ExcelFile(path)
  data={}
#   print(data_xls.sheet_names)
#   for name in data_xls.sheet_names:
#     df=pd.read_excel(data_xls,sheetname=name,header=None)
#     data[name]=df
#   return data
#
# a = read_excel2('C:/Users/xiaofei.yu/Desktop/测试数据/HH/瀚晖申诉流向/工作簿7.xlsx')
# print(a)

# data_xls = pd.io.excel.ExcelFile('C:/Users/xiaofei.yu/Desktop/测试数据/HH/瀚晖申诉流向/工作簿7.xlsx')
# print(type(data_xls))

data = {'省':['ddd']}

print(data['省'])

