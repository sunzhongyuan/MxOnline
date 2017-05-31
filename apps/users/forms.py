# _*_ coding:utf-8 _*_
__author__ = 'zyzy'
__date__ = '2017/5/31 15:06'
from django import forms


'''用来存储form定义的文件'''


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
