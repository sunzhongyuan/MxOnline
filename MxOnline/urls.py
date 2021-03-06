# _*_ coding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.views.static import serve
# from django.contrib import admin
from django.views.generic import TemplateView   # 处理静态页面转换为view

import xadmin

from users.views import LoginView, RegisterView, ActiveView, ForgetView, ResetView, ModifyPwdView
from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 将静态文件转换为view 不用自己写view函数
    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetView.as_view(), name='forget'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),



    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),

    # 导入org的urls文件
    url(r'^org/', include('organization.urls', namespace='org')),

    # 导入course的urls文件
    url(r'^course/', include('courses.urls', namespace='course')),
]
