#!/usr/local/python
# -*- coding:utf-8 -*-

import simplejson as json
import xlwt
import logging

from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader
from smtplib import SMTPRecipientsRefused

from labour.models import EmployeeProfile, UserProfile, CompanyProfile, Contract
from labour.models import LoginLog, UserAction
from manager.forms import UserAddForm
from utils import adjacent_paginator

INFO_LOG = logging.getLogger('info')

@login_required
def index(request, template_name="manager/index.html"):
    """ 后台管理员界面"""
    user = request.user
    inner_ip = request.META['REMOTE_ADDR']
    return render(request, template_name,{
        'user': user,
        'inner_ip': inner_ip,
    })

@csrf_exempt
@login_required
def update(request, template_name="manager/index.html"):
    """ 账号管理"""
    user = request.user
    update_type = request.POST.get('update_type', None)
    username = request.GET.get("username", '')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            update_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(json.dumps('user_not_exist'))

        if update_type == 'reset_pwd':
            update_user.set_password('111111')
            update_user.save()
            Data = {
                'result': True,
                'name': update_user.username,
            }
            UserAction(
                user=request.user,
                ip=request.META['REMOTE_ADDR'],
                table_name='User',
                modified_type=0,
                modified_id=update_user.id,
                action='重置密码',
            ).save()
            data = u'user=%s, ModifyTable=User, action=重置密码, modified_username=%s'  % (request.user.username, update_user.username)
            INFO_LOG.info(data)
            return HttpResponse(json.dumps(Data))
        elif update_type == 'disabled_user':
            update_user.is_active = False
            update_user.save()
            Data = {
                'result': True,
                'name': update_user.username,
            }
            UserAction(
                user=request.user,
                ip=request.META['REMOTE_ADDR'],
                table_name='User',
                modified_type=0,
                modified_id=update_user.id,
                action='禁止用户',
            ).save()
            data = u'user=%s, ModifyTable=User, action=禁止用户, modified_username=%s'  % (request.user.username, update_user.username)
            INFO_LOG.info(data)
            return HttpResponse(json.dumps(Data))
        elif update_type == 'del_user':
            try:
                account = UserProfile.objects.get(user=update_user)
                if account.level == 1:
                    company = CompanyProfile.objects.get(profile=account)
                    company.profile = None
                    company.save()
            except Exception:
                pass
            
            update_user.delete()
            Data = {
                'result': True,
                'name': update_user.username,
            }
            UserAction(
                user=request.user,
                ip=request.META['REMOTE_ADDR'],
                table_name='User',
                modified_type=0,
                modified_id=update_user.id,
                action='删除用户',
            ).save()
            data = u'user=%s, ModifyTable=User, action=删除用户, modified_username=%s'  % (request.user.username, update_user.username)
            INFO_LOG.info(data)
            return HttpResponse(json.dumps(Data))
        elif update_type == 'active_user':
            update_user.is_active = True
            update_user.save()
            Data = {
                'result': True,
                'name': update_user.username,
            }
            UserAction(
                user=request.user,
                ip=request.META['REMOTE_ADDR'],
                table_name='User',
                modified_type=0,
                modified_id=update_user.id,
                action='解禁用户',
            ).save()
            data = u'user=%s, ModifyTable=User, action=解禁用户, modified_username=%s'  % (request.user.username, update_user.username)
            INFO_LOG.info(data)
        return HttpResponse(json.dumps(Data))

    self_id = user.id
    if username is None:
        user_list = User.objects.all().exclude(id=self_id)
    else:
        user_list = User.objects.filter(username__contains=username).exclude(id=self_id)

    users, page_numbers = adjacent_paginator(user_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'user': user,
        'users': users,
        'page_numbers': page_numbers,
    })


@login_required
def add(request, form_class=UserAddForm, template_name='manager/user_add.html'):
    """ 增加用户"""
    user = request.user
    companys = CompanyProfile.objects.filter(profile=None)

    if request.method == 'POST':
        form = form_class(request, data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, '添加成功', extra_tags='user_add_succ')
    else:
        form = form_class(request)

    return render(request, template_name, {
        'user': user,
        'form': form,
        'companys': companys,
    })

