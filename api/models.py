from django.db import models


class Position(models.Model):
    tracker = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
