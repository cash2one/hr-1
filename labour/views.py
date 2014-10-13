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
from django.contrib.auth.decorators import login_required


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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def employees(request, template_name='labour/employees.html'):
    """ 全部员工信息"""
    
    name = request.GET.get('name', None)
    id_no = request.GET.get('id_no', None)
    health_card = request.GET.get('health_card', None)
    search = request.GET.get('search', None)
    export = request.POST.get('export', None)
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

    # 导出表格
    if export is not None:
        employees_id = request.POST.get('employees_id')
        items = request.POST.get('item')
        employees_arr = employees_id.split(',')
        items_arr = items.split(',')
        employee_export = EmployeeProfile.objects.filter(id__in=employees_arr)
        excel_title = []
        if 'name' in items:
            excel_title.append('姓名')


    employees, page_numbers = adjacent_paginator(employee_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'employees': employees,
        'user': request.user,
        'name': name,
        'id_no': id_no,
        'health_card': health_card,
    })

@login_required
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

@login_required
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


@login_required
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

@login_required
def statistics(request, statis_type='all', template_name='labour/labour_statistics.html'):
    """ 劳务信息统计"""
    today = datetime.datetime.now()
    is_contract = None
    is_employee = None

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
        employee_list = EmployeeProfile.objects.all()
        year = datetime.datetime.now().year
        retire_count = 0
        for employee in employee_list:
            id_no_year = int(employee.id_no[6:10])
            if employee.sex == '女':
                if year - id_no_year >= 50:
                    retire_count = retire_count + 1
            else:
                if year - id_no_year >= 60:
                    retire_count = retire_count + 1

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
            'retire_count': retire_count,
        })

    elif statis_type == 'endowment':
        profiles = EmployeeProfile.objects.filter(endowment_payment_end__lt=today)
        is_employee = True
    elif statis_type == 'health':
        profiles = EmployeeProfile.objects.filter(health_payment_end__lt=today)
        is_employee = True
    elif statis_type == 'born':
        profiles = EmployeeProfile.objects.filter(born_payment_end__lt=today)
        is_employee = True
    elif statis_type == 'industrial':
        profiles = EmployeeProfile.objects.filter(industrial_payment_end__lt=today)
        is_employee = True
    elif statis_type == 'unemployeed':
        profiles = EmployeeProfile.objects.filter(unemployed_payment_end__lt=today)
        is_employee = True
    elif statis_type == 'reserved':
        profiles = EmployeeProfile.objects.filter(reserved_payment_end__lt=today)
        is_employee = True
    elif statis_type == 'company_protocal':
        profiles = Contract.objects.filter(company_protocal_end__lt=today)
        is_contract = True
    elif statis_type == 'labour_contract':
        profiles = Contract.objects.filter(labour_contract_end__lt=today)
        is_contract = True
    elif statis_type == 'probation':
        profiles = Contract.objects.filter(probation_end__lt=today)
        is_contract = True
    elif statis_type == 'retire':
        employee_list = EmployeeProfile.objects.all()
        is_employee = True
        year = datetime.datetime.now().year
        retire_id = []
        for employee in employee_list:
            id_no_year = int(employee.id_no[6:10])
            if employee.sex == '女':
                if year - id_no_year >= 50:
                    retire_id.append(employee.id)
            else:
                if year - id_no_year >= 60:
                    retire_id.append(employee.id)

        profiles = EmployeeProfile.objects.filter(id__in=retire_id)
    else:
        return HttpResponseRedirect(reverse('labour.views.statistics'))

    template_name = 'labour/labour_statistics_detail.html'

    employees, page_numbers = adjacent_paginator(profiles, request.GET.get('page', 1))
    
    return render(request, template_name, {
        'employees': employees,
        'is_contract': is_contract,
        'is_employee': is_employee,
    })

@login_required
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

@login_required
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


