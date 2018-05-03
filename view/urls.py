from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from view import views

urlpatterns = [
    url(r'map/$', views.show_map, name='show_map'),
]
