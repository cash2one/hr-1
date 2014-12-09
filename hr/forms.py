#!/usr/bin/python
#encoding:utf8

import logging
import re
import urllib2
import datetime

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate

from labour.models import LoginLog

from utils import generate_info_msg

LOGIN_LOG = logging.getLogger('login')
INFO_LOG = logging.getLogger('info')


class LoginForm(forms.Form):
    """ 登录验证"""

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self._request = request

    username = forms.CharField(label='用户名', max_length=20, 
                                widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}), 
                                error_messages={'required': '请输入用户名'})
    password = forms.CharField(label='密码', max_length=20, 
                                widget=forms.PasswordInput(render_value=False, attrs={'placeholder': '请输入密码', 'id': 'password'}), 
                                error_messages={'required': '请输入密码'})

    def login(self, request):
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])  
        login(request, user)

    def clean_username(self):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            if not user.is_active:
                raise forms.ValidationError('该用户已被禁用!')
        except User.DoesNotExist:
            raise forms.ValidationError('您输入的用户名不存在!')
        return self.cleaned_data['username']

    def clean(self):
        if self.errors:
            return
        import socket
        inner_ip = socket.gethostbyname(socket.gethostname())
        # outer_ip = self._request.META['REMOTE_ADDR']
        #import ipgetter
        #outer_ip = ipgetter.myip()
        #outer_ip = urllib2.urlopen('https://enabledns.com/ip').read()
        # inner_ip = re.search('\d+\.\d+\.\d+\.\d+',urllib2.urlopen("http://www.whereismyip.com").read()).group(0)
        outer_ip = self._request.META['REMOTE_ADDR']
        #outer_ip = urllib2.urlopen("http://myip.dnsdynamic.org/").read()
        user = User.objects.get(username=self.cleaned_data['username'])
        if not user.check_password(self.cleaned_data['password']):
            log = LoginLog(
                user=user,
                inner_ip=inner_ip,
                outer_ip=outer_ip,
                result=u'密码错误',
                created=datetime.datetime.now(),
            )
            log.save()
            data = u'user=%s, action=login, result=%s' % (user.username, log.result)
            LOGIN_LOG.info(data)
            raise forms.ValidationError('您输入的用户名或密码错误!')
        else:
            if user.is_active:
                log = LoginLog(
                    user=user,
                    inner_ip=inner_ip,
                    outer_ip=outer_ip,
                    result=u'成功',
                    created=datetime.datetime.now(),
                )
                log.save()
                data = u'user=%s, action=login, result=%s' % (user.username, log.result)
                LOGIN_LOG.info(data)
            else:
                log = LoginLog(
                    user=user,
                    inner_ip=inner_ip,
                    outer_ip=outer_ip,
                    result=u'账号冻结',
                    created=datetime.datetime.now(),
                )
                log.save()
                data = u'user=%s, action=login, result=%s' % (user.username, log.result)
                LOGIN_LOG.info(data)
                raise forms.ValidationError('该账号已被冻结')
            
        return self.cleaned_data

class ChangePwdForm(forms.Form):
    """ 修改密码"""
    def __init__(self, request=None, *args, **kwargs):
        super(ChangePwdForm, self).__init__(*args, **kwargs)
        self._request = request
        self._user = request.user

    old_pwd = forms.CharField(label='原密码', widget=forms.PasswordInput(render_value=False), error_messages={'required': '请输入原密码'})
    new_pwd = forms.CharField(label='新密码', widget=forms.PasswordInput(render_value=False), error_messages={'required': '请输入密码'})
    confirm_pwd = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=False), error_messages={'required': '请输入确认密码'})

    def clean_old_pwd(self):
        if not self._user.check_password(self.cleaned_data['old_pwd']):
            raise forms.ValidationError('原密码输入错误')
        return self.cleaned_data['old_pwd']

    def clean(self):
        if self.errors:
            return
        new_pwd = self.cleaned_data['new_pwd']
        confirm_pwd = self.cleaned_data['confirm_pwd']
        if len(new_pwd) == 0 or len(confirm_pwd) == 0:
            raise forms.ValidationError('新密码不能为空')
        if new_pwd != confirm_pwd:
            raise forms.ValidationError('两次密码输入不一致')
        if self.cleaned_data['old_pwd'] == self.cleaned_data['new_pwd']:
            raise forms.ValidationError('原密码和新密码不能相同')
        return self.cleaned_data

    def save(self):
        self._user.set_password(self.cleaned_data['new_pwd'])
        self._user.save()