@login_required
def labour_export(request):
    """ excel导出"""

    export = request.GET.get('export', None)
    #company_id = request.GET.get('company_id', None)

    if export is not None:
        employees_id = request.POST.get('employees_id')
        item = request.POST.get('item')
        employees_arr = employees_id.split(',')
        items = item.split(',')
        employees_arr[0] = employees_arr[1]
        employees = EmployeeProfile.objects.filter(id__in=employees_arr)
        x_count = 0
        y_count = 0
        temp = 0
        insert_sign = None

        book = xlwt.Workbook(encoding='utf-8')
        ws = book.add_sheet('导出职员信息')
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'
        style.font = font

        def insert(insert_sign, x, y, name, value):
            if insert_sign is None:
                ws.write(x, y, name, style)
            else:
                if value is None:
                    ws.write(x, y, '无', style)
                else:
                    ws.write(x, y, value, style)
            y += 1
            return y

        def insurance_base(insert_sign, x_count, y_count, name, value, card):
            if insert_sign is None:
                if card is not None:
                    ws.write(x_count, y_count, '%s保险卡' % name, style)
                    y_count += 1
                ws.write(x_count, y_count, '%s缴费基数' % name, style)
                y_count += 1
                ws.write(x_count, y_count, '%s个人缴费' % name, style)
                y_count += 1
                ws.write(x_count, y_count, '%s公司缴费' % name, style)
                y_count += 1
                ws.write(x_count, y_count, '%s缴费起始时间' % name, style)
                y_count += 1
                ws.write(x_count, y_count, '%s缴费终止时间' % name, style)
                y_count += 1
            else:
                if value is None or value == 'None':
                    value = '无'
                ws.write(x_count, y_count, value, style)
                y_count += 1

            return y_count
                
        def select_insert_excel(insert_sign, x_count, y_count, style, employee):
            if 'serial_id' in items:
                y_count = insert(insert_sign, x_count, y_count, '序号', employee.serial_id)
            if 'name' in items:
                y_count = insert(insert_sign, x_count, y_count, '姓名', employee.name)
            if 'email' in items:
                y_count = insert(insert_sign, x_count, y_count, '邮箱', employee.email)
            if 'sex' in items:
                y_count = insert(insert_sign, x_count, y_count, '性别', employee.sex)
            if 'id_no' in items:
                y_count = insert(insert_sign, x_count, y_count, '身份证号', employee.id_no)
            if 'nation' in items:
                y_count = insert(insert_sign, x_count, y_count, '民族', employee.nation)
            if 'birth' in items:
                y_count = insert(insert_sign, x_count, y_count, '出生日期', str(employee.birth)[:10])
            if 'edu_level' in items:
                y_count = insert(insert_sign, x_count, y_count, '教育水平', employee.edu_level)
            if 'graduate' in items:
                y_count = insert(insert_sign, x_count, y_count, '毕业院校', employee.graduate)
            if 'profession' in items:
                y_count = insert(insert_sign, x_count, y_count, '专业', employee.profession)
            if 'residence_type' in items:
                y_count = insert(insert_sign, x_count, y_count, '户口类型', employee.residence_type)
            if 'residence_place' in items:
                y_count = insert(insert_sign, x_count, y_count, '户籍行政区', employee.residence_place)
            if 'now_address' in items:
                y_count = insert(insert_sign, x_count, y_count, '现在住址', employee.now_address)
            if 'emergency_name' in items:
                y_count = insert(insert_sign, x_count, y_count, '联系人姓名', employee.emergency_name)
            if 'emergency_mobile' in items:
                y_count = insert(insert_sign, x_count, y_count, '联系人电话', employee.emergency_mobile)
            if 'fire' in items:
                if insert_sign is None:
                    ws.write(x_count, y_count, '是否解雇', style)
                    y_count += 1
                    ws.write(x_count, y_count, '解雇时间', style)
                    y_count += 1
                    ws.write(x_count, y_count, '解雇原因', style)
                    y_count += 1
                else:
                    ws.write(x_count, y_count, employee.is_fired, style)
                    y_count += 1
                    ws.write(x_count, y_count, str(employee.fired_date)[:10], style)
                    y_count += 1
                    ws.write(x_count, y_count, employee.fired_reason, style)
                    y_count += 1

            if 'yliao' in items:
                if insert_sign:
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.health_card, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.health_payment_base, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.health_payment_self, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.health_payment_company, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.health_payment_start)[:10], 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.health_payment_end)[:10], 'yes')
                else:
                    y_count = insurance_base(insert_sign, x_count, y_count, '医疗保险', '', 'yes')

            if 'ylao' in items:
                if insert_sign:
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.endowment_card, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.endowment_payment_base, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.endowment_payment_self, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.endowment_payment_company, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.endowment_payment_start)[:10], 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.endowment_payment_end)[:10], 'yes')
                else:
                    y_count = insurance_base(insert_sign, x_count, y_count, '养老保险', '', 'yes')

            if 'syu' in items:
                if insert_sign:
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.born_payment_base, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.born_payment_self, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.born_payment_company, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.born_payment_start)[:10], 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.born_payment_end)[:10], 'yes')
                else:
                    y_count = insurance_base(insert_sign, x_count, y_count, '生育保险', '', None)

            if 'gshang' in items:
                if insert_sign:
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.industrial_payment_base, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.industrial_payment_self, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.industrial_payment_company, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.industrial_payment_start)[:10], 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.industrial_payment_end)[:10], 'yes')
                else:
                    y_count = insurance_base(insert_sign, x_count, y_count, '工伤保险', '', None)

            if 'sye' in items:
                if insert_sign:
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.unemployed_payment_base, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.unemployed_payment_self, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.unemployed_payment_company, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.unemployed_payment_start)[:10], 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.unemployed_payment_end)[:10], 'yes')
                else:
                    y_count = insurance_base(insert_sign, x_count, y_count, '失业保险', '', None)

            if 'gjj' in items:
                if insert_sign:
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.reserved_payment_base, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.reserved_payment_self, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', employee.reserved_payment_company, 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.reserved_payment_start)[:10], 'yes')
                    y_count = insurance_base(insert_sign, x_count, y_count, '', str(employee.reserved_payment_end)[:10], 'yes')
                else:
                    y_count = insurance_base(insert_sign, x_count, y_count, '公积金', '', None)

            if 'company' in items:
                if insert_sign is None:
                    ws.write(x_count, y_count, '公司名称', style)
                    y_count += 1
                    ws.write(x_count, y_count, '公司地址', style)
                    y_count += 1
                    ws.write(x_count, y_count, '公司邮箱', style)
                    y_count += 1
                    ws.write(x_count, y_count, '公司联系人', style)
                    y_count += 1
                    ws.write(x_count, y_count, '公司电话', style)
                    y_count += 1
                    ws.write(x_count, y_count, '服务费', style)
                    y_count += 1
                else:
                    try:
                        ws.write(x_count, y_count, employee.company.name, style)
                        y_count += 1
                        ws.write(x_count, y_count, employee.company.address, style)
                        y_count += 1
                        ws.write(x_count, y_count, employee.company.email, style)
                        y_count += 1
                        ws.write(x_count, y_count, employee.company.link_man, style)
                        y_count += 1
                        ws.write(x_count, y_count, employee.company.link_man_mobile, style)
                        y_count += 1
                        ws.write(x_count, y_count, employee.company.service_cost, style)
                        y_count += 1
                    except:
                        ws.write_merge(x_count, x_count, y_count, y_count+5, u"无", style)
                        y_count += 6
            if 'contract' in items:
                if insert_sign is None:
                    ws.write(x_count, y_count, '工种', style)
                    y_count += 1
                    ws.write(x_count, y_count, '单位协议开始时间', style)
                    y_count += 1
                    ws.write(x_count, y_count, '单位协议结束时间', style)
                    y_count += 1
                    ws.write(x_count, y_count, '劳动合同开始时间', style)
                    y_count += 1
                    ws.write(x_count, y_count, '劳动合同结束时间', style)
                    y_count += 1
                    ws.write(x_count, y_count, '试用期开始时间', style)
                    y_count += 1
                    ws.write(x_count, y_count, '试用期结束时间', style)
                    y_count += 1
                    ws.write(x_count, y_count, '银行卡号', style)
                    y_count += 1
                    ws.write(x_count, y_count, '月工资', style)
                    y_count += 1
                    ws.write(x_count, y_count, '实发工资', style)
                    y_count += 1
                    ws.write(x_count, y_count, '工资发放时间', style)
                    y_count += 1
                else:
                    try:
                        ws.write(x_count, y_count, employee.contract.job_type, style)
                        y_count += 1
                        ws.write(x_count, y_count, str(employee.contract.company_protocal_start)[:10], style)
                        y_count += 1
                        ws.write(x_count, y_count, str(employee.contract.company_protocal_end)[:10], style)
                        y_count += 1
                        ws.write(x_count, y_count, str(employee.contract.labour_contract_start)[:10], style)
                        y_count += 1
                        ws.write(x_count, y_count, str(employee.contract.labour_contract_end)[:10], style)
                        y_count += 1
                        ws.write(x_count, y_count, str(employee.contract.probation_start)[:10], style)
                        y_count += 1
                        ws.write(x_count, y_count, str(employee.contract.probation_end)[:10], style)
                        y_count += 1
                        ws.write(x_count, y_count, employee.contract.bank_no, style)
                        y_count += 1
                        ws.write(x_count, y_count, employee.contract.month_salary, style)
                        y_count += 1
                        ws.write(x_count, y_count, employee.contract.real_salary, style)
                        y_count += 1
                        ws.write(x_count, y_count, str(employee.contract.salary_provide)[:10], style)
                        y_count += 1
                    except:
                        ws.write_merge(x_count, x_count, y_count, y_count+10, u"无", style)
                        y_count += 1

            x_count += 1
            y_count = 0
            return x_count, y_count, ws

        for employee in employees:
            if insert_sign is None:
                x_count, y_count, ws = select_insert_excel(insert_sign, x_count, y_count, style, employee)
            insert_sign = True
            x_count, y_count, ws = select_insert_excel(insert_sign, x_count, y_count, style, employee)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=劳务职员信息.xls'
    book.save(response)
    return response
