#!/usr/bin/python
# -*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from labour.models import EmployeeProfile

class EmployeeProfileForm(forms.ModelForm):
    """ 公司员工信息表单"""
    def __init__(self, request=None, *args, **kwargs):
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = EmployeeProfile
        fields = ('serial_id', 'name', 'sex')
        exclude = ['get_pwd_code']

    SEX_TYPE_CHOICES = (
        ('1', '男'),
        ('2', '女')
    )


    serial_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '请输入序列号'}), error_messages={'required': '请输入序列号'})
    name = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': '请输入姓名'}), error_messages={'required': '请输入姓名'})
    sex = forms.ChoiceField(choices=SEX_TYPE_CHOICES, widget=forms.RadioSelect(), initial=SEX_TYPE_CHOICES[0][0])
"""
    nation = models.CharField('民族', max_length=10, default=None, null=True)
    birth = models.DateTimeField('出生日期', default=None, null=True)
    id_no = models.DateTimeField('身份证号', default=None, null=True)

    edu_level = models.CharField('文化程度', max_length=10, default=None, null=True)
    graduate = models.CharField('毕业院校', max_length=20, default=None, null=True)
    profession = models.CharField('专业', max_length=20, default=None, null=True)
    residence_type = models.CharField('户口类型', max_length=20, default=None, null=True)
    residence_place = models.CharField('户籍行政区', max_length=100, default=None, null=True)
    now_address = models.CharField('先住址', max_length=100, default=None, null=True)
    mobile = models.CharField('电话', max_length=15, default=None, null=True)
    emergency_name = models.CharField('紧急联系人', max_length=15, default=None, null=True)
    emergency_mobile = models.CharField('紧急联系人电话', max_length=15, default=None, null=True)

    job_type = models.CharField('工种', max_length=15, default=None, null=True)
    is_fired = models.BooleanField('是否解除劳动关系', default=False, blank=True)
    fired_date = models.DateTimeField('解除时间', default=None, null=True)
    fired_reason = models.DateTimeField('解除原因', default=None, null=True)

    realname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入您的真实姓名', 'class': 'form-control pull-left'}), error_messages={'required': '请输入您的真实姓名'})
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': '请填写您常用的邮箱', 'class': 'form-control pull-left'}), error_messages={'required': '请填写您常用的邮箱'})
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入您的手机号码', 'class': 'form-control pull-left'}), error_messages={'required': '请输入您的手机号码'})
    """
