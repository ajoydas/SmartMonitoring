from datetime import datetime, timezone, timedelta
import random
import string

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from decouple import config


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
        now = datetime.now(timezone.utc)

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
        if self.lat is None or self.lon is None or self.tracked == False:
            return "None"

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

        return mapfile

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
