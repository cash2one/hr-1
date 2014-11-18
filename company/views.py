#!/usr/local/python
# -*- coding:utf-8 -*-

import datetime
import xlwt
import xlrd
import logging

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from labour.forms import EmployeeProfileForm, ContractForm, CompanyForm
from labour.models import EmployeeProfile, UserProfile, CompanyProfile, Contract
from labour.models import MoneyRecord, UserAction
from labour.forms import HealthForm, BornForm, UnemployeedForm, ReservedForm
from labour.forms import LabourImportForm, IndustrialForm, EndowmentForm
from utils import adjacent_paginator

from django.shortcuts import render

INFO_LOG = logging.getLogger('info')

@login_required
def property(request, template_name='labour/company_property.html'):
    """ 企业资金管理"""
    today = datetime.datetime.now()
    year = today.year
    month = today.month

    if not MoneyRecord.objects.filter(year=year, month=month).exists():
        company_list = CompanyProfile.objects.all()
        for company in company_list:
            employee_count = EmployeeProfile.objects.filter(company=company).count()
            contracts = Contract.objects.filter(employee__company=company)
            employee_salary_sum = 0.0
            for contract in contracts:
                employee_salary_sum = employee_salary_sum + float(contract.real_salary)
            deserve = float(company.service_cost) * employee_count + employee_salary_sum
            actual = 0.0
            balance = 0.0
            history_balance = MoneyRecord.objects.filter(company=company, year=year)
            for history in history_balance:
                balance = balance + float(history.balance)

            balance = balance + actual - deserve
            MoneyRecord(
                company=company,
                deserve=str(deserve),
                actual=str(actual),
                balance=str(balance),
                year=year,
                month=month,
            ).save()

    money_list = MoneyRecord.objects.filter(year=year, month=month)

    companys, page_numbers = adjacent_paginator(money_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'companys': companys,
        'page_numbers': page_numbers,
    })


@login_required
def property_detail(request, template_name='labour/company_property_detail.html'):
    """ 该公司资金详情"""
    year = request.GET.get('year', '2014')
    company_id = request.GET.get('id')
    try:
        company = CompanyProfile.objects.get(pk=company_id)
    except CompanyProfile.DoesNotExist:
        return HttpResponseRedirect(reverse('company.views.property'))

    record_list = MoneyRecord.objects.filter(company=company, year=year)
    deserve_sum = 0.0
    actual_sum = 0.0
    for record in record_list:
        deserve_sum = deserve_sum + float(record.deserve)
        actual_sum = actual_sum + float(record.actual)
    
    balance_sum = actual_sum - deserve_sum
    records, page_numbers = adjacent_paginator(record_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'records': records,
        'page_numbers': page_numbers,
        'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'deserve_sum': deserve_sum,
        'actual_sum': actual_sum,
        'balance_sum': balance_sum,
        'year': year,
        'company_id': company_id
    })


