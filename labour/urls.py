#!/usr/local/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('labour.views',

    url(r'^$', 'index'),
    
    #url(r'^(?P<folder>\D+)/info/(?P<recipe_id>\d+)/$', 'recipe_info'),

)
