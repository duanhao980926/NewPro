import pandas as pd
from openpyxl import load_workbook
from pathlib import Path

i = 0

# 将多个sheet表写到同一张已存在的xlsx表
def write_excel(dataframe, path, sheetname):
    """
    数据写入到Excel,可以写入不同的sheet
    """
    excelWriter = pd.ExcelWriter(path, engine='openpyxl')
    excelWriter.book = load_workbook(excelWriter.path)
    dataframe.to_excel(excel_writer=excelWriter, sheet_name=sheetname, index=None)
    excelWriter.close()
