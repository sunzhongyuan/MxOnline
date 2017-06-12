# _*_ coding:utf-8 _*_
"""
Author:     zyzy
Created:    2017/6/12

Description:

"""
from django.conf.urls import url

from .views import OrgView, AddUserAskView

urlpatterns = [
    # 课程机构
    url(r'^list/$', OrgView.as_view(), name='list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
]