##
# 邮件自动推送 -- 20191105 created by terrell
# 配置相关变量
# 设置主题、正文等信息
# 添加附件
# 登录、发送#
import pandas as pd
import smtplib
import datetime
from pathlib import Path
import traceback
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


today = datetime.datetime.now().strftime('%Y%m%d')
list_aim_file_path = []
file_path = './'
config_path = file_path+'/邮箱自动推送配置文件.xlsx'
accessory_path = file_path+'/附件'
for fileName in os.listdir(accessory_path):
    file = os.path.join(accessory_path,fileName)
    list_aim_file_path.append(file)


#取到对应的邮箱SMTP服务
def SMTPserver(MailName):
    if MailName == '腾讯邮箱':
        return 'smtp.exmail.qq.com'
    elif MailName == '阿里邮箱':
        return 'smtp.qiye.aliyun.com'

# 读取配置文件
def Read_configfile(TFP_path):
    df = pd.read_excel(TFP_path)
    Valus = []
    for i in range(0,df.shape[0]) :
        if ('文件路径' in df.at[i,'参数']) | ('附件' in df.at[i,'参数']) :
            df.at[i, '值'] = df.at[i,'值'].split(',')
        Valus.append(df.at[i,'值'])
    return Valus

#在全路径中拿取文件名
def file_name(path):
    return Path(path).parts[-1]

def send():
    #读取配置文件
    Values = Read_configfile(config_path)
    # 配置变量
    sender = Values[1]

    receiver = Values[3]
    cc = Values[4]
    subject =Values[5]
    username = Values[1]
    password = Values[2]

    # 邮件主题、正文设置
    massage = MIMEMultipart()
    massage['subject'] = subject
    massage['to'] = receiver
    if str(cc) != 'nan':
        massage['Cc'] = cc
    massage['from'] = sender
    body = 'Dear all,\r\n\r\n'+Values[6]+ \
                     '\r\n\r\n\r\n\r\n\r\nQT Consulting Co.,Ltd' \
                     '\r\nAdd: Room 306 building A. No. 2337, Gu Dai Road, Minhang Distrcit, Shanghai' \
                     '\r\nPost: 201199' \
                     '\r\nEmail: '+sender

    massage.attach(MIMEText(body, _subtype='plain', _charset='utf-8'))
    # 添加附件
    list_file = list_aim_file_path
    for file in list_file:
        filename = file_name(file)
        appendix = MIMEApplication(open(file, 'rb').read())
        appendix.add_header('content-disposition', 'attachment', filename=filename)
        massage.attach(appendix)

    def main():
        # time.sleep(300)
        try:
            # 发送邮箱服务器
            smtp_server = SMTPserver(Values[0])
            # smtp_server = 'smtp.163.com'
            server = smtplib.SMTP_SSL(smtp_server, 465)
            server.set_debuglevel(1)
            server.login(username, password)
            print('登录成功')
            if str(cc) != 'nan':
                server.sendmail(sender, receiver.split(',') + cc.split(','), massage.as_string())
                print(receiver.split(',') + cc.split(','))
            else:
                server.sendmail(sender, receiver.split(','), massage.as_string())
                print(receiver.split(','))
            print('邮件发送完成')
        except Exception as e:
            print('报错了...')
            print(e)
            traceback.print_exc()
        else:
            server.quit()


    main()


send()

