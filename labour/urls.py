#!/usr/local/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('labour.views',

    url(r'^$', 'index'),

    #个人信息
    url(r'^employee/add/$', 'employee_add'),
    url(r'^employee/(?P<employee_id>\d+)/update/$', 'employee_update'),
    url(r'^employee/(?P<employee_id>\d+)/contract/$', 'contract'),

    #公司信息
    url(r'^company/add/$', 'company_add'),
    url(r'^company/(?P<company_id>\d+)/update/$', 'company_update'),

)
