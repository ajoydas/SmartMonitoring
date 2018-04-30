from django.http import HttpResponse
from django.shortcuts import render

from api.models import Position


def store_location(request, tracker, lat, lon):
    position = Position(tracker=tracker, lat=lat, lon=lon)
    position.save()
    return HttpResponse("tracker:"+str(tracker)+" lat:"+str(lat)+" lon:"+str(lon))


def validate_password(request, tracker, password):
    if int(tracker) == 12 and int(password) == 234:
        return HttpResponse("success")
    return HttpResponse("error")