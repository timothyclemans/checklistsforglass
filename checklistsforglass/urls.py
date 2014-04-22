from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from .views import AuthComplete, LoginError
urlpatterns = patterns('',
    # Examples:

    url(r'^$', 'checklistsforglass.views.home', name='home'),
    url(r'^edit_checklist/(?P<checklist_id>\d+)/$', 'checklistsforglass.views.edit_checklist', name='edit_checklist'),
    url(r'^audit_trail/(?P<data_id>\d+)/$', 'checklistsforglass.views.audit_trail', name='audit_trail'),
    url(r'^audit_trails/$', 'checklistsforglass.views.audit_trails', name='audit_trails'),
    url(r'^delete_checklist/(?P<checklist_id>\d+)/$', 'checklistsforglass.views.delete_checklist', name='delete_checklist'),
    url(r'^delete_checklistV2/(?P<checklist_id>\d+)/$', 'checklistsforglass.views.delete_checklistV2', name='delete_checklistV2'),
    url(r'^create_checklist/$', 'checklistsforglass.views.create_checklist', name='create_checklist'),
    url(r'^edit_checklistV2/(?P<checklist_id>\d+)/$', 'checklistsforglass.views.edit_checklistV2', name='edit_checklistV2'),
    url(r'^export/$', 'checklistsforglass.views.export', name='export'),
    url(r'^create_checklistV2/$', 'checklistsforglass.views.create_checklistV2', name='create_checklistV2'),
    url(r'^edit_checklistV2/(?P<checklist_id>\d+)/save_image/$', 'checklistsforglass.views.save_image', name='save_image'),
    # url(r'^checklistsforglass/', include('checklistsforglass.foo.urls')),
    url(r'^is_registered/(?P<serial_number>[\w\d]+)/$', 'checklistsforglass.views.is_registered'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^install/$', 'checklistsforglass.views.install'),
    url(r'^unregistered_devices/$', 'checklistsforglass.views.unregistered_devices'),
    url(r'^register_device/(?P<serial_number>[\w\d]+)/$', 'checklistsforglass.views.register_device'),
    url(r'^get_users_checklists/(?P<user_id>\d+)/$', 'checklistsforglass.views.get_users_checklists'),
    url(r'^get_all_checklists/$', 'checklistsforglass.views.get_all_checklists'),
    url(r'^get_checklists/(?P<serial_number>[\w\d]+)/$', 'checklistsforglass.views.get_checklists'),
    url(r'^get_full_json/$', 'checklistsforglass.views.get_full_json'),
    url(r'^get_full_checklist/(?P<checklist_id>\d+)/$', 'checklistsforglass.views.get_full_checklist'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^save_data/$', 'checklistsforglass.views.save_data'),
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^login-error/$', LoginError.as_view()),
    url(r'', include('social_auth.urls')),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
