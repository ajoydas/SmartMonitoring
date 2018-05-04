from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from api.models import Tracker
from view.forms import TrackerForm


def home(request):
    print("In home view")
    trackers = Tracker.objects.filter()
    return render(request, 'view/home.html',{"trackers": trackers})


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
    for i in range(0,5):
        gmap.marker( lats[i], lons[i], '#FF0000',title="New marker")

    # Draw
    gmap.draw("media/map.html")
    return render(request, 'view/show_map.html')


def tracker_add(request):
    return None


def tracker_view(request, module_id):
    return None


def tracker_edit(request, module_id):
    print("In tracker edit")
    tracker = Tracker.objects.filter(module_id=module_id).get()
    if request.method == 'POST':
        print("Tracker form submitted")
        form = TrackerForm(request.POST)
    else:
        form = TrackerForm(instance=tracker, initial={
            'module_id' : tracker.module_id,
            'lat' : tracker.lat,
            'lon': tracker.lon,
            'password': tracker.password,
            'tracked': tracker.tracked,
            'locked' : tracker.locked,
            'contact_num' :tracker.contact_num
        })
    return render(request, 'view/tracker_edit.html', {'form': form, "tracker": tracker})


def tracker_delete(request, module_id):
    return None


def add_contacts(request):
    return None


def gen_pass(request):
    return None


def send_pass(request):
    return None
