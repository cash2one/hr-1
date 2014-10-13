#!/usr/bin/python
#encoding:utf-8

import simplejson as json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from labour.models import UserProfile
from hr.forms import LoginForm

def login(request, form_class=LoginForm, template_name='login.html'):
    """ 用户登录"""
    if request.method == "POST":
        form = form_class(request, data=request.POST)
        if form.is_valid():
            form.login(request)
            level = request.user.account.level
            if level == UserProfile.ADMIN:
                return HttpResponseRedirect(reverse('labour.views.index'))
    else:
        form = form_class(request)
    return render(request, template_name, {
        'form': form,
    })

def logout(request):
    """ 退出"""
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect('/')
