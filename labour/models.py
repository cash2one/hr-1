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


class Company(SoftDeletionModel):
    """ 公司信息"""
    pass


class UserProfile(SoftDeletionModel):
    """ 用户基本信息"""
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    serial_id = models.CharField('序号', max_length=20)
    name = models.CharField('姓名', max_length=10)
    sex = models.CharField('性别', max_length=2)
    nation = models.CharField('民族', max_length=10, default=None, null=True)
    birth = models.DatetimeField('出生日期', default=None, null=True)
    id_no = models.DatetimeField('身份证号', default=None, null=True)

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
    fired_date = models.DatetimeField('解除时间', default=None, null=True)
    fired_reason = models.DatetimeField('解除原因', default=None, null=True)

    def __unicode__(self):
        return self.name


class 
