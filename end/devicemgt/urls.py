from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *
from appdata import *

from django.conf.urls.static import static

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
    url(r'^app/meter/$', app_meter),

    url(r'^app/avatar/$', app_avatar),

    url(r'^app/login/$', app_login),
    url(r'^app/password/$', app_password),
    url(r'^app/userinfo/$', app_userinfo),
    url(r'^app/userinfo/submit/$', app_userinfo_submit),
    url(r'^app/score/$', app_score),
    url(r'^app/score/rank/$', app_score_rank),

    url(r'^app/checkinfo/$', app_checkinfo),
    url(r'^app/check/$', app_check),

    url(r'^app/maintain/list/1/$', app_maintain_list_1),
    url(r'^app/maintain/list/2/$', app_maintain_list_2),
    url(r'^app/maintain/add/$', app_maintain_add),
    url(r'^app/maintain/image/$', app_maintain_image),
    url(r'^app/maintain/confirm/$', app_maintain_confirm),
    url(r'^app/maintain/update/$', app_maintain_update),
    url(r'^app/maintain/submit/$', app_maintain_submit),

    url(r'^app/task/list/$', app_task_list),
    url(r'^app/task/confirm/$', app_task_confirm),
    url(r'^app/task/update/$', app_task_update),
    url(r'^app/task/submit/$', app_task_submit),

    url(r'^app/feedback/$', app_feedback),
    url(r'^app/egg/$', app_egg),
    url(r'^app/egg/time/$', app_egg_time),
    url(r'^app/egg/info/$', app_egg_info),
    url(r'^app/version/$', app_version),

    url(r'^app/device/brief/$', app_device_brief),
    url(r'^app/device/info/$', app_device_info),

    url(r'app/class/tree/$', app_class_tree),
    url(r'app/device/class/$', app_class_device_type_classified),

    url(r'app_test/$', app_test),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', index),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^register/$', register),
    url(r'^change_password/$', change_password),
    url(r'^change_avatar/$', change_avatar),
    url(r'^user/$', usermgt),
    url(r'^useradd/$', useradd),
    url(r'^userbatch_add/$', userbatch_add),
    url(r'^userbatch_submit/$', userbatch_submit),
    url(r'^user_operate/$', operate_user),
    url(r'^userdel/$', userdel),
    url(r'^userset/$', userset),
    url(r'^profile/$', profile),

    url(r'^device/$', devicemgt),
    url(r'^devicebyclass/$', devicebyclass),
    url(r'^deviceadd/$', deviceadd),
    url(r'^devicebatch_add/$', devicebatch_add),
    url(r'^devicebatch_submit/$', devicebatch_submit),
    url(r'^devicedel/$', devicedel),
    url(r'^device_type/$', device_type),
    url(r'^device_type_add/$', device_type_add),
    url(r'^device_type_submit/$', device_type_submit),
    url(r'^device_type_revise/$', device_type_revise),
    url(r'^device_type_del/$', device_type_del),
    url(r'^operate_device/$', operate_device),

    url(r'^supplier/$', supplier),
    url(r'^add_supplier/$', add_supplier),
    url(r'^del_supplier/$', del_supplier),
    url(r'^submit_supplier/$', submit_supplier),
    url(r'^producer/$', producer),
    url(r'^add_producer/$', add_producer),
    url(r'^del_producer/$', del_producer),
    url(r'^submit_producer/$', submit_producer),

    url(r'^setting/$', setting),
    url(r'^deviceall/$', deviceall),
    url(r'^purview/$', purview),
    url(r'^view_schedule/$', view_schedule),
    url(r'^add_schedule/$', add_schedule),
    url(r'^delete_schedule/$', delete_schedule),

    url(r'^view_role/$', view_role),
    url(r'^operate_role/$', operate_role),
    url(r'^submit_role/(\d*)/$', submit_role),
    url(r'^submit_role/$', submit_role),
    url(r'^delete_role/$', delete_role),

    url(r'^view_route/$', view_route),
    url(r'^operate_route/$', operate_route),
    url(r'^submit_route/(\d*)/$', submit_route),
    url(r'^submit_route/$', submit_route),
    url(r'^delete_route/$', delete_route),

    url(r'^view_form/$', view_form),
    url(r'^submit_form/$', submit_form),
    url(r'^delete_form/$', delete_form),

    url(r'^view_deviceplan/$', view_deviceplan),
    url(r'^submit_deviceplan/$', submit_deviceplan),
    url(r'^delete_deviceplan/$', delete_deviceplan),

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

    url(r'^view_spare/$', view_spare),
    url(r'^operate_spare/$', operate_spare),
    url(r'^submit_spare/$', submit_spare),
    url(r'^delete_spare/$', delete_spare),
    url(r'^view_sparebill/$', view_sparebill),
    url(r'^submit_sparebill/$', submit_sparebill),
    url(r'^delete_sparebill/$', delete_sparebill),
    url(r'^view_sparecount/$', view_sparecount),
    url(r'^submit_sparecount/$', submit_sparecount),
    url(r'^delete_sparecount/$', delete_sparecount),
    url(r'^sparebatch_add/$', sparebatch_add),
    url(r'^sparebatch_submit/$', sparebatch_submit),
    
    url(r'^view_tool/$', view_tool),
    url(r'^operate_tool/$', operate_tool),
    url(r'^submit_tool/$', submit_tool),
    url(r'^delete_tool/$', delete_tool),
    url(r'^view_tooluse/$', view_tooluse),
    url(r'^submit_tooluse/$', submit_tooluse),
    url(r'^delete_tooluse/$', delete_tooluse),
    url(r'^view_toolcount/$', view_toolcount),
    url(r'^submit_toolcount/$', submit_toolcount),
    url(r'^delete_toolcount/$', delete_toolcount),

    url(r'^department/$', department),
    url(r'^departmentadd/$', departmentadd),
    url(r'^department_submit/$', department_submit),
    url(r'^department_revise/$', department_revise),
    url(r'^department_del/$', department_del),

    url(r'^meter/$', meter),
    url(r'^meter_device/$', meter_device),
    url(r'^meter_date/$', meter_date),

    url(r'^score/$', score),
    url(r'^score/submit/$', score_submit),
     url(r'^score_history/$', score_history),
    url(r'^egg/$', egg),
    url(r'^egg/submit/$', egg_submit),
    url(r'^egg_history/$', egg_history),
    url(r'^receive_bonus/(\d*)/$', receive_bonus),
    url(r'^attendance_history/$', attendance_history)
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
