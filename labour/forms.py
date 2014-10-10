#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import random

from django import forms
from django.contrib.auth.models import User

from labour.models import EmployeeProfile, Contract, CompanyProfile

IMPORT_FILE_TYPES = ['.xls', ]

class EmployeeProfileForm(forms.ModelForm):
    """ 公司员工信息表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = EmployeeProfile
        fields = ['birth', 'email', 'id_no','name', 'nation', 'graduate', 'profession', \
            'residence_type', 'residence_place', 'now_address', 'mobile', 'emergency_name',\
            'emergency_mobile', 'sex', 'edu_level', 'is_fired']

    #serial_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '请输入序列号'}), error_messages={'required': '请输入序列号'})
    name = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': '请输入姓名'}), error_messages={'required': '请输入姓名'})
    email = forms.EmailField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '请输入邮箱'}), error_messages={'required': '请输入邮箱'})
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
        return self.cleaned_data['id_no']

    #def clean_serial_id(self):
    #    if EmployeeProfile.objects.filter(serial_id=self.cleaned_data['serial_id']).exclude(id=self.instance.id).exists():
    #        raise forms.ValidationError("序列号已存在")
    #    return self.cleaned_data['serial_id']

    def clean_birth(self):
        if not self.cleaned_data['birth']:
            raise forms.ValidationError("请输入出生日期")
        return self.cleaned_data['birth']

    def clean(self):
        print self.errors
        return self.cleaned_data

    def save(self, request, commit=True):
        m = super(EmployeeProfileForm, self).save(commit=False)
        print m.serial_id
        if m.serial_id is None or len(str(m.serial_id)) == 0:
            count = EmployeeProfile.objects.all().count()
            if count == 0:
                m.serial_id = random.randint(100000, 900000)
            else:
                employee_last = EmployeeProfile.objects.all().order_by('-created')[0]
                m.serial_id = str(int(employee_last.serial_id) + 1)
        fired_date = request.POST.get("fired_date")
        fired_reason = request.POST.get("fired_reason")
        is_fired = request.POST.get('is_fired')
        m.is_fired = int(is_fired)
        m.fired_date = fired_date
        m.fired_reason = fired_reason
        m.save()
        return m


class ContractForm(forms.ModelForm):
    """ 员工合同表单"""
    def __init__(self, request=None, employee=None, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self._request = request
        self._employee = employee

    class Meta:
        model = Contract
        exclude = ['employee','created', 'updated', 'deleted']

    job_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入工种类型', 'class': 'txt', 'style': "margin-left:28px;width:205px;"}),
            error_messages={'required': '请输入工种类型'})
    company_protocal_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入单位协议开始时间', 'class': 'txt calendar', 'id': 'startDate1', 'style': "margin-left:28px;width:205px;margin-top:10px;"}),
            error_messages={'required': '请输入单位协议开始时间'})
    company_protocal_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入单位协议结束时间', 'class': 'txt calendar','id': 'startDate2', 'style': "margin-left:28px;width:205px;margin-top:10px;"}),
            error_messages={'required': '请输入单位协议结束时间'})
    labour_contract_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入劳动合同开始时间', 'class': 'txt calendar','id': 'startDate3', 'style': "margin-left:28px;width:205px;margin-top:10px;"}),
            error_messages={'required': '请输入劳动合同开始时间'})
    labour_contract_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入劳动合同结束时间', 'class': 'txt calendar','id': 'startDate4', 'style': "margin-left:28px;width:205px;margin-top:10px;"}),
            error_messages={'required': '请输入劳动合同结束时间'})
    probation_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入实习开始时间', 'class': 'txt calendar','id': 'startDate5', 'style': "margin-left:28px;width:205px;margin-top:10px;"}),
            error_messages={'required': '请输入实习开始时间'})
    probation_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入实习结束时间', 'class': 'txt calendar','id': 'startDate6', 'style': "margin-left:28px;width:205px;margin-top:10px;"}),
            error_messages={'required': '请输入实习结束时间'})
    bank_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入银行卡号', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;margin-top:px;"}),
            error_messages={'required': '请输入银行卡号'})
    month_salary = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入月工资', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;margin-top:-1px;"}),
            error_messages={'required': '请输入月工资'})
    real_salary = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入实际工资', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;margin-top:-1px;"}),
            error_messages={'required': '请输入实际工资'})
    salary_provide = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入工资发放时间', 'class': 'txt calendar','id': 'startDate7', 'style': "margin-left:28px;width:205px;margin-top:10px;"}),
            error_messages={'required': '请输入工资发放时间'})

    def clean_bank_no(self):
        try:
            float(self.cleaned_data['bank_no'])
        except ValueError:
            raise forms.ValidationError("请输入正确的银行卡")
        return self.cleaned_data['bank_no']

    def clean_month_salary(self):
        try:
            float(self.cleaned_data['month_salary'])
        except ValueError:
            raise forms.ValidationError("请输入正确的月工资")
        return self.cleaned_data['month_salary']

    def clean_real_salary(self):
        try:
            int(self.cleaned_data['real_salary'])
        except ValueError:
            raise forms.ValidationError("请输入正确的实际工资")
        return self.cleaned_data['real_salary']

    def clean(self):
        if self.errors:
            return self.cleaned_data
        if self.cleaned_data['company_protocal_start'] > self.cleaned_data['company_protocal_end']:
            raise forms.ValidationError('协议开始时间大于结束时间')
        if self.cleaned_data['labour_contract_start'] > self.cleaned_data['labour_contract_end']:
            raise forms.ValidationError('劳动合同开始时间大于结束时间')
        if self.cleaned_data['probation_start'] > self.cleaned_data['probation_end']:
            raise forms.ValidationError('实习开始时间大于结束时间')
        return self.cleaned_data

    def save(self, request=None, employee=None, commit=True):
        if employee:
            c = super(ContractForm, self).save(commit=False)
            c.employee = employee
            company = CompanyProfile.objects.get(id=request.POST['company'])
            employee.company = company
            employee.save()
            c.save()
            return c
        else:
            super(ContractForm, self).save(commit=True)


class CompanyForm(forms.ModelForm):
    """ 公司添加表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = CompanyProfile
        fields = ['name', 'address', 'email', 'link_man', 'link_man_mobile', 'service_cost']

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入公司名称', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入公司名称'})
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': '请输入公司邮箱', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入公司邮箱'})
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入公司地址', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入公司地址'})
    link_man = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入联系人', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入联系人'})
    link_man_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入联系人电话', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入联系人电话'})
    service_cost = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入服务费', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}), error_messages={'required': '请输入服务费'})
   
    def clean_name(self):
        if CompanyProfile.objects.filter(name=self.cleaned_data['name']).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("公司已存在")
        return self.cleaned_data['name']

    def clean_link_man_mobile(self):
        try:
            int(self.cleaned_data['link_man_mobile'])
        except:
            raise forms.ValidationError('电话格式错误')
        return self.cleaned_data['link_man_mobile']

    def clean(self):
        return self.cleaned_data

    def clean_service_cost(self):
        try:
            int(self.cleaned_data['service_cost'])
        except:
            raise forms.ValidationError('服务费输入错误')
        return self.cleaned_data['service_cost']

