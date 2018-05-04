from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from api.models import Tracker
from view.forms import TrackerForm
from django.contrib import messages


def home(request):
    print("In home view")
    trackers = Tracker.objects.filter()
    return render(request, 'view/home.html', {"trackers": trackers})


def show_map(request):
    from gmplot import gmplot

    # Place map
    gmap = gmplot.GoogleMapPlotter(23.4348, 90.236, 13)
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

    # Polygon
    # golden_gate_park_lats, golden_gate_park_lons = zip(*[
    #     (23.4348, 90.236),
    #     (23.5348, 90.236),
    #     (23.6348, 90.236),
    #     (23.7348, 90.236),
    #     (23.8348, 90.236),
    #
    # ])
    lats = [23.4348, 23.5348, 23.6348, 23.7348, 23.8348]
    lons = [90.236, 90.236, 90.236, 90.236, 90.236]
    gmap.plot(lats, lons, 'cornflowerblue', edge_width=10)

    # # Scatter points
    # top_attraction_lats, top_attraction_lons = zip(*[
    #     (23.4348, 90.236),
    #     (23.5348, 90.236),
    #     (23.6348, 90.236),
    #     (23.7348, 90.236),
    #     (23.8348, 90.236)
    # ])
    # gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=60, marker=True)

    # # Marker
    hidden_gem_lat, hidden_gem_lon = 23.4348, 90.236
    for i in range(0, 5):
        gmap.marker(lats[i], lons[i], '#FF0000', title="New marker")

    # Draw
    gmap.draw("media/map.html")
    return render(request, 'view/show_map.html')


def tracker_add(request):
    if request.method == 'POST':
        print("Tracker form submitted")
        form = TrackerForm(request.POST)
        if form.is_valid():
            print("Tracker form validated")
            tracker = Tracker()
            tracker.module_id = form.cleaned_data.get('module_id')
            tracker.lat = form.cleaned_data.get('lat')
            tracker.lon = form.cleaned_data.get('lon')
            tracker.password = form.cleaned_data.get('password')
            tracker.tracked = form.cleaned_data.get('tracked')
            tracker.locked = form.cleaned_data.get('locked')
            tracker.contact_num = form.cleaned_data.get('contact_num')
            tracker.save()
            messages.success(request, 'The tracker is saved successfully.')
        else:
            messages.error(request, 'Submitted form is not valid. Please try again.')
    else:
        form = TrackerForm()
    return render(request, 'view/tracker_add.html', {'form': form})


def tracker_view(request, tracker_id):
    tracker = get_object_or_404(Tracker, id=tracker_id)
    mapfile = tracker.gen_map()
    return render(request, 'view/tracker_view.html', {'mapfile': mapfile, "tracker": tracker})


def tracker_edit(request, tracker_id):
    print("In tracker edit")
    tracker = get_object_or_404(Tracker, id=tracker_id)
    if request.method == 'POST':
        print("Tracker form submitted")
        form = TrackerForm(request.POST, instance=tracker)
        if form.is_valid():
            print("Tracker form validated")
            tracker.module_id = form.cleaned_data.get('module_id')
            tracker.lat = form.cleaned_data.get('lat')
            tracker.lon = form.cleaned_data.get('lon')
            tracker.password = form.cleaned_data.get('password')
            tracker.tracked = form.cleaned_data.get('tracked')
            tracker.locked = form.cleaned_data.get('locked')
            tracker.contact_num = form.cleaned_data.get('contact_num')
            tracker.save()
            messages.success(request, 'The tracker is saved successfully.')
        else:
            messages.error(request, 'Submitted form is not valid. Please try again.')
    else:
        form = TrackerForm(instance=tracker, initial={
            'module_id': tracker.module_id,
            'lat': tracker.lat,
            'lon': tracker.lon,
            'password': tracker.password,
            'tracked': tracker.tracked,
            'locked': tracker.locked,
            'contact_num': tracker.contact_num
        })
    return render(request, 'view/tracker_edit.html', {'form': form, "tracker": tracker})


def tracker_delete(request, tracker_id):
    tracker = get_object_or_404(Tracker, id=tracker_id)
    tracker.delete()
    messages.success(request, 'The tracker has been removed successfully.')
    return redirect('view:home')


def add_contacts(request):
    return None


def gen_pass(request):
    if request.method == 'POST':
        keys = request.POST.keys()
        print(keys)
        for key in keys:
            try:
                if int(key):
                    print(key + " " + request.POST[key])
                    tracker = get_object_or_404(Tracker, id=key)

                    if request.POST[key] == 'selected':
                        tracker.gen_password()
                        messages.success(request, "Password Generated Successfully for tracker: "
                                         + str(tracker.module_id))

                else:
                    messages.error(request, "Password Generated Failed for tracker: "+ str(key))

            except Exception:
                None

    trackers = Tracker.objects.filter()
    return render(request, 'view/passwords_gen.html', {"trackers": trackers})


def send_pass(request):
    if request.method == 'POST':
        keys = request.POST.keys()
        print(keys)
        for key in keys:
            try:
                if int(key):
                    print(key + " " + request.POST[key])
                    tracker = get_object_or_404(Tracker, id=key)

                    if request.POST[key] == 'selected':
                        tracker.gen_password()
                        messages.success(request, "Password Sent Successfully for tracker: "
                                         + str(tracker.module_id))

                else:
                    messages.error(request, "Password Send Failed for tracker: "+ str(key))

            except Exception:
                None

    trackers = Tracker.objects.filter()
    return render(request, 'view/passwords_gen.html', {"trackers": trackers})
