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


def test(request, template_name='test.html'):
    return render(request, template_name)


def login(request, form_class=LoginForm, template_name='login.html'):
    """ 用户登录"""
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:
        ip = request.META['REMOTE_ADDR']  
    print ip
    if request.method == "POST":
        form = form_class(request, data=request.POST)
        if form.is_valid():
            form.login(request)
            level = request.user.account.level
            if level == UserProfile.ADMIN:
                return HttpResponseRedirect(reverse('labour.views.index'))
            elif level == UserProfile.MANAGER:
                return HttpResponseRedirect(reverse('manager.views.update'))
            elif level == UserProfile.COMPANY:
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
