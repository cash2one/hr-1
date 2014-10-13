from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'hr.views.login'),
    url(r'^labour/', include('labour.urls')),
    url(r'^logout/', 'hr.views.logout'),

)
