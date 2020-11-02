## created by terrell on 2020-08-30
# lts file union by python
# aimed to integration lts data in one file
# step1 find all conform rules file create file list
# step2 read file one by one
# step3 concat file one by one
# step4 create union file
# #
import os
import sys
import time
import re
from datetime import datetime, timedelta
from pathlib import Path, PurePath
from fuzzywuzzy import process
import logging
import pandas as pd
from openpyxl import load_workbook

hour = sys.argv[1]
# 控制运行时机 每日5点到9点上传
now = time.strftime("%H")
if (0 <= int(now) < 6) or (int(hour) <= int(now) <= 23):
    print('时机不对， 我先走了')
    sys.exit()
else:
    # time.sleep(300)
    pass

# param definition
today = datetime.now().strftime('%Y%m%d')
yesterday = datetime.now() - timedelta(1)
startI = yesterday.strftime('%Y%m%d')
startS = (datetime.now() - timedelta(90)).strftime('%Y%m%d')
startP = (datetime.now() - timedelta(60)).strftime('%Y%m%d')
file_path = '/ftp/gk/lts/daily'
compareFilePath = Path("./Z_product_list.xlsx")
blackFilePath = Path("./Z_black_list.xlsx")
s_aim_file_path = file_path + '/LTS-销售日采集-' + today + '.csv'
p_aim_file_path = file_path + '/LTS-采购日采集-' + today + '.csv'
i_aim_file_path = file_path + '/LTS-库存日采集-' + today + '.csv'
lv_aim_file_path = file_path + '/LTS-进销存采集填充率-' + today + '.xlsx'
s_rules = '_S_' + today
p_rules = '_P_' + today
i_rules = '_I_' + today
s_essential_column = ['deliveryNoteNumber', 'controlDate', 'code', 'dealerName', 'customerCode', 'customerName',
                      'productCode', 'productName', 'productGeneralName', 'productSpec', 'unit', 'manufacture',
                      'productLot', 'approvedID', 'qty', 'price', 'amount', 'expdate', 'subsidiaryMark']
p_essential_column = ['importID', 'supplierName', 'controlDate', 'code', 'dealerName', 'productCode', 'productName',
                      'productGeneralName', 'productSpec', 'unit', 'productOrigin', 'productLot', 'approvedID', 'qty',
                      'price', 'amount', 'expdate', 'subsidiaryMark']
i_essential_column = ['controlDate', 'code', 'dealerName', 'manufacture', 'productCode', 'productName',
                      'productGeneralName', 'productSpec', 'unit', 'approvedID', 'productLot', 'qty', 'price', 'amount',
                      'expirationDate', 'subsidiaryMark']
p_rename_column = {'importID': '客户进货单号', 'supplierName': '供应商', 'controlDate': '购入日期', 'code': '经销商代码',
                   'dealerName': '经销商名称', 'productCode': '产品编号', 'productName': '产品名称', 'productGeneralName': '产品通用名',
                   'productSpec': '产品规格', 'unit': '计量单位', 'productOrigin': '生产企业', 'productLot': '批号',
                   'approvedID': '批准文号', 'qty': '采购数量', 'price': '采购单价', 'amount': '采购金额', 'expdate': '效期',
                   'subsidiaryMark': '分子公司名称'
                   }

s_rename_column = {'deliveryNoteNumber': '客户流向单号', 'controlDate': '销售日期', 'code': '经销商代码', 'dealerName': '经销商名称',
                   'customerCode': '购入客户代码', 'customerName': '购入客户名称', 'productCode': '产品编号', 'productName': '产品名称',
                   'productGeneralName': '产品通用名', 'productSpec': '产品规格', 'unit': '计量单位', 'manufacture': '生产企业',
                   'productLot': '批号', 'approvedID': '批准文号', 'qty': '销售数量', 'price': '销售单价', 'amount': '销售金额',
                   'expdate': '效期', 'subsidiaryMark': '分子公司名称'
                   }

i_rename_column = {'controlDate': '统计日期', 'code': '经销商代码', 'dealerName': '经销商名称', 'manufacture': '生产企业',
                   'productCode': '产品编号', 'productName': '产品名称', 'productGeneralName': '产品通用名', 'productSpec': '产品规格',
                   'unit': '计量单位', 'approvedID': '批准文号', 'productLot': '批号', 'qty': '数量', 'price': '单价', 'amount': '金额',
                   'expirationDate': '效期', 'subsidiaryMark': '分子公司名称'
                   }

P_filling_columns = ['供应商','购入日期','经销商代码','经销商名称','产品名称','产品规格','计量单位','生产企业','批号','采购数量','采购单价']
S_filling_columns = ['销售日期','经销商代码','经销商名称','购入客户名称','产品名称','产品规格','计量单位','生产企业','批号','销售数量','销售单价']
I_filling_columns = ['统计日期','经销商代码','经销商名称','生产企业','产品名称','产品规格','计量单位','批号','数量','效期']

logger = logging.getLogger()
handler1 = logging.StreamHandler()
handler2 = logging.FileHandler('/ftp/logs/' + sys.argv[0].split('.')[0] + '_' + today + '.log', mode='a')
logger.setLevel(logging.DEBUG)
handler1.setLevel(logging.ERROR)
handler2.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(name)s:%(levelname)s:%(message)s")
handler1.setFormatter(formatter)
handler2.setFormatter(formatter)
logger.addHandler(handler1)
logger.addHandler(handler2)


