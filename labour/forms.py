#!/usr/bin/python
# -*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from labour.models import EmployeeProfile, Contract, CompanyProfile

class EmployeeProfileForm(forms.ModelForm):
    """ 公司员工信息表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = EmployeeProfile
        fields = ['serial_id', 'birth', 'id_no','name', 'nation', 'graduate', 'profession', \
            'residence_type', 'residence_place', 'now_address', 'mobile', 'emergency_name',\
            'emergency_mobile', 'sex']

    serial_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '请输入序列号'}), error_messages={'required': '请输入序列号'})
    name = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': '请输入姓名'}), error_messages={'required': '请输入姓名'})
    nation = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': '请输入民族'}), required=False)
    id_no = forms.CharField(max_length=18, widget=forms.TextInput(attrs={'placeholder': '请输入身份证号'}), error_messages={'required': '请输入身份证号'})

    graduate = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '请输入毕业院校'}), required=False)
    profession = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '请输入专业'}), required=False)
    residence_place = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': '请输入户籍行政区'}), required=False)
    now_address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': '请输入地址', 'style': 'width:370px'}), required=False)
    mobile = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': '请输入电话'}), error_messages={'required': '请输入电话'})
    emergency_name = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': '请输入紧急联系人'}), required=False)
    emergency_mobile = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': '请输入紧急联系人电话'}), required=False)

    def clean_id_no(self):
        if len(self.cleaned_data['id_no']) != 18:
            raise forms.ValidationError("身份证输入错误")
        elif EmployeeProfile.objects.filter(id_no=self.cleaned_data['id_no'], is_fired=False).exists():
            raise forms.ValidationError("身份证号已存在")
        return self.cleaned_data['id_no']

    def clean_serial_id(self):
        if EmployeeProfile.objects.filter(serial_id=self.cleaned_data['serial_id']).exists():
            raise forms.ValidationError("序列号已存在")
        return self.cleaned_data['serial_id']

    def clean_birth(self):
        if not self.cleaned_data['birth']:
            raise forms.ValidationError("请输入出生日期")
        return self.cleaned_data['birth']

    def clean(self):
        return self.cleaned_data

    def save(self, request, commit=True):
        m = super(EmployeeProfileForm, self).save(commit=False)
        sex = request.POST.get('sex', '男')
        edu_level = request.POST.get('edu_level', '无')
        residence_type = request.POST.get('residence_type', '城市户口')
        is_fired = request.POST.get('is_fired', '0')
        m.sex = sex
        m.edu_level = edu_level
        m.residence_type = residence_type
        m.is_fired = int(is_fired)
        m.save(request)
        return m


class ContractForm(forms.ModelForm):
    """ 员工合同表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = Contract
        exclude = ['user']


class CompanyForm(forms.ModelForm):
    """ 公司添加表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = CompanyProfile
        exclude = ['name', 'address', 'link_man', 'link_man_mobile']

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入用户名', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '请输入密码', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入密码'})
    confirm_pwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '请再次输入', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请再次输入'})
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入公司名称', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入公司名称'})
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入公司地址', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入公司地址'})
    link_man = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入联系人', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入联系人'})
    link_man_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入联系人电话', 'class': 'txt_input', 'style': "margin-left:20px;width:205px;"}), error_messages={'required': '请输入联系人电话'})
   
    def save(self, request, commit=True):
        m = super(CompanyForm, self).save(commit=False)
        user = User()


