from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    url(r'location/(?P<lat>(\d+\.\d+))/(?P<lon>(\d+\.\d+))$', views.store_location, name='store_location'),
]
