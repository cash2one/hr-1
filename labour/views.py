#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import xlwt
import xlrd

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from labour.forms import EmployeeProfileForm, ContractForm, CompanyForm
from labour.models import EmployeeProfile, UserProfile, CompanyProfile, Contract
from labour.forms import HealthForm, BornForm, UnemployeedForm, ReservedForm
from labour.forms import LabourImportForm, IndustrialForm, EndowmentForm
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

def company_show(request, company_id, template_name='labour/company_show.html'):
    """ 公司信息show"""
    try:
        company = CompanyProfile.objects.get(id=company_id)
    except CompanyProfile.DoesNotExist:
        messages.error(request, '该公司不存在', extra_tags='company_not_exist')
        return HttpResponseRedirect(reverse("labour.views.company_add"))

    return render(request, template_name, {
        'company': company,
        'user': request.user,
    })

def employee_show(request, employee_id, template_name='labour/employee_show.html'):
    """ 员工信息show"""
    try:
        employee = EmployeeProfile.objects.get(id=employee_id)
    except EmployeeProfile.DoesNotExist:
        messages.error(request, '该雇员不存在', extra_tags='employee_not_exist')
        return HttpResponseRedirect(reverse("labour.views.employee_add"))

    return render(request, template_name, {
        'user': request.user,
        'employee': employee,
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
    health_card = request.GET.get('health_card', None)
    search = request.GET.get('search', None)
    search_dict = {}

    if search is not None:
        if name != '':
            search_dict['name__contains'] = name
        if id_no != '':
            search_dict['id_no__contains'] = id_no
        if health_card != '':
            search_dict['health_card__contains'] = health_card

        employee_list = EmployeeProfile.objects.filter(**search_dict)
    else:
        employee_list = EmployeeProfile.objects.all()


    employees, page_numbers = adjacent_paginator(employee_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'employees': employees,
        'user': request.user,
        'name': name,
        'id_no': id_no,
        'health_card': health_card,
    })

def company_employees(request, company_id, template_name='labour/company_employees.html'):
    """ 全部员工信息"""
    try:
        company = CompanyProfile.objects.get(id=company_id)
    except CompanyProfile.DoesNotExist:
        messages.error(request, '该公司不存在', extra_tags='company_not_exist')
        return HttpResponseRedirect(reverse("labour.views.company_add"))

    employee_list = EmployeeProfile.objects.filter(company=company)

    employees, page_numbers = adjacent_paginator(employee_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'employees': employees,
        'user': request.user,
        'company': company,
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
            if employee is None:
                messages.info(request, '添加成功', extra_tags='add_succ')
            else:
                messages.info(request, '修改成功', extra_tags='update_succ')
    else:
        form = form_class(instance=employee)
    return render(request, template_name, {
        'form': form,
        'user': request.user,
        'employee': employee,
    })

def statistics(request, statis_type='all', template_name='labour/labour_statistics.html'):
    """ 劳务信息统计"""
    today = datetime.datetime.now()

    if statis_type == 'all':
        endowment_count = EmployeeProfile.objects.filter(endowment_payment_end__lt=today).count()
        health_count = EmployeeProfile.objects.filter(health_payment_end__lt=today).count()
        born_count = EmployeeProfile.objects.filter(born_payment_end__lt=today).count()
        industrial_count = EmployeeProfile.objects.filter(industrial_payment_end__lt=today).count()
        unemployed_count = EmployeeProfile.objects.filter(unemployed_payment_end__lt=today).count()
        reserved_count = EmployeeProfile.objects.filter(reserved_payment_end__lt=today).count()
        company_protocal_count = Contract.objects.filter(company_protocal_end__lt=today).count()
        labour_contract_count = Contract.objects.filter(labour_contract_end__lt=today).count()
        probation_count = Contract.objects.filter(probation_end__lt=today).count()

        return render(request, template_name, {
            'endowment_count': endowment_count,
            'health_count': health_count,
            'born_count': born_count,
            'industrial_count': industrial_count,
            'unemployed_count': unemployed_count,
            'reserved_count': reserved_count,
            'company_protocal_count': company_protocal_count,
            'labour_contract_count': labour_contract_count,
            'probation_count': probation_count,
        })
    elif statis_type == 'endowment':
        profiles = EmployeeProfile.objects.filter(endowment_payment_end__lt=today)
    elif statis_type == 'health':
        profiles = EmployeeProfile.objects.filter(health_payment_end__lt=today)
    elif statis_type == 'born':
        profiles = EmployeeProfile.objects.filter(born_payment_end__lt=today)
    elif statis_type == 'industrial':
        profiles = EmployeeProfile.objects.filter(industrial_payment_end__lt=today)
    elif statis_type == 'unemployeed':
        profiles = EmployeeProfile.objects.filter(unemployed_payment_end__lt=today)
    elif statis_type == 'reserved':
        profiles = EmployeeProfile.objects.filter(reserved_payment_end__lt=today)
    elif statis_type == 'company_protocal':
        profiles = Contract.objects.filter(company_protocal_end__lt=today)
    elif statis_type == 'labour_contract':
        profiles = Contract.objects.filter(labour_contract_end__lt=today)
    elif statis_type == 'probation':
        profiles = Contract.objects.filter(probation_end__lt=today)
    else:
        return HttpResponseRedirect(reverse('labour.views.statistics'))

    template_name = 'labour/labour_statistics_detail.html'

    employees, page_numbers = adjacent_paginator(profiles, request.GET.get('page', 1))
    
    return render(request, template_name, {
        'employees': employees,
    })

def labour_history(request, template_name='labour/labour_history.html'):
    """ 历史劳务信息"""
    employee_list = EmployeeProfile.objects.filter(is_fired=True)
    companys = CompanyProfile.objects.all()

    name = request.GET.get('name', None)
    id_no = request.GET.get('id_no', None)
    company_id = request.GET.get('company_id', None)
    search = request.GET.get('search', None)
    search_dict = {}

    if search is not None:
        if name != '':
            search_dict['name__contains'] = name
        if id_no != '':
            search_dict['id_no__contains'] = id_no
        if company_id != '0':
            search_dict['company_id'] = company_id

        employee_list = EmployeeProfile.objects.filter(is_fired=True, **search_dict)
    else:
        employee_list = EmployeeProfile.objects.filter(is_fired=True)


    employees, page_numbers = adjacent_paginator(employee_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'employees': employees,
        'page_numbers': page_numbers,
        'companys': companys,
        'name': name,
        'id_no': id_no,
        'company_id': company_id,
    })

def labour_import(request, form_class=LabourImportForm, template_name='labour/labour_import.html'):
    """ excel导入"""
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['labour_import']
            data = xlrd.open_workbook(file_contents=input_excel.read())
            table = data.sheets()[0]
            nrows = table.nrows
            for i in range(1, nrows):
                print table.row_values(i)
    else:
        form = form_class()

    return render(request, template_name, {
        'form': form,
    })


def labour_export(request):
    """ excel导出"""

    export_type = request.GET.get('export_type', None)
    company_id = request.GET.get('company_id', None)

    book = xlwt.Workbook(encoding='utf-8')
    ws = book.add_sheet('导出职员信息')
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'SimSun'
    style.font = font
    ws.write(0, 0, "姓名", style)
    ws.write(0, 1, "性别", style)
    ws.write(0, 2, "出生日期", style)
    ws.write(0, 3, "身份证号", style)
    ws.write(0, 4, "医疗卡号", style)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=劳务职员信息.xls'
    book.save(response)
    return response













