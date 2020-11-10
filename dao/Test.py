#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.messagebox import *
import time
from tkinter.filedialog import askdirectory

LOG_LINE_NUM = 0
init_window = Tk()

def selectPath():
  path_ = askdirectory()
  path.set(path_)


def selectPath1():
  path_ = askdirectory()
  path1.set(path_)



path = StringVar()
path1 = StringVar()

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("标准化小程序")           #窗口名
        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('400x100+10+10')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高

        # 标签
        self.init_data_Label = Label(self.init_window_name, text="目标路径:").grid(row=0, column=0)
        #输入文本器
        self.init_data_Entry = Entry(self.init_window_name, textvariable=path,width=38)
        self.init_data_Entry.grid(row=0, column=1)
        #选择文件路径按钮
        self.init_data_Button = Button(self.init_window_name, text="路径选择", command=selectPath).grid(row=0, column=2)

        self.result_data_Label = Label(self.init_window_name, text="存放路径:").grid(row=1, column=0)
        self.result_data_Entry = Entry(self.init_window_name, textvariable=path1,width=38)
        self.result_data_Entry.grid(row=1, column=1)
        self.result_data_Button = Button(self.init_window_name, text="路径选择", command=selectPath1).grid(row=1, column=2)

        #执行按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="点击执行", bg="lightblue", width=10,command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=2, column=1)


    #功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Entry.get()
        print(src)
        cun_src = self.result_data_Entry.get()
        print(cun_src)
        showinfo('提示', '好吃的都给你')


    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

if __name__ == '__main__':
    gui_start()