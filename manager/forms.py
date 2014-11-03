#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

from django import forms
from django.contrib.auth.models import User

from labour.models import UserProfile, CompanyProfile, UserAction

INFO_LOG = logging.getLogger('info')

class UserAddForm(forms.Form):
    """ 添加用户"""
    def __init__(self, request=None, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        self._request = request

    username = forms.CharField(label='用户名', max_length=30, widget=forms.TextInput(attrs={'placeholder': '请输入您的用户名', 'class': 'text_input'}), error_messages={'required': '请输入您的用户名'})
    name = forms.CharField(label='姓名', max_length=30, widget=forms.TextInput(attrs={'placeholder': '请输入真实姓名', 'class': 'text_input'}), error_messages={'required': '请输入真实姓名'})
    pwd = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=False, attrs={'placeholder': '请输入密码', 'class': 'text_input'}), error_messages={'required': '请输入您的密码'})
    confirm = forms.CharField(label='再次输入', widget=forms.PasswordInput(render_value=False, attrs={'placeholder': '请再次输入密码', 'class': 'text_input'}), error_messages={'required': '请输入再次输入密码'})

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('该用户已存在')
        return self.cleaned_data['username']

    def clean(self):
        pwd = self.cleaned_data.get('pwd', None)
        confirm = self.cleaned_data.get('confirm', None)
        name = self.cleaned_data.get('name', None)

        if pwd is None:
            raise forms.ValidationError('密码不能为空')
        elif confirm is None:
            raise forms.ValidationError('请再次输入密码')
        elif name is None:
            raise forms.ValidationError('请输入姓名')
        
        if pwd != confirm:
            raise forms.ValidationError('两次输入的密码不同')
        return self.cleaned_data

    def save(self):
        user = User(
            username=self.cleaned_data['username'],
            is_active=True,
        )
        user.set_password(self.cleaned_data['pwd'])
        user.save()
        level = self._request.POST['level']
        profile = UserProfile(
            user=user,
            name=self.cleaned_data['name'],
            level=level,
        )
        profile.save()
        if level == '1':
            company = CompanyProfile.objects.get(id=self._request.POST.get('company_id'))
            company.user = user
            company.save()

        data = u'user=%s, modify_table=UserProfile, action=添加, add_user_id=%d, add_user_name=%s' % (self._request.user.username, user.id, profile.name)
        INFO_LOG.info(data)

        UserAction(
            user=self._request.user,
            ip=self._request.META['REMOTE_ADDR'],
            table_name='雇员信息表',
            modified_type=0,
            modified_id=user.id,
            action='添加',
        ).save()