# step1 find file which conform rules
# need folder and rules
# return file_list
def find_file(path, rules):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:
            image_name = os.path.join(dirpath, filepath)  # 获取文件的全路径
            # image_name = filepath
            str1 = re.compile(rules + '''(.*?).xls''')
            match_obj = re.findall(str1, image_name)
            if match_obj:
                # print(image_name)
                file_list.append(image_name)
    print(file_list)
    return file_list


# step2 read file only need essential column
# need filename essential_column
# return file dataframe
def read_file(fn, ec):
    flag = 'OK'
    try:
        fileDF = pd.read_excel(fn, usecols=ec)
        # print(str(fn).split('\\')[-1][0:8], fileDF.shape[0])
        print(fileDF.columns)
    except Exception as e:
        fileDF = pd.DataFrame()
        logger.error('%s, read file failed, reason is %s', fn, str(e))
        flag = 'ERR'
    return fileDF, flag


# step3 concat file
# need all dataframe and new dataframe
# return concat dataframe
def concat_file(fn, origin, new):
    flag = 'OK'
    try:
        concatDF = origin.append(new)
    except Exception as e:
        print(e)
        flag = 'ERR'
        logger.error('%s, concat file failed, reason is %s', fn, str(e))
        return origin, flag
    return concatDF, flag


# step3-1 product filter
# need concatDF product_list product_black_list or path
# return filtered dataframe
def product_filter(cd, pp, pbp):
    # 产品过滤 -- 根据产品名称进行过滤，不包含产品规格的原因为，当不同产品的产品规格想同你时，导致fuzzy计算的分数偏高，产生噪声明显
    try:
        compare_df = pd.read_excel(pp)
        compare_list1 = list(set(compare_df['产品标准名称'].tolist()))
        compare_list2 = list(set(compare_df['产品化学名'].dropna().tolist()))
        black_df = pd.read_excel(pbp)
        black_list = black_df['productName'].tolist()
        product_list = cd['productName'].astype(str).tolist()
        filtered_set = set()
        for i in product_list:
            result1 = process.extract(i, compare_list1)
            result2 = process.extract(i, compare_list2)
            if result1[0][1] >= 70 or result2[0][1] >= 70:
                filtered_set.add(i)

        def judge(x):
            if x in list(filtered_set):
                return True
            return False

        def black_filter(x):
            if x in black_list:
                return False
            return True

        productDF = cd[cd['productName'].apply(judge)]
        productDF = productDF[productDF['productName'].apply(black_filter)]
    except Exception as e:
        productDF = cd
        logger.error('产品过滤异常 ------- %s', str(e))
    return productDF


# 时间过滤
def date_filter(sdf, start):
    try:
        sdf = sdf[sdf['controlDate'] >= int(start)]
    except Exception as e:
        logger.error(str(e))
    return sdf


# 生成进销存采购的填充率
def filling_rate(type_columns, aimpath):
    df_init = pd.read_csv(aimpath)
    df_init.fillna('nan', inplace=True)
    to_count = df_init.shape[0]
    list = []
    print(type_columns)
    for itmes in type_columns:
        filling_count = df_init.loc[df_init[itmes].apply(lambda a: str(a) != 'nan')].shape[0]
        if filling_count != 0:
            lv_filina = filling_count / to_count
            list.append('{:.0%}'.format(lv_filina))
        else:
            list.append('0')
    data = {'关键列': type_columns, '填充率': list}
    df = pd.DataFrame(data=data)
    return df

# step4 create file
# need file_path dataframe
# return create flag
def create_file(fp, df):
    try:
        df.to_csv(fp, index=False, encoding='utf-8')
    except Exception as e:
        logger.error('%s, create file failed, reason is %s', fp, str(e))


# main def
def process_file(rule, essenclo, aimpath, start, renameclo):
    st = datetime.now()
    originDF = pd.DataFrame()
    okNum = 0
    file_list = find_file(file_path, rule)
    if len(file_list) < 1:
        logger.error('pending process file is null')
        print('pending process file is null')
        return
    for filename in file_list:
        readDF, flag = read_file(filename, essenclo)
        if flag == 'ERR':
            continue
        originDF, flag = concat_file(filename, originDF, readDF)
        if flag == 'ERR':
            continue
        okNum += 1
    logger.info('all file is: %s, append ok file is: %s', len(file_list), okNum)
    # productDF = product_filter(originDF, compareFilePath, blackFilePath)
    # productDF = productDF[essenclo]
    productDF = originDF[essenclo]
    dateDF = date_filter(productDF, start)
    dateDF.rename(columns=renameclo, inplace=True)
    create_file(aimpath, dateDF)
    en = datetime.now()
    print(sys.argv[0].split('.')[0], en - st)

def filling_rate_table():
    writer = pd.ExcelWriter(lv_aim_file_path)
    filling_rate(P_filling_columns, p_aim_file_path).to_excel(writer, sheet_name='采购',index=None)
    filling_rate(S_filling_columns, s_aim_file_path).to_excel(writer, sheet_name='销售',index=None)
    filling_rate(I_filling_columns, i_aim_file_path).to_excel(writer, sheet_name='库存',index=None)
    writer.save()

process_file(s_rules, s_essential_column, s_aim_file_path, startS, s_rename_column)
process_file(p_rules, p_essential_column, p_aim_file_path, startP, p_rename_column)
process_file(i_rules, i_essential_column, i_aim_file_path, startI, i_rename_column)
filling_rate_table()
print(datetime.now())