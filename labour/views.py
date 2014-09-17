#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

def login(request, tempalte_name='login.html'):
    """ 登录"""
    return render(request, tempalte_name, {})