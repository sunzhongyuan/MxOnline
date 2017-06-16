# _*_ coding:utf-8 _*_
"""
Author:     zyzy
Created:    2017/6/16

Description:

"""
from django.conf.urls import url

from .views import CourseView, CourseDescView

urlpatterns = [
    # 公开课
    url(r'^list/$', CourseView.as_view(), name='list'),
    url(r'^desc/(?P<course_id>\d+)/$', CourseDescView.as_view(), name='desc'),

]