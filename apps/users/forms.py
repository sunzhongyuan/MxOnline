# _*_ coding:utf-8 _*_
__author__ = 'zyzy'
__date__ = '2017/5/31 15:06'
from django import forms

from captcha.fields import CaptchaField


'''用来存储form定义的文件'''


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ModifyPwdForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    password1 = forms.CharField(required=True, min_length=5)