@login_required
def login_log(request, template_name='manager/login_log.html'):
    """ 登录日志查看"""
    user = request.user
    username = request.GET.get('username', '')

    if username == '':
        login_list = LoginLog.objects.all()
    else:
        user_list = User.objects.filter(username__contains=username)
        login_list = LoginLog.objects.filter(user__id__in=user_list)
    login_logs, page_numbers = adjacent_paginator(login_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'user': user,
        'login_logs': login_logs,
        'page_numbers': page_numbers,
        'username': username,
    })


@login_required
def user_action(request, template_name='manager/action_log.html'):
    """ 用户行为记录"""
    user = request.user
    export = request.GET.get('export', None)

    action_list = UserAction.objects.all().order_by("-created")
    user_actions, page_numbers = adjacent_paginator(action_list, request.GET.get('page', 1))

    if export:
        book = xlwt.Workbook(encoding='utf-8')
        ws = book.add_sheet('导出职员信息')
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'
        style.font = font

        x_count = 0
        y_count = 0

        ws.write(x_count, y_count, '操作IP', style)
        y_count += 1
        ws.write(x_count, y_count, '操作账号', style)
        y_count += 1
        ws.write(x_count, y_count, '操作者姓名', style)
        y_count += 1
        ws.write(x_count, y_count, '操作内容', style)
        y_count += 1
        ws.write(x_count, y_count, '操作时间', style)
        y_count += 1

        y_count = 0
        x_count += 1
        for action in action_list:
            ws.write(x_count, y_count, action.ip, style)
            y_count += 1
            ws.write(x_count, y_count, action.user.username, style)
            y_count += 1
            ws.write(x_count, y_count, action.user.account.name, style)
            y_count += 1
            ws.write(x_count, y_count, "%s--%s" % (action.table_name, action.action), style)
            y_count += 1
            ws.write(x_count, y_count, str(action.created)[:10], style)
            y_count += 1

            x_count += 1
            y_count = 0

        response = HttpResponse(mimetype='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=用户操作记录表.xls'
        book.save(response)

        UserAction(
            user=request.user,
            ip=request.META['REMOTE_ADDR'],
            table_name='用户行为信息表',
            modified_type=2,
            modified_id=None,
            action='导出',
        ).save()
        data = u'user=%s, Export_table=UserAction, action=导出' % (request.user.username)
        INFO_LOG.info(data)
        return response

    return render(request, template_name, {
        'user': user,
        'actions': user_actions,
        'page_numbers': page_numbers,
    })

@csrf_exempt
@login_required
def send_email(request, template_name='manager/send_mail.html'):
    """ 发送邮件"""
    companys = CompanyProfile.objects.all()
    #print send_mail(title, content, settings.DEFAULT_FROM_EMAIL, mail_list, fail_silently=False)
    #print "send_mail_succ"
    if request.method == "POST":
        company_ids = request.POST.get("companys")
        title = request.POST.get("title")
        content = request.POST.get("content")
        companys = CompanyProfile.objects.filter(id__in=company_ids.split(",")[1:])
        mail_list = []
        for company in companys:
            mail_list.append(company.email)

        print mail_list
        context = {
            'content': content,
        }
        t = loader.get_template('manager/send_email_template.html')
        try:
            msg = EmailMultiAlternatives(title, t.render(Context(context)), settings.DEFAULT_FROM_EMAIL, mail_list)
            msg.content_subtype = 'html'
            msg.send()
            data = {
                'result': True,
            }
        except SMTPRecipientsRefused:
            messages.error(request, '邮箱不存在，请换个邮箱')
            data = {
                'result': False,
            }

        UserAction(
            user=request.user,
            ip=request.META['REMOTE_ADDR'],
            table_name='无',
            modified_type=2,
            modified_id=None,
            action='发送邮件',
        ).save()
        data = u'user=%s, action=发送邮件, mail_list=%s, content=%s '  % (request.user.username, str(mail_list), content)
        INFO_LOG.info(data)
        return HttpResponse(json.dumps(data))

    return render(request, template_name, {
        'companys': companys,
    })


@login_required
@csrf_exempt
def employee_audit(request, template_name='manager/employee_audit.html'):
    """ 企业人员导入，人员审核"""
    if request.method == 'POST':
        employees_id = request.POST.get('employees_id')
        id_arr = employees_id.lstrip(',').split(',')
        EmployeeProfile.objects.filter(id__in=id_arr).update(is_active=True)
        return HttpResponse(json.dumps({'result': True}))

    empoyees_list = EmployeeProfile.objects.filter(is_active=False)
    empoyees, page_numbers = adjacent_paginator(empoyees_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'employees': empoyees,
    })