class HealthForm(forms.ModelForm):
    """ 医疗保险表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(HealthForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = CompanyProfile
        fields = ['health_card', 'health_payment_base', 'health_payment_self', 'health_payment_company', 'health_payment_start', 'health_payment_end']

    health_card = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入卡号', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入卡号'})
    health_payment_base = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入缴费基数', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入缴费基数'})
    health_payment_self = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入个人缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入个人缴费金额'})
    health_payment_company = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入公司缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入公司缴费金额'})
    health_payment_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险起始时间', 'class': 'txt calendar', 'id':'startDate2', 'style': "margin-left:28px;width:205px;margin-top:3px"}),
        error_messages={'required': '请输入保险起始时间'})
    health_payment_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险终止时间', 'class': 'txt calendar', 'id':'startDate1', 'style': "margin-left:28px;width:205px;margin-top:10px"}),
        error_messages={'required': '请输入保险终止时间'})

    def clean_health_payment_base(self):
        try:
            int(self.cleaned_data['health_payment_base'])
        except KeyError:
            raise forms.ValidationError("缴费基数输入错误")
        return self.cleaned_data['health_payment_base']
    
    def clean_health_payment_self(self):
        try:
            int(self.cleaned_data['health_payment_self'])
        except KeyError:
            raise forms.ValidationError("个人缴费金额输入错误")
        return self.cleaned_data['health_payment_self']
    
    def clean_health_payment_company(self):
        try:
            int(self.cleaned_data['health_payment_company'])
        except KeyError:
            raise forms.ValidationError("公司缴费金额输入错误")
        return self.cleaned_data['health_payment_company']
   
    def clean(self):
        if self.errors:
            return self.cleaned_data
        if self.cleaned_data['health_payment_start'] > self.cleaned_data['health_payment_end']:
            raise forms.ValidationError("起始日期不能大于结束日期")
        return self.cleaned_data
   

class EndowmentForm(forms.ModelForm):
    """ 养老保险表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(EndowmentForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = CompanyProfile
        fields = ['endowment_card', 'endowment_payment_base', 'endowment_payment_self', 'endowment_payment_company', 'endowment_payment_start', 'endowment_payment_end']

    endowment_card = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入卡号', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入卡号'})
    endowment_payment_base = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入缴费基数', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入缴费基数', 'invalid': '缴费基数输入错误'})
    endowment_payment_self = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入个人缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入个人缴费金额', 'invalid': '个人缴费金额输入错误'})
    endowment_payment_company = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入公司缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入公司缴费金额', 'invalid': '公司缴费金额输入错误'})
    endowment_payment_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险起始时间', 'class': 'txt calendar', 'id':'startDate2', 'style': "margin-left:28px;width:205px;margin-top:3px"}),
        error_messages={'required': '请输入保险起始时间'})
    endowment_payment_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险终止时间', 'class': 'txt calendar', 'id':'startDate1', 'style': "margin-left:28px;width:205px;margin-top:10px"}),
        error_messages={'required': '请输入保险终止时间'})
   
    def clean(self):
        if self.errors:
            return self.cleaned_data
        if self.cleaned_data['endowment_payment_start'] > self.cleaned_data['endowment_payment_end']:
            raise forms.ValidationError("起始日期不能大于结束日期")
        return self.cleaned_data
   

