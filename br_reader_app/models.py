from django.db import models

class Reading(models.Model):
    pressure = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    temprature = models.FloatField(blank=True, null=True)
    read_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)