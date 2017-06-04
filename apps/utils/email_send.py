# _*_ coding:utf-8 _*_
"""
Author:     zyzy
Created:    2017/6/1

Description:    发送邮件模块

"""
from random import Random
from django.core.mail import send_mail  # 发送邮件函数

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


# 随机产生指定长度的字符串
def random_str(random_length=8):
    result = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        result += chars[random.randint(0, length)]
    return result


# 生成邮件内容并发送
def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)   # 生成一个16位的激活码
    email_record.code = code
    email_record.send_type = send_type
    email_record.email = email
    email_record.save()     # 将激活码保存到数据库 用来验证用户送来的激活码时候合法

    if send_type == 'register':
        email_title = 'zy在线激活链接'
        email_body = '请点击下面链接激活您的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        # 发送邮件 send_mail这个函数需要预先配置用来发送邮件的邮箱 配置在settings.py文件中
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == 'forget':
        email_title = 'zy在线重置密码链接'
        email_body = '请点击下面链接重置您的账号：http://127.0.0.1:8000/reset/{0}'.format(code)

        # 发送邮件 send_mail这个函数需要预先配置用来发送邮件的邮箱 配置在settings.py文件中
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
