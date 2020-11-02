'''
处理RR文件
1遍历目标目录，生成包含rr文件的文件清单
2根据filepath 聚合，合并psi文件到同一文件的不同sheet中，文件命名为：customer_list.xlsx,sheet_name=P/S/I生成合并文件
'''

#*********导包区****************
import pandas as pd
import os
from pathlib import Path

#*********变量区****************
old_path = r'D:/Work/Project/TestData'
new_path =r'D:/Work/Project/NewPro/data'
Inventory_path = Path(old_path)/Path('rr文件清单.xlsx')
filepath_list = []
filename_list = []
psiType_list = []
targetPath_list = []


#将多个DataFrame以多个sheet表的形式写到一张xlsx表中
def write_new_cexel(list_df_path, path):
    writer = pd.ExcelWriter(path)
    len = list_df_path.__len__()
    if len > 0 :
        for df_path in list_df_path:
            df = pd.read_excel(df_path)
            df.to_excel(writer, sheet_name=Path(df_path).parts[-1][7:8],index=None)
        writer.save()
    else:
        return


#生成包含rr文件的文件清单
def CreateInventoryAndMergeFiles():
    for file_Name in os.listdir(old_path):
        if os.path.isdir(os.path.join(old_path,file_Name)) :
            file_D = os.path.join(old_path, file_Name)
        else:
            continue
        list_df_path = []
        for file_name in os.listdir(file_D):
            if Path(file_name).match('rename*.rr'):
                #清单数据
                filepath_list.append(file_D)
                filename_list.append(file_name)
                psiType_list.append(file_name[7:8])
                targetPath_list.append(Path(new_path) / Path(file_D).parts[-1])

                #获取同一经销商下所有的RR文件路径
                oldSrc = os.path.join(file_D,file_name)
                list_df_path.append(oldSrc)
        # 合并psi文件到同一文件的不同sheet中，文件命名为：customer_list.xlsx,sheet_name=P/S/I生成合并文件
        write_new_cexel(list_df_path,Path(file_D)/Path(file_D+'.xlsx').parts[-1])
    #添加数据，并生成清单
    data = {'filepath':filepath_list,'filename':filename_list,'psiType':psiType_list,'targetPath':targetPath_list}
    df_Inventory = pd.DataFrame(data)
    df_Inventory.to_excel(Inventory_path,index=None)

CreateInventoryAndMergeFiles()
