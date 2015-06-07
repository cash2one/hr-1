#!/usr/bin/python
#encoding:utf-8

import datetime

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

def generate_paginator(queryset, page):
    """ 分页"""
    limit = 15  # 每页显示的记录数
    paginator = Paginator(queryset, limit)  # 实例化一个分页对象
    try:
        paged_queryset = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        paged_queryset = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        paged_queryset = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return paged_queryset

def adjacent_paginator(queryset, page, page_num=30, adjacent_pages=2):
    """ 分页"""
    paginator = Paginator(queryset, page_num)
    try:
        paged_queryset = paginator.page(page)
    except PageNotAnInteger:
        paged_queryset = paginator.page(1)
    except EmptyPage:
        paged_queryset = paginator.page(paginator.num_pages)

    start_page = max(paged_queryset.number - adjacent_pages, 1)
    end_page = min(paged_queryset.number + adjacent_pages, paginator.num_pages)

    page_numbers = range(start_page, end_page + 1)
    return paged_queryset, page_numbers

def generate_sn():
    """ 生成序列号"""
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

def generate_info_msg(request, action, **kwargs):
    data = ''
    for key in request.POST.keys():
        if key not in ['password', 'password1', 'csrfmiddlewaretoken']:
            data += '%s=%s ' % (key, request.POST[key])

    for key in kwargs.keys():
        data += '%s=%s ' % (key, kwargs[key])
    return 'userid=%d action=%s %s' % (request.user.id, action, data)