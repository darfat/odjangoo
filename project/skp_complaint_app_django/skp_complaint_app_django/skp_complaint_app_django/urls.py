from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skp_complaint_app_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^skpcomplaint/$', 'skpcomplaint.views.index'),
    url(r'^skpcomplaint/search/$', 'skpcomplaint.views.search'),
    url(r'^skpcomplaint/(?P<employee_id>\d+)/$', 'skpcomplaint.views.detail'),
    url(r'^skpcomplaint/(?P<employee_id>\d+)/results/$', 'skpcomplaint.views.results'),
    url(r'^skpcomplaint/(?P<employee_id>\d+)/propose/$', 'skpcomplaint.views.propose'),

)
