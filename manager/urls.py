#!/usr/local/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('manager.views',
    # 后台管理员
    url(r'^index/$', 'index'),
    url(r'^add/$', 'add'),
    url(r'^update/$', 'update'),
    url(r'^login_log/$', 'login_log'),
    url(r'^user_action/$', 'user_action'),
    url(r'^send_email/$', 'send_email'),

    # 人员审核
    url(r'^audit/$', 'employee_audit'),

)