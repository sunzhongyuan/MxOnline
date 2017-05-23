# _*_ coding:utf-8 _*_
__author__ = 'zyzy'
__date__ = '2017/5/22 14:15'

import xadmin

from . import models


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(models.EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(models.Banner, BannerAdmin)