@login_required
def salary(request, template_name='labour/company_salary_search.html'):
    """ 个人工资搜索"""
    search_args = {}

    name = request.GET.get('name', '')
    id_no = request.GET.get('id_no', '')
    company_id = request.GET.get('company_id', '')
    export = request.GET.get('export_s', None)

    if name:
        search_args['name__contains'] = name
    if id_no:
        search_args['id_no__contains'] = id_no
    if company_id:
        search_args['company__id'] = company_id

    try:
        int(company_id)
    except:
        company_id = 0

    # 批量修改工资发放时间
    if request.method == 'POST':
        change_date = request.POST.get("change_date", None)
        select_ids = request.POST.get("select_ids", None)
        if change_date:
            id_attr = select_ids.split(',')[1:]
            contracts = Contract.objects.filter(employee__id__in=id_attr)
            for contract in contracts:
                contract.salary_provide = change_date
                contract.save()
                UserAction(
                    user=request.user,
                    ip=request.META['REMOTE_ADDR'],
                    table_name='合同表',
                    modified_type=3,
                    modified_id=contract.employee.id,
                    action='工资发放时间修改',
                ).save()
                data = u'操作员=%s, ModifyTable=Contract, action=工资发放时间修改, modified_username=%s, company_name=%s, money=%s'  % (request.user.username, contract.employee.name, contract.employee.company.name, contract.real_salary)
                INFO_LOG.info(data)

    employee_list = EmployeeProfile.objects.filter(company__isnull=False, **search_args)
    companys = CompanyProfile.objects.all()
    employees, page_numbers = adjacent_paginator(employee_list, request.GET.get('page', 1))

    # 导出
    if export:
        book = xlwt.Workbook(encoding='utf-8')
        ws = book.add_sheet('工资管理信息')
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'
        style.font = font

        x_count = 0
        y_count = 0

        ws.write(x_count, y_count, '姓名', style)
        y_count += 1
        ws.write(x_count, y_count, '用工单位', style)
        y_count += 1
        ws.write(x_count, y_count, '月工资', style)
        y_count += 1
        ws.write(x_count, y_count, '实发工资', style)
        y_count += 1
        ws.write(x_count, y_count, '养老保险', style)
        y_count += 1
        ws.write(x_count, y_count, '医疗保险', style)
        y_count += 1
        ws.write(x_count, y_count, '生育保险', style)
        y_count += 1
        ws.write(x_count, y_count, '工伤保险', style)
        y_count += 1
        ws.write(x_count, y_count, '失业保险', style)
        y_count += 1
        ws.write(x_count, y_count, '公积金', style)
        y_count += 1

        x_count += 1
        y_count = 0

        for employee in employees:
            ws.write(x_count, y_count, employee.name, style)
            y_count += 1
            ws.write(x_count, y_count, employee.company.name, style)
            y_count += 1
            ws.write(x_count, y_count, employee.contract.month_salary, style)
            y_count += 1
            ws.write(x_count, y_count, employee.contract.real_salary, style)
            y_count += 1
            ws.write(x_count, y_count, employee.endowment_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.health_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.born_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.industrial_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.unemployed_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.reserved_payment_self, style)
            y_count = 0
            x_count += 1
            
        response = HttpResponse(mimetype='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=工资管理信息.xls'
        book.save(response)
        UserAction(
            user=request.user,
            ip=request.META['REMOTE_ADDR'],
            table_name='User',
            modified_type=3,
            modified_id=None,
            action='工资导出',
        ).save()
        data = u'操作者=%s, ModifyTable=Contract, action=工资导出'  % (request.user.username)
        INFO_LOG.info(data)

        return response

    return render(request, template_name, {
        'employees': employees,
        'page_numbers': page_numbers,
        'companys': companys,
        'name': name,
        'id_no': id_no,
        'company_id': int(company_id),
    })


@login_required
def insurance(request, template_name='labour/company_insurance_search.html'):
    """ 保险搜索"""
    search_args = {}

    name = request.GET.get('name', '')
    id_no = request.GET.get('id_no', '')
    company_id = request.GET.get('company_id', '')
    export = request.GET.get('export_s', None)
    if name:
        search_args['name__contains'] = name
    if id_no:
        search_args['id_no__contains'] = id_no
    if company_id:
        search_args['company__id'] = company_id

    try:
        int(company_id)
    except:
        company_id = 0

    # 批量修改工资发放时间
    if request.method == 'POST':
        change_date = request.POST.get("change_date", None)
        select_ids = request.POST.get("select_ids", None)
        insurance_type = request.POST.get('insurance_type', None)

        if change_date:
            id_attr = select_ids.split(',')[1:]
            employees = EmployeeProfile.objects.filter(id__in=id_attr)
            for employee in employees:
                if insurance_type == 'health':
                    employee.health_payment_end = change_date
                elif insurance_type == 'endowment':
                    employee.endowment_payment_end = change_date
                elif insurance_type == 'born':
                    employee.born_payment_end = change_date
                elif insurance_type == 'industrial':
                    employee.industrial_payment_end = change_date
                elif insurance_type == 'unemployed':
                    employee.unemployed_payment_end = change_date
                elif insurance_type == 'reserved':
                    employee.reserved_payment_end = change_date
                employee.save()
                UserAction(
                    user=request.user,
                    ip=request.META['REMOTE_ADDR'],
                    table_name='员工信息表',
                    modified_type=3,
                    modified_id=employee.id,
                    action=u'%s保险截止时间修改' % insurance_type,
                ).save()
                data = u'操作员=%s, ModifyTable=EmployeeProfile, action=%s保险截止时间修改, modified_username=%s, company_name=%s'  % (request.user.username, insurance_type, employee.name, employee.company.name)
                INFO_LOG.info(data)

    employee_list = EmployeeProfile.objects.filter(company__isnull=False, **search_args)
    companys = CompanyProfile.objects.all()
    employees, page_numbers = adjacent_paginator(employee_list, request.GET.get('page', 1))

    # 导出
    if export:
        book = xlwt.Workbook(encoding='utf-8')
        ws = book.add_sheet('保险管理信息')
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'
        style.font = font

        x_count = 0
        y_count = 0

        ws.write(x_count, y_count, '姓名', style)
        y_count += 1
        ws.write(x_count, y_count, '用工单位', style)
        y_count += 1
        ws.write(x_count, y_count, '养老保险截止时间', style)
        y_count += 1
        ws.write(x_count, y_count, '医疗保险截止时间', style)
        y_count += 1
        ws.write(x_count, y_count, '生育保险截止时间', style)
        y_count += 1
        ws.write(x_count, y_count, '工伤保险截止时间', style)
        y_count += 1
        ws.write(x_count, y_count, '失业保险截止时间', style)
        y_count += 1
        ws.write(x_count, y_count, '公积金截止时间', style)
        y_count += 1

        x_count += 1
        y_count = 0

        for employee in employees:
            ws.write(x_count, y_count, employee.name, style)
            y_count += 1
            ws.write(x_count, y_count, employee.company.name, style)
            y_count += 1
            ws.write(x_count, y_count, employee.contract.month_salary, style)
            y_count += 1
            ws.write(x_count, y_count, employee.contract.real_salary, style)
            y_count += 1
            ws.write(x_count, y_count, employee.endowment_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.health_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.born_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.industrial_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.unemployed_payment_self, style)
            y_count += 1
            ws.write(x_count, y_count, employee.reserved_payment_self, style)
            y_count = 0
            x_count += 1
            
        response = HttpResponse(mimetype='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=保险管理信息.xls'
        book.save(response)
        UserAction(
            user=request.user,
            ip=request.META['REMOTE_ADDR'],
            table_name='User',
            modified_type=3,
            modified_id=None,
            action='工资导出',
        ).save()
        data = u'操作者=%s, ModifyTable=Contract, action=工资导出'  % (request.user.username)
        INFO_LOG.info(data)

        return response

    return render(request, template_name, {
        'employees': employees,
        'page_numbers': page_numbers,
        'companys': companys,
        'name': name,
        'id_no': id_no,
        'company_id': int(company_id),
    })