from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^labour/', include('labour.urls')),
    url(r'^company/', include('company.urls')),
    url(r'^manager/', include('manager.urls')),

    url(r'^$', 'hr.views.test'),
    url(r'^login/$', 'hr.views.login'),
    url(r'^logout/', 'hr.views.logout'),
    url(r'^reset_pwd/', 'hr.views.reset_pwd'),
    url(r'^log/', 'hr.views.log'),

)
