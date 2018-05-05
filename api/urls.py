from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    url(r'location/(?P<tracker>(\d+))/(?P<lat>(\d+\.\d+))/(?P<lon>(\d+\.\d+))$', views.store_location,
        name='store_location'),
    url(r'validate/(?P<tracker>(\d+))/(?P<lat>(\d+\.\d+))/(?P<lon>(\d+\.\d+))/(?P<password>(\d+))$', views.validate_password, name='validate_password'),
    url(r'seed/$', views.seed, name='seed'),
    url(r'clear/$', views.clear, name='clear'),
]
