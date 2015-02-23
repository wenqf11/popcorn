from django.conf.urls import patterns, include, url
from views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'devicemgt.views.home', name='home'),
    # url(r'^devicemgt/', include('devicemgt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^login/$', login),
    url(r'^register/$', register),
    url(r'^user/$', usermgt),
    url(r'^device/$', devicemgt),
    url(r'^profile/$', profile),
    url(r'^front/$', front),
    url(r'^setting/$', setting),
    url(r'^unmain/$', unmain),
    url(r'^mainhist/$', mainhist),
    url(r'^spare/$', spare),
    url(r'^sparetype/$', sparetype),
    url(r'^sparebrand/$', sparebrand),
    url(r'^sparehist/$', sparehist),
)
