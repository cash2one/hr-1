#!/usr/local/python
# -*- coding:utf-8 -*-

import simplejson as json

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

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            update_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(json.dumps('user_not_exist'))

        if update_type == 'reset_pwd':
            update_user.set_password('111111')
            update_user.save()
            data = {
                'result': True,
                'name': update_user.username,
            }
            return HttpResponse(json.dumps(data))
        elif update_type == 'disabled_user':
            update_user.is_active = False
            update_user.save()
            data = {
                'result': True,
                'name': update_user.username,
            }
            return HttpResponse(json.dumps(data))
        elif update_type == 'active_user':
            update_user.is_active = True
            update_user.save()
            data = {
                'result': True,
                'name': update_user.username,
            }
        return HttpResponse(json.dumps(data))

    self_id = user.id
    user_list = User.objects.all().exclude(id=self_id)
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
        print request.POST
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
    username = request.GET.get('username', None)

    if username is None :
        login_list = LoginLog.objects.all()
    else:
        user_list = User.objects.filter(username__contains=username)
        login_list = LoginLog.objects.filter(user__id__in=user_list)
    login_logs, page_numbers = adjacent_paginator(login_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'user': user,
        'login_logs': login_logs,
        'page_numbers': page_numbers,
    })


@login_required
def user_action(request, template_name='manager/action_log.html'):
    """ 用户行为记录"""
    user = request.user
    action_list = UserAction.objects.all()
    user_actions, page_numbers = adjacent_paginator(action_list, request.GET.get('page', 1))

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
        
        return HttpResponse(json.dumps(data))
    return render(request, template_name, {
        'companys': companys,
    })
