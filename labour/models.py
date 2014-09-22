#!/usr/local/python
# -*- coding:utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import User

class SoftDeletionModel(models.Model):
    DELETE_STATUS_CHOICES = (
        (0, '正常'),
        (1, '已删除')
    )
    is_deleted = models.BooleanField('是否已删除', choices=DELETE_STATUS_CHOICES, default=False, blank=True)
    deleted = models.DateTimeField('删除时间', default=None, null=True)
    created = models.DateTimeField('创建时间', default=datetime.datetime.now())
    updated = models.DateTimeField('更新时间', default=datetime.datetime.now()) 

    class Meta:
        abstract = True 

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        return super(SoftDeletionModel, self).save(*args, **kwargs)

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


class UserProfile(SoftDeletionModel):
    """ 用户基本信息"""
    ADMIN = 0
    COMPANY = 1

    LEVEL_CHOICES = (
        (ADMIN, '管理员'),
        (COMPANY, '公司'),
    )

    user = models.OneToOneField(User, related_name='account')
    level = models.IntegerField('用户权限', choices=LEVEL_CHOICES, default=0)


class CompanyProfile(SoftDeletionModel):
    """ 公司信息"""
    profile = models.OneToOneField(UserProfile, related_name='profile')
    name = models.CharField('公司姓名', max_length=30)
    address = models.CharField('公司地址', max_length=50)
    link_man = models.CharField('联系人', max_length=20)
    link_man_mobile = models.CharField('联系人电话', max_length=20)


class EmployeeProfile(SoftDeletionModel):
    """ 员工基本信息"""
    company = models.ForeignKey(CompanyProfile, default=None, null=True)
    serial_id = models.CharField('序号', max_length=20)
    name = models.CharField('姓名', max_length=10)
    sex = models.CharField('性别', max_length=2)
    nation = models.CharField('民族', max_length=10, default=None, null=True, blank=True)
    birth = models.DateTimeField('出生日期', default=None, null=True, blank=True)
    id_no = models.CharField('身份证号', max_length=18)

    edu_level = models.CharField('文化程度', max_length=20, default=None, null=True, blank=True)
    graduate = models.CharField('毕业院校', max_length=20, default=None, null=True, blank=True)
    profession = models.CharField('专业', max_length=20, default=None, null=True, blank=True)
    residence_type = models.CharField('户口类型', max_length=20, default=None, null=True, blank=True)
    residence_place = models.CharField('户籍行政区', max_length=100, default=None, null=True, blank=True)
    now_address = models.CharField('先住址', max_length=100, default=None, null=True, blank=True)
    mobile = models.CharField('电话', max_length=15, default=None, null=True, blank=True)
    emergency_name = models.CharField('紧急联系人', max_length=15, default=None, null=True, blank=True)
    emergency_mobile = models.CharField('紧急联系人电话', max_length=15, default=None, null=True, blank=True)

    job_type = models.CharField('工种', max_length=15, default=None, null=True, blank=True)
    is_fired = models.BooleanField('是否解除劳动关系', default=False, blank=True)
    fired_date = models.DateTimeField('解除时间', default=None, null=True, blank=True)
    fired_reason = models.DateTimeField('解除原因', default=None, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Contract(SoftDeletionModel):
    """ 员工合同信息"""
    user = models.ForeignKey(EmployeeProfile, related_name='contract')
    company_protocal_start = models.DateTimeField('单位协议开始时间', default=None, null=True)
    company_protocal_end = models.DateTimeField('单位协议结束时间', default=None, null=True)
    labour_contract_start = models.DateTimeField('劳动合同开始时间', default=None, null=True)
    labour_contract_end = models.DateTimeField('劳动合同结束时间', default=None, null=True)
    probation_start = models.DateTimeField('试用期开始时间', default=None, null=True)
    probation_end = models.DateTimeField('试用期结束时间', default=None, null=True)
    bank_no = models.CharField('银行卡号', max_length=20)
    month_salary = models.CharField('实发工资', max_length=10)
    real_salary = models.CharField('实发工资', max_length=10)
    service_pay = models.CharField('服务费', max_length=10)
    salary_provide = models.DateTimeField('工资发放时间', default=None, null=True)

