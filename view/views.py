from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
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
    gmap.draw("media/my_map.html")
    return HttpResponse("Generated")