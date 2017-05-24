# _*_ coding:utf-8 _*_
__author__ = 'zyzy'
__date__ = '2017/5/22 14:15'

import xadmin
from xadmin import views

from . import models


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


class BaseSetting(object):
    enable_themes = True    # 是否支持主题
    use_bootswatch = True   # 可选择的主题


class GlobalSettings(object):
    site_title = '后台管理系统'   # 左上角的名称
    site_footer = 'oo'              # 底部的公司名称
    menu_style = 'accordion'    # 将app折叠起来

# 注册
xadmin.site.register(models.EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(models.Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)