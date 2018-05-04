from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from view import views

app_name = 'view'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'map/$', views.show_map, name='show_map'),
    url(r'tracker/add$', views.tracker_add, name='tracker_add'),
    url(r'tracker/(?P<module_id>(\d+))/view$', views.tracker_view, name='tracker_view'),
    url(r'tracker/(?P<module_id>(\d+))/edit$', views.tracker_edit, name='tracker_edit'),
    url(r'tracker/(?P<module_id>(\d+))/delete', views.tracker_delete, name='tracker_delete'),
    url(r'add_contacts/$', views.add_contacts, name='add_contacts'),
    url(r'gen_pass/$', views.gen_pass, name='gen_pass'),
    url(r'send_pass/$', views.send_pass, name='send_pass'),
]
