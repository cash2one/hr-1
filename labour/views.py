#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render

from labour.forms import EmployeeProfileForm

# Create your views here.

def index(request, template_name="labour/index.html"):
    """ 管理员登陆页面"""
    user = request.user
    return render(request, template_name, {
        'user': user,
    })

def personal(request, form_class=EmployeeProfileForm, template_name='labour/personal_add.html'):
    """ 个人信息添加"""
    if request.method == "post":
        pass
    else:
        form = form_class()
    return render(request, template_name, {
        'form': form,
    })