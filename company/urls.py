#!/usr/local/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('company.views',
    # 企业资金管理
    url(r'^property/$', 'property'),
    url(r'^insurance/$', 'insurance'),
    url(r'^property/detail/$', 'property_detail'),
    url(r'^salary/$', 'salary'),
)