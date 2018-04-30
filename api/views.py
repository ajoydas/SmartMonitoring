from django.http import HttpResponse
from django.shortcuts import render


def store_location(request, lat, lon):
    return  HttpResponse("lat:"+str(lat)+" lon:"+str(lon))