class BornForm(forms.ModelForm):
    """ 生育保险表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(BornForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = CompanyProfile
        fields = ['born_payment_base', 'born_payment_self', 'born_payment_company', 'born_payment_start', 'born_payment_end']

    born_payment_base = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入缴费基数', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入缴费基数', 'invalid': '缴费基数输入错误'})
    born_payment_self = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入个人缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入个人缴费金额', 'invalid': '个人缴费金额输入错误'})
    born_payment_company = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入公司缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入公司缴费金额', 'invalid': '公司缴费金额输入错误'})
    born_payment_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险起始时间', 'class': 'txt calendar', 'id':'startDate2', 'style': "margin-left:28px;width:205px;margin-top:3px"}),
        error_messages={'required': '请输入保险起始时间'})
    born_payment_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险终止时间', 'class': 'txt calendar', 'id':'startDate1', 'style': "margin-left:28px;width:205px;margin-top:10px"}),
        error_messages={'required': '请输入保险终止时间'})

    def clean(self):
        if self.errors:
            return self.cleaned_data
        if self.cleaned_data['born_payment_start'] > self.cleaned_data['born_payment_end']:
            raise forms.ValidationError("起始日期不能大于结束日期")
        return self.cleaned_data


class IndustrialForm(forms.ModelForm):
    """ 工伤保险表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(IndustrialForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = CompanyProfile
        fields = ['industrial_payment_base', 'industrial_payment_self', 'industrial_payment_company', 'industrial_payment_start', 'industrial_payment_end']

    industrial_payment_base = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入缴费基数', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入缴费基数', 'invalid': '缴费基数输入错误'})
    industrial_payment_self = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入个人缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入个人缴费金额', 'invalid': '个人缴费金额输入错误'})
    industrial_payment_company = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入公司缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入公司缴费金额', 'invalid': '公司缴费金额输入错误'})
    industrial_payment_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险起始时间', 'class': 'txt calendar', 'id':'startDate2', 'style': "margin-left:28px;width:205px;margin-top:3px"}),
        error_messages={'required': '请输入保险起始时间'})
    industrial_payment_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险终止时间', 'class': 'txt calendar', 'id':'startDate1', 'style': "margin-left:28px;width:205px;margin-top:10px"}),
        error_messages={'required': '请输入保险终止时间'})
   
    def clean(self):
        if self.errors:
            return self.cleaned_data
        if self.cleaned_data['industrial_payment_start'] > self.cleaned_data['industrial_payment_end']:
            raise forms.ValidationError("起始日期不能大于结束日期")
        return self.cleaned_data
  

