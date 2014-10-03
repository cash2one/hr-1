#!/usr/local/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('labour.views',

    url(r'^$', 'index'),

    # 个人信息
    url(r'^employee/add/$', 'employee_add'),
    url(r'^employee/(?P<employee_id>\d+)/update/$', 'employee_update'),
    url(r'^employee/(?P<employee_id>\d+)/show/$', 'employee_show'),
    url(r'^(?P<company_id>\d+)/employees/$', 'company_employees'),
    url(r'^employees/$', 'employees'),
    
    # 公司信息
    url(r'^company/add/$', 'company_add'),
    url(r'^company/(?P<company_id>\d+)/update/$', 'company_update'),
    url(r'^company/(?P<company_id>\d+)/show/$', 'company_show'),
    url(r'^companys/$', 'companys'),

    # 合同信息
    url(r'^employee/(?P<employee_id>\d+)/contract/$', 'contract_add'),
    url(r'^contract/(?P<contract_id>\d+)/update/$', 'contract_update'),

    # 保险信息
    url(r'^employee/(?P<employee_id>\d+)/(?P<insurance>\D+)/$', 'insurance'),

    # 劳务统计
    url(r'^statistics/(?P<statis_type>\D+)/$', 'statistics'),

    # 历史劳务信息
    url(r'^history/$', 'labour_history'),

    # 上传导入职员
    url(r'^import/$', 'labour_import'),

    # 导出职员信息
    url(r'^export/$', 'labour_export'),


)
