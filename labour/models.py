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
    profile = models.OneToOneField(UserProfile, related_name='profile', default=None, null=True)
    name = models.CharField('公司姓名', max_length=30)
    address = models.CharField('公司地址', max_length=50)
    link_man = models.CharField('联系人', max_length=20)
    link_man_mobile = models.CharField('联系人电话', max_length=20)
    service_cost = models.CharField('服务费', max_length=20)


class EmployeeProfile(SoftDeletionModel):
    """ 员工基本信息"""
    company = models.ForeignKey(CompanyProfile, default=None, null=True)
    serial_id = models.CharField('序号', max_length=20)
    name = models.CharField('姓名', max_length=10)
    email = models.EmailField('邮箱', max_length=20)
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

    is_fired = models.BooleanField('是否解除劳动关系', default=False, blank=True)
    fired_date = models.DateTimeField('解除时间', default=None, null=True, blank=True)
    fired_reason = models.CharField('解除原因', max_length=100, default=None, null=True, blank=True)

    #医疗保险
    health_card = models.CharField('医疗保险卡号', max_length=30, default=None, blank=True, null=True)
    health_payment_base = models.CharField('医疗保险缴费基数', max_length=10, default=None, blank=True, null=True)
    health_payment_self = models.CharField('医疗保险个人缴费', max_length=10, default=None, blank=True, null=True)
    health_payment_company = models.CharField('医疗保险公司缴费', max_length=10, default=None, blank=True, null=True)
    health_payment_start = models.DateTimeField('医疗保险缴费起始时间', default=None, null=True, blank=True)
    health_payment_end = models.DateTimeField('医疗保险缴费终止时间', default=None, null=True, blank=True)

    #养老保险
    endowment_card = models.CharField('养老保险卡号', max_length=30, default=None, blank=True, null=True)
    endowment_payment_base = models.CharField('养老保险缴费基数', max_length=10, default=None, blank=True, null=True)
    endowment_payment_self = models.CharField('养老保险个人缴费', max_length=10, default=None, blank=True, null=True)
    endowment_payment_company = models.CharField('养老保险公司缴费', max_length=10, default=None, blank=True, null=True)
    endowment_payment_start = models.DateTimeField('养老保险缴费起始时间', default=None, null=True, blank=True)
    endowment_payment_end = models.DateTimeField('养老保险缴费终止时间', default=None, null=True, blank=True)

    #生育保险
    born_payment_base = models.CharField('生育保险缴费基数', max_length=10, default=None, blank=True, null=True)
    born_payment_self = models.CharField('生育保险个人缴费', max_length=10, default=None, blank=True, null=True)
    born_payment_company = models.CharField('生育保险公司缴费', max_length=10, default=None, blank=True, null=True)
    born_payment_start = models.DateTimeField('生育保险缴费起始时间', default=None, null=True, blank=True)
    born_payment_end = models.DateTimeField('生育保险缴费终止时间', default=None, null=True, blank=True)

    #工伤保险
    industrial_payment_base = models.CharField('工伤保险缴费基数', max_length=10, default=None, blank=True, null=True)
    industrial_payment_self = models.CharField('工伤保险个人缴费', max_length=10, default=None, blank=True, null=True)
    industrial_payment_company = models.CharField('工伤保险公司缴费', max_length=10, default=None, blank=True, null=True)
    industrial_payment_start = models.DateTimeField('工伤保险缴费起始时间', default=None, null=True, blank=True)
    industrial_payment_end = models.DateTimeField('工伤保险缴费终止时间', default=None, null=True, blank=True)

    #失业保险
    unemployed_payment_base = models.CharField('失业保险缴费基数', max_length=10, default=None, blank=True, null=True)
    unemployed_payment_self = models.CharField('失业保险个人缴费', max_length=10, default=None, blank=True, null=True)
    unemployed_payment_company = models.CharField('失业保险公司缴费', max_length=10, default=None, blank=True, null=True)
    unemployed_payment_start = models.DateTimeField('失业保险缴费起始时间', default=None, null=True, blank=True)
    unemployed_payment_end = models.DateTimeField('失业保险缴费终止时间', default=None, null=True, blank=True)

    #公积金
    reserved_payment_base = models.CharField('公积金缴费基数', max_length=10, default=None, blank=True, null=True)
    reserved_payment_self = models.CharField('公积金个人缴费', max_length=10, default=None, blank=True, null=True)
    reserved_payment_company = models.CharField('公积金公司缴费', max_length=10, default=None, blank=True, null=True)
    reserved_payment_start = models.DateTimeField('公积金缴费起始时间', default=None, null=True, blank=True)
    reserved_payment_end = models.DateTimeField('公积金缴费终止时间', default=None, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Contract(SoftDeletionModel):
    """ 员工合同信息"""
    employee = models.OneToOneField(EmployeeProfile, related_name='contract')
    job_type = models.CharField('工种', max_length=15, default=None, null=True, blank=True)
    company_protocal_start = models.DateTimeField('单位协议开始时间', default=None, null=True)
    company_protocal_end = models.DateTimeField('单位协议结束时间', default=None, null=True)
    labour_contract_start = models.DateTimeField('劳动合同开始时间', default=None, null=True)
    labour_contract_end = models.DateTimeField('劳动合同结束时间', default=None, null=True)
    probation_start = models.DateTimeField('试用期开始时间', default=None, null=True)
    probation_end = models.DateTimeField('试用期结束时间', default=None, null=True)
    bank_no = models.CharField('银行卡号', max_length=20)
    month_salary = models.CharField('实发工资', max_length=10)
    real_salary = models.CharField('实发工资', max_length=10)
    salary_provide = models.DateTimeField('工资发放时间', default=None, null=True)

def ActionLog(SoftDeletionModel):
    """ 行为日志"""
    pass




















