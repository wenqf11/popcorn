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
    url(r'^useradd/$', useradd),
    url(r'^user_operate/$', user_operate),
    url(r'^userdel/$', userdel),
    url(r'^userset/$', userset),
    url(r'^device/$', devicemgt),
    url(r'^deviceadd/$', deviceadd),
    url(r'^profile/$', profile),
    url(r'^setting/$', setting),
    url(r'^spare/$', spare),
    url(r'^sparetype/$', sparetype),
    url(r'^sparebrand/$', sparebrand),
    url(r'^sparehist/$', sparehist),
    url(r'^deviceall/$', deviceall),
    url(r'^purview/$', purview),
    url(r'^schedule/$', schedule),
    url(r'^view_role/$', view_role),
    url(r'^operate_role/$', operate_role),
    url(r'^submit_role/(\d*)/$', submit_role),
    url(r'^delete_role/$', delete_role),
    url(r'^view_route/$', view_route),
    url(r'^operate_route/$', operate_route),
    url(r'^submit_route/(\d*)/$', submit_route),
    url(r'^delete_route/$', delete_route),
    url(r'^view_form/$', view_form),
    url(r'^submit_form/$', submit_form),
    url(r'^delete_form/$', delete_form),
    url(r'^view_maintaining/$', view_maintaining),
    url(r'^view_maintained/$', view_maintained),
    url(r'^add_maintenance/$', add_maintenance),
    url(r'^submit_maintenance/$', submit_maintenance),
    url(r'^delete_maintenance/$', delete_maintenance),
    url(r'^department/$', department),
    url(r'^score/$', score),
)
