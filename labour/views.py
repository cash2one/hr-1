#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from labour.forms import EmployeeProfileForm, ContractForm, CompanyForm
from labour.models import EmployeeProfile, UserProfile, CompanyProfile, Contract
from labour.forms import HealthForm, BornForm, UnemployeedForm, ReservedForm, IndustrialForm, EndowmentForm
from utils import adjacent_paginator


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
    else:
        form = form_class(request, instance=employee)

    return render(request, template_name, {
        'user': user,
        'employee': employee,
        'form': form,
    })

def contract_add(request, employee_id, form_class=ContractForm, template_name="labour/employee_contract_add.html"):
    """ 员工公司合同信息"""
    try:
        employee = EmployeeProfile.objects.get(id=employee_id)
        if Contract.objects.filter(employee=employee, is_deleted=0).exists():
            contract = Contract.objects.get(employee=employee, is_deleted=0)
            #for contract in employee.contract:
                #c = contract
            return HttpResponseRedirect(reverse('labour.views.contract_update', args=(contract.id,)))
    except EmployeeProfile.DoesNotExist:
        messages.error(request, '该雇员不存在', extra_tags='employee_not_exist')
        return HttpResponseRedirect(reverse("labour.views.employee_add"))

    user = request.user
    companys = CompanyProfile.objects.all()

    if request.method == "POST":
        form = form_class(request, data=request.POST)
        if form.is_valid():
            c = form.save(request, employee)
            messages.info(request, '添加成功', extra_tags='contract_add_succ')
            return HttpResponseRedirect(reverse("labour.views.contract_update", args=(c.id, )))
    else:
        form = form_class()
    return render(request, template_name, {
        'user': user,
        'form': form,
        'companys': companys,
        'employee': employee,
    })

def contract_update(request, contract_id, form_class=ContractForm, template_name='labour/employee_contract_update.html'):
    """ 合同信息修改"""
    try:
        contract = Contract.objects.get(id=contract_id)
    except Contract.DoesNotExist:
        messages.error(request, '该合同不存在', extra_tags='contract_not_exist')
        return HttpResponseRedirect(reverse("labour.views.employee_add"))

    if request.method == "POST":
        form = form_class(request, data=request.POST, instance=contract)
        if form.is_valid():
            form.save(commit=True)
            messages.info(request, '修改成功', extra_tags='contract_update_succ')
    else:
        form = form_class(instance=contract)
    return render(request, template_name, {
        'form': form,
        'company': contract.employee.company,
        'employee': contract.employee,
    })

def company_add(request, form_class=CompanyForm, template_name='labour/company_add.html'):
    """ 公司信息添加"""
    if request.method == "POST":
        form = form_class(request, data=request.POST)
        if form.is_valid():
            company = form.save(request)
            messages.info(request, '添加成功', extra_tags='company_add_succ')
            return HttpResponseRedirect(reverse("labour.views.company_update", args=(company.id, )))
    else:
        form = form_class()
    return render(request, template_name, {
        'form': form,
    })

def company_update(request, company_id, form_class=CompanyForm, template_name='labour/company_update.html'):
    """ 公司信息修改"""
    try:
        company = CompanyProfile.objects.get(id=company_id)
    except CompanyProfile.DoesNotExist:
        messages.error(request, '该公司不存在', extra_tags='company_not_exist')
        return HttpResponseRedirect(reverse("labour.views.company_add"))

    if request.method == "POST":
        form = form_class(request, data=request.POST, instance=company)
        if form.is_valid():
            form.save(request)
            messages.info(request, '修改成功', extra_tags='company_update_succ')
    else:
        form = form_class(instance=company)
    return render(request, template_name, {
        'form': form,
    })

def companys(request, template_name='labour/companys.html'):
    """ 全部公司信息"""
    search = request.GET.get('search', None)
    if search is not None:
        company_list = CompanyProfile.objects.filter(name__contains=search)
    else:
        company_list = CompanyProfile.objects.filter(is_deleted=0)

    companys, page_numbers = adjacent_paginator(company_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'companys': companys,
        'page_numbers': page_numbers,
    })

def employees(request, template_name='labour/employees.html'):
    """ 全部员工信息"""
    name = request.GET.get('name', None)
    id_no = request.GET.get('id_no', None)
    return render(request, template_name, {

    })

def insurance(request, employee_id, insurance):
    """ 保险信息分流"""
    if insurance == 'health':
        # 养老保险
        return base_insurance(request, employee_id, HealthForm, 'labour/health_insurance.html')
    elif insurance == 'endowment':
        # 医疗保险
        return base_insurance(request, employee_id, EndowmentForm, 'labour/endowment_insurance.html')

    elif insurance == 'born':
        # 生育保险
        return base_insurance(request, employee_id, BornForm, 'labour/born_insurance.html')

    elif insurance == 'industrial':
        # 工伤保险
        return base_insurance(request, employee_id, IndustrialForm, 'labour/industrial_insurance.html')

    elif insurance == 'unemployeed':
        # 失业保险
        return base_insurance(request, employee_id, UnemployeedForm, 'labour/unemployeed_insurance.html')

    elif insurance == 'reserved':
        # 住房公积金
        return base_insurance(request, employee_id, ReservedForm, 'labour/reserved_insurance.html')


def base_insurance(request, employee_id, form_class, template_name):
    """ 保险信息"""
    try:
        employee = EmployeeProfile.objects.get(id=employee_id)
    except EmployeeProfile.DoesNotExist:
        employee = None

    if request.method == "POST":
        form = form_class(request, data=request.POST, instance=employee)
        if form.is_valid():
            form.save(request)
    else:
        form = form_class()
    return render(request, template_name, {
        'form': form,
        'user': request.user,
        'employee': employee,
    })












