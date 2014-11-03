#!/usr/local/python
# -*- coding:utf-8 -*-

import datetime
import xlwt
import xlrd
import random
import time

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


from labour.forms import EmployeeProfileForm, ContractForm, CompanyForm
from labour.models import EmployeeProfile, UserProfile, CompanyProfile, Contract
from labour.forms import HealthForm, BornForm, UnemployeedForm, ReservedForm
from labour.forms import LabourImportForm, IndustrialForm, EndowmentForm
from utils import adjacent_paginator

from django.shortcuts import render

def property(request, template_name='labour/company_property.html'):
    """ 企业资金管理"""
    company_list = CompanyProfile.objects.all()

    companys, page_numbers = adjacent_paginator(company_list, request.GET.get('page', 1))

    return render(request, template_name, {
        'companys': companys,
        'page_numbers': page_numbers,
    })


def property_detail(request, template_name='labour/company_property_detail.html'):
    """ 该公司资金详情"""
    return render(request, template_name)


def salary(request, template_name='labour/company_salary_search.html'):
    """ 个人工资搜索"""
    return render(request, template_name)

    