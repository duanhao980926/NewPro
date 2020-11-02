##
# 邮件自动推送 -- 20191105 created by terrell
# 配置相关变量
# 设置主题、正文等信息
# 添加附件
# 登录、发送#
import pandas as pd
import time
import os
import smtplib
import email
import datetime
import sys
import traceback
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


hour = sys.argv[1]
today = datetime.datetime.now().strftime('%Y%m%d')
config_path = '/邮箱自动推送配置文件.xlsx'
data_file_path = '/入口返回情况与汇总'+today+'.xlsx'
list_aim_file_path = [data_file_path]


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
    list = path.split('/')
    index = list.__len__()
    return list[index-1]


def read_data(data_file_path):
    df = pd.read_excel(data_file_path,sheet_name='汇总')
    return df

def send():

    # 配置变量
    # 读取配置文件
    Values = Read_configfile(config_path)
    # 配置变量
    sender = Values[1]

    receiver = Values[3]
    cc = Values[4]
    subject = today + ' ' + Values[5]
    username = Values[1]
    password = Values[2]

    df = read_data(data_file_path)
    # 邮件主题、正文设置
    massage = MIMEMultipart()
    massage['subject'] = subject
    massage['to'] = receiver
    massage['Cc'] = cc
    massage['from'] = sender
    body = """"""
    for i in range(0,df.shape[0]):

        body1 = """ 
            <tr>
              <td>""" + str(df.at[i,'产线']) + """</td>
              <td>""" + str(df.at[i,'家数']) + """</td>
              <td width="60" align="center">""" + str(df.at[i,'已返回']) + """</td>
              <td width="75">""" + str(df.at[i,'未返回']) + """</td>
              <td width="80">""" + str(df.at[i,'返回占比']) + """</td>
              <td width="80">""" + str(df.at[i,'时间']) + """</td>
            </tr>
            """
        body += body1

    html = """\

        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />


        <body>
        <div>Dear All:</div>
        <div>"""+Values[6]+"""</div>
        <div id="container">
        <p><strong>入口各个产线返回情况统计表:</strong></p>
        <div id="content">
        <table width="70%" border="2" bordercolor="black" cellspacing="0" cellpadding="0">
        <tr>
            <td width="40"><strong>产线</strong></td>
            <td width="50"><strong>家数</strong></td>
            <td width="60" align="center"><strong>已返回</strong></td>
            <td width="50"><strong>未返回</strong></td>
            <td width="80"><strong>返回占比</strong></td>
            <td width="80"><strong>时间</strong></td>
        </tr>""" + body + """
        </table>
        </div>
        </div>
        </div>
        <div>------------------</div>
        <div>Best regards!</div>
        <div>QT Consulting Co.,Ltd</div>
        <div>Add: Room 306 building A. No. 2337, Gu Dai Road, Minhang Distrcit, Shanghai</div>
        <div>Post: 201199</div>
        <div>Email: """+sender+"""</div>
        </body>
        </html>
      """
    massage.attach(MIMEText(html, _subtype='html', _charset='utf-8'))

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
            server.sendmail(sender, receiver.split(',') + cc.split(','), massage.as_string())
            print('邮件发送完成')
        except Exception as e:
            print('报错了...')
            print(e)
            traceback.print_exc()
        else:
            server.quit()

    if int(datetime.datetime.now().strftime('%H')) != int(hour) or datetime.datetime.weekday(
            datetime.datetime.now()) > 4:
        print(datetime.datetime.now().strftime('%H'))
        sys.exit()
    else:
        # pass
        main()


send()