#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

def index(request, template_name="labour/index.html"):
    """ 管理员登陆页面"""
    user = request.user
    return render(request, template_name, {
        'user': user,
    })