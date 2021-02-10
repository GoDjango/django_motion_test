from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
