from django.http import HttpResponse
from django.shortcuts import render

from api.models import Position, Tracker, WarningEvent
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def store_location(request, tracker, lat, lon):
    position = Position(tracker=tracker, lat=lat, lon=lon)
    position.save()
    return HttpResponse("tracker:"+str(tracker)+" lat:"+str(lat)+" lon:"+str(lon))


@csrf_exempt
def validate_password(request, tracker, password):
    if int(tracker) == 12 and int(password) == 234:
        return HttpResponse("success")
    return HttpResponse("error")


def seed(request):
    # try:
        modules = [1,2,3,4,5]
        lats = [23.4348, 23.5348, 23.6348, 23.7348, 23.8348]
        lons = [90.236, 90.236, 90.236, 90.236, 90.236]
        passwords = ["11","12","13","14","15"]

        for i in range(0, len(modules)):
            tracker = Tracker(module_id=modules[i], lat=lats[i],lon=lons[i],password=passwords[i])
            tracker.save()

        trackers = Tracker.objects.filter()
        for i in range(0,len(modules)):
            for j in range(0,5):
                position = Position(tracker=trackers[i], lat= trackers[i].lat- j*0.1,
                                    lon= trackers[i].lon + j*0.1)
                position.save()
                print("i:"+str(i)+" j:"+str(j))

        positions = Position.objects.filter()
        for i in range(0, int(len(modules)/2)):
            position = Position.objects.filter(tracker=trackers[i*2])
            event = WarningEvent(position = position, password = position.tracker.password + str(i))
            event.save()

        return HttpResponse("Success")
    # except Exception as err:
    #     print(err)
    #     return HttpResponse("Failed")


def clear(request):
    try:
        Tracker.objects.filter().delete()
        Position.objects.filter().delete()
        WarningEvent.objects.filter().delete()
        return HttpResponse("Success")
    except:
        return HttpResponse("Failed")