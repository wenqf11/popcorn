from django.conf.urls import patterns, include, url
from views import *
from appdata import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'devicemgt.views.home', name='home'),
    # url(r'^devicemgt/', include('devicemgt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^app/route/$', app_route),
    url(r'^app/form/$', app_form),
    url(r'^app/login/$', app_login),
    url(r'^app/password/$', app_password),
    url(r'app/userinfo/$', app_userinfo),
    url(r'app/score/$', app_score),

    url(r'app_test/$', app_test),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', index),
    url(r'^login/$', login),
    url(r'^register/$', register),
    url(r'^user/$', usermgt),
    url(r'^useradd/$', useradd),
    url(r'^user_operate/$', operate_user),
    url(r'^userdel/$', userdel),
    url(r'^userset/$', userset),
    url(r'^profile/$', profile),

    url(r'^device/$', devicemgt),
    url(r'^deviceadd/$', deviceadd),
    url(r'^device_type/$', device_type),
    url(r'^device_type_add/$', device_type_add),
    url(r'^operate_device/$', operate_device),

    url(r'^supplier/$', supplier),
    url(r'^add_supplier/$', add_supplier),
    url(r'^submit_supplier/$', submit_supplier),
    url(r'^producer/$', producer),
    url(r'^add_producer/$', add_producer),
    url(r'^submit_producer/$', submit_producer),

    url(r'^setting/$', setting),
    url(r'^spare/$', spare),
    url(r'^sparetype/$', sparetype),
    url(r'^sparebrand/$', sparebrand),
    url(r'^sparehist/$', sparehist),
    url(r'^deviceall/$', deviceall),
    url(r'^purview/$', purview),
    url(r'^schedule/$', schedule),
    url(r'^get_schedule/$', get_schedule),
    url(r'^save_schedule/$', save_schedule),

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

    url(r'^view_upkeeping/$', view_upkeeping),
    url(r'^view_upkeeped/$', view_upkeeped),
    url(r'^submit_upkeep/$', submit_upkeep),
    url(r'^delete_upkeep/$', delete_upkeep),

    url(r'^view_tasking/$', view_tasking),
    url(r'^view_tasked/$', view_tasked),
    url(r'^add_task/$', add_task),
    url(r'^submit_task/$', submit_task),
    url(r'^delete_task/$', delete_task),

    url(r'^view_taskitem/$', view_taskitem),
    url(r'^submit_taskitem/$', submit_taskitem),
    url(r'^delete_taskitem/$', delete_taskitem),

    url(r'^department/$', department),
    url(r'^score/$', score),
)
