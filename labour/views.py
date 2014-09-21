#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from labour.forms import EmployeeProfileForm
from labour.models import EmployeeProfile

# Create your views here.

def index(request, template_name="labour/index.html"):
    """ 管理员登陆页面"""
    user = request.user
    return render(request, template_name, {
        'user': user,
    })

def employee_add(request, form_class=EmployeeProfileForm, template_name='labour/employee_add.html'):
    """ 雇员信息添加"""
    employee = None
    user = request.user

    if request.method == "POST":
        form = form_class(request, data=request.POST)
        if form.is_valid():
            employee = form.save(request)
            messages.info(request, '添加成功', extra_tags='employee_add_succ')
            return HttpResponseRedirect(reverse("labour.views.employee_update", args=(employee.id, )))
    else:
        form = form_class()
    return render(request, template_name, {
        'form': form,
        'user': user,
        'employee': employee,
    })


def employee_update(request, employee_id, form_class=EmployeeProfileForm, template_name="labour/employee_update.html"):
    """ 雇员信息修改"""
    try:
        employee = EmployeeProfile.objects.get(id=employee_id)
    except EmployeeProfile.DoesNotExist:
        messages.error(request, '该雇员不存在', extra_tags='employee_not_exist')
        return HttpResponseRedirect(reverse("labour.views.employee_add"))

    user = request.user

    if request.method == "POST":
        form = form_class(request, data=request.POST, instance=employee)
        if form.is_valid():
            employee = form.save(request)
            messages.info(request, '修改成功', extra_tags='employee_update_succ')
    return render(request, template_name, {
        'user': user,
        'employee': employee,
    })