@login_required
@csrf_exempt
def companys(request, template_name='manager/companys.html'):
    """ 公司信息-删除"""
    user = request.user

    if request.method == "POST":
        if request.is_ajax():
            try:
                company_id = request.POST.get("company_id")
                if not EmployeeProfile.objects.filter(company_id=company_id, is_deleted=0).exists():
                    company = CompanyProfile.objects.get(id=company_id)
                    company.is_deleted = 1
                    company.save()
                    UserAction(
                        user=request.user,
                        ip=request.META['REMOTE_ADDR'],
                        table_name='公司信息表',
                        modified_type=1,
                        modified_id=None,
                        action='删除',
                    ).save()
                    data = u'user=%s, delete_table=CompanyProfile,  action=删除, \
                             delete_name=%s, delete_id=%s' % (user.username, company.name, company.id)
                    INFO_LOG.info(data)
                    return HttpResponse(json.dumps({"result": True, "msg": "删除成功"}))
                else:
                    return HttpResponse(json.dumps({"result": False, "msg": "请先删除全部员工信息再删除公司"}))
            except CompanyProfile.DoesNotExist:
                pass

    company_list = CompanyProfile.objects.filter(is_deleted=0)

    companys, page_numbers = adjacent_paginator(company_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'companys': companys,
        'page_numbers': page_numbers,
    })


@login_required
@csrf_exempt
def company_employees(request, company_id, template_name='manager/company_employees.html'):
    """ 公司人员信息-删除"""
    user = request.user
    name = request.GET.get('name', None)
    id_no = request.GET.get('id_no', None)
    health_card = request.GET.get('health_card', None)
    search = request.GET.get('search', None)
    search_dict = {}
    extra_kwargs = {}

    if search is not None:
        if name != '':
            search_dict['name__contains'] = name
        if id_no != '':
            search_dict['id_no__contains'] = id_no
        if health_card != '':
            search_dict['health_card__contains'] = health_card

        UserAction(
            user=user,
            ip=request.META['REMOTE_ADDR'],
            table_name='雇员信息表',
            modified_type=2,
            modified_id=None,
            action='搜索',
        ).save()
        data = u'user=%s, search_table=EmployeeProfile,  action=搜索, search_name=%s, search_id_no=%s, search_health_card=%s' % (user.username, name, id_no, health_card)
        INFO_LOG.info(data)

        employee_list = EmployeeProfile.objects.filter(company_id=company_id, is_deleted=0, **search_dict)
    else:
        employee_list = EmployeeProfile.objects.filter(company_id=company_id, is_deleted=0, **extra_kwargs)

    employees, page_numbers = adjacent_paginator(employee_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'employees': employees,
        'user': request.user,
        'name': name,
        'id_no': id_no,
        'health_card': health_card,
    })


@login_required
@csrf_exempt
def delete_employee(request):
    """ 公司人员信息-删除"""
    if request.method == "POST":
        if request.is_ajax():
            try:
                employee_arr = request.POST.get("employees_id").split(",")[1:]
                employees = EmployeeProfile.objects.filter(id__in=employee_arr, is_deleted=0)
                for employee in employees:
                    employee.delete()
                    UserAction(
                        user=request.user,
                        ip=request.META['REMOTE_ADDR'],
                        table_name='职员信息表',
                        modified_type=3,
                        modified_id=employee.id,
                        action='删除',
                    ).save()
                return HttpResponse(json.dumps({"result": True, "msg": "删除成功"}))

            except EmployeeProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": False, "msg": "职员不存在"}))
    return HttpResponse(json.dumps({"result": False, "msg": "error"}))


