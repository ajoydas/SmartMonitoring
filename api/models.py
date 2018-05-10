from datetime import datetime, timezone, timedelta
import random
import string

import numpy
import pandas
import pytz
from bs4 import BeautifulSoup
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from decouple import config
from django.conf import settings as django_settings


class Tracker(models.Model):
    module_id = models.IntegerField(null=False, unique=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    contact_num = PhoneNumberField(null=True)
    password = models.CharField(max_length=10, null=True)
    locked = models.BooleanField(default=False)
    tracked = models.BooleanField(default=False)

    def has_reached(self):
        if self.lat is None or self.lon is None or self.tracked == False:
            return False

        limit = float(config('GEO_RANGE'))
        last_entry = Position.objects.filter(tracker=self).order_by('-created_at')[0]
        last_lat = last_entry.lat
        last_lon = last_entry.lon

        print("Dest: "+str(self.lat)+", "+str(self.lon)+" last entry: "+str(last_lat)+", "+str(last_lon))
        if (self.lat >= last_lat - limit and self.lat <= last_lat + limit) \
                and (self.lon >= last_lon - limit and self.lon <= last_lon + limit):
            print("Reached Destination")
            return True

        return False

    def is_online(self):
        if self.lat is None or self.lon is None or self.tracked == False:
            return False
        limit = int(config('TIME_RANGE'))
        last_updated = Position.objects.filter(tracker=self).order_by('-created_at')[0].created_at
        now = datetime.now(pytz.timezone('Asia/Dhaka'))

        print("Now: "+str(now)+" Last updated: "+str(last_updated))
        if last_updated + timedelta(minutes = limit) > now:
            return True

        return False

    def num_warnings(self):
        return len(WarningEvent.objects.filter(position__tracker=self).all())

    @staticmethod
    def id_generator(size=6, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def gen_password(self):
        self.password = self.id_generator()
        print("Generated Pass: "+self.password)
        self.save()

    def gen_map(self):
        if self.lat is None or self.lon is None or self.lat ==0 or self.lon ==0 \
                or self.tracked == False:
            return None

        from gmplot import gmplot
        # Place map
        gmap = gmplot.GoogleMapPlotter(self.lat, self.lon, 10)
        gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

        positions = Position.objects.filter(tracker=self)
        lats = []
        lons = []
        times = []
        for position in positions:
            lats.append(position.lat)
            lons.append(position.lon)
            times.append(position.created_at)

        gmap.plot(lats, lons, 'cornflowerblue', edge_width=10)

        for i in range(0, len(lats)):
            title = "Point: "+str(i)+"  Lat: "+str(lats[i])+"  Lon: "+str(lons[i])+ "  Time: "+ str(times[i])
            gmap.marker(lats[i], lons[i], '#FF0000', title=title)

        mapfile = "/static/maps/map_"+str(self.id)+".html"
        # Draw
        gmap.draw("view"+ mapfile)

        from view.views import insertapikey
        insertapikey("view"+ mapfile, config('GMAP_API'))

        return mapfile

    def gen_graph(self):
        positions = Position.objects.filter(tracker= self).all()
        if positions.count() < 1:
            return None
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from matplotlib.figure import Figure

        fig = Figure(figsize=(9.5, 5.5))
        ax = fig.add_subplot(111)

        prev_pos = positions[0]
        time_diff = []
        # positions_id = [i for i in range(1,positions.count())]
        for i in range(1, positions.count()):
            diff_min = (positions[i].created_at - prev_pos.created_at).total_seconds() / 60.0
            # print(diff_min)
            time_diff.append(diff_min)
            prev_pos = positions[i]

        pd = pandas.DataFrame(data=time_diff)
        x_pos = numpy.arange(positions.count()-1)

        # ax.set_xticklabels(x_pos)
        # ax.set_xticks(x_pos)

        ax.plot(x_pos, pd[:][0].astype(float), label='Time Interval', color='b', marker='o')
        ax.set_title('No. of Position')
        ax.set_ylabel('Time Difference Between Consecutive Position ')
        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels)
        ax.grid('on')

        canvas = FigureCanvas(fig)
        graph1 = '/static/graphs/graph1_' + str(self.id)+'.jpg'
        file1 = open('view'+graph1, 'wb')
        canvas.print_png(file1)
        file1.close()
        return graph1

    def reset(self):
        self.lat = None
        self.lon = None
        self.tracked = False
        self.locked = False
        self.password = None
        Position.objects.filter(tracker= self).all().delete()
        WarningEvent.objects.filter(position__tracker=self).all().delete()
        self.save()


class Position(models.Model):
    tracker = models.ForeignKey(Tracker, null=False, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class WarningEvent(models.Model):
    position = models.ForeignKey(Position, null=False, on_delete=models.CASCADE)
    password = models.CharField(max_length=10, null=True)
