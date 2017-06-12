# _*_ coding:utf-8 _*_
"""
Author:     zyzy
Created:    2017/6/12

Description:

"""
from django import forms
import re

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):     # ModelForm  与form相比不仅可以验证 还可以直接提交（调用model的save()方法）
    # 还可以添加model之外的字段
    # my_filed = forms.CharField()

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 默认验证方式是根据model的定义进行验证 还可以自定义验证方式 固定格式如下
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号非法', code='mobile_invalid')
