#!/usr/bin/python
# -*- coding: UTF-8 -*-


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib

sender = 'from@runoob.com'
receivers = ['429240967@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')  # 发送者
message['To'] = Header("测试", 'utf-8')  # 接收者

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')


def addimg(src, imgid):  # 定义图片读取函数，参数1为图片路径，2为图片ID机标识符
    with open(src, 'rb') as f:
        msgimage = MIMEImage(f.read())  # 读取图片内容
    msgimage.add_header('Content-ID', imgid)  # 指定文件的Content-ID,<img>,在HTML中图片src将用到
    return msgimage


android_version = "2.119"
android_url = "////////"
msgtext = MIMEText("""
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<table width="600" border="1" cellspacing="0" cellpadding="4">
    <tr bgcolor="#CECFAD" height="20">
        <td colspan=2>测试邮件地址<a href="monitor.domain.com">更多>></a></td>
    </tr>
    <tr bgcolor="#EFEBDE" height="20">
        <td>
            <a>Android版本更新信息</a>
        </td>
        <td>
            <a>ROS版本更新信息</a>
        </td>
    </tr>
    <tr bgcolor="#EFEBDE" height="20">
        <td>
            <a>Android版本:""" + android_version + """</a>
            <br/>
            <a>下载地址:""" + android_url + """</a>
        </td>
        <td>
            <a>ROS版本更新信息</a>
        </td>
    </tr>
    <tr bgcolor="#EFEBDE" height="100">
    </tr>
</table>
</body>
</html>""", "html", "utf-8")

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.ehlo()
    server.login('469282670@qq.com', '628543985DD')
    message = MIMEMultipart()
    # 将正文以text的形式插入邮件中
    message.attach(MIMEText("hello", 'plain', 'utf-8'))
    message.attach(msgtext)
    # 生成发件人名称（这个跟发送的邮件没有关系）
    message['From'] = Header("dandan", 'utf-8')
    # 生成收件人名称（这个跟接收的邮件也没有关系）
    message['To'] = Header("good", 'utf-8')
    # 生成邮件主题
    message['Subject'] = Header("subject", 'utf-8')
    server.sendmail('469282670@qq.com', 'cqdanlili@126.com', message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print("Error: 无法发送邮件" + e)