class UnemployeedForm(forms.ModelForm):
    """ 失业保险表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(UnemployeedForm, self).__init__(*args, **kwargs)
        self._request = request
        
    class Meta:
        model = CompanyProfile
        fields = ['unemployed_payment_base', 'unemployed_payment_self', 'unemployed_payment_company', 'unemployed_payment_start', 'unemployed_payment_end']

    unemployed_payment_base = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入缴费基数', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入缴费基数', 'invalid': '缴费基数输入错误'})
    unemployed_payment_self = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入个人缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入个人缴费金额', 'invalid': '个人缴费金额输入错误'})
    unemployed_payment_company = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入公司缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入公司缴费金额', 'invalid': '公司缴费金额输入错误'})
    unemployed_payment_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险起始时间', 'class': 'txt calendar', 'id':'startDate2', 'style': "margin-left:28px;width:205px;margin-top:3px"}),
        error_messages={'required': '请输入保险起始时间'})
    unemployed_payment_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入保险终止时间', 'class': 'txt calendar', 'id':'startDate1', 'style': "margin-left:28px;width:205px;margin-top:10px"}),
        error_messages={'required': '请输入保险终止时间'})

    def clean(self):
        if self.errors:
            return self.cleaned_data
        if self.cleaned_data['unemployed_payment_start'] > self.cleaned_data['unemployed_payment_end']:
            raise forms.ValidationError("起始日期不能大于结束日期")
        return self.cleaned_data
  

class ReservedForm(forms.ModelForm):
    """ 公积金表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(ReservedForm, self).__init__(*args, **kwargs)
        self._request = request
        
    class Meta:
        model = CompanyProfile
        fields = ['reserved_payment_base', 'reserved_payment_self', 'reserved_payment_company', 'reserved_payment_start', 'reserved_payment_end']

    reserved_payment_base = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入缴费基数', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入缴费基数', 'invalid': '缴费基数输入错误'})
    reserved_payment_self = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入个人缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入个人缴费金额', 'invalid': '个人缴费金额输入错误'})
    reserved_payment_company = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '请输入公司缴费金额', 'class': 'txt_input', 'style': "margin-left:28px;width:205px;"}),
        error_messages={'required': '请输入公司缴费金额', 'invalid': '公司缴费金额输入错误'})
    reserved_payment_start = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入起始时间', 'class': 'txt calendar', 'id':'startDate1', 'style': "margin-left:28px;width:205px;margin-top:3px"}),
        error_messages={'required': '请输入起始时间'})
    reserved_payment_end = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': '请输入终止时间', 'class': 'txt calendar', 'id':'startDate2', 'style': "margin-left:28px;width:205px;margin-top:10px"}),
        error_messages={'required': '请输入终止时间'})

    def clean(self):
        if self.errors:
            return self.cleaned_data
        if self.cleaned_data['reserved_payment_start'] > self.cleaned_data['reserved_payment_end']:
            raise forms.ValidationError("起始日期不能大于结束日期")
        return self.cleaned_data
  
class LabourImportForm(forms.Form):
    """ 职员信息批量插入"""
    labour_import = forms.FileField(required= True, label= u"Upload the Excel file to import to the system.")

    def clean_input_excel(self):
        input_excel = self.cleaned_data['labour_import']
        extension = os.path.splitext( input_excel.name )[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError("请输入正确的excel格式文件")
        else:
            return input_excel
