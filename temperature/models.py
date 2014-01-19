from django.db import models

class Temperature(models.Model):
    timestamp = models.DateTimeField('Temperature sample time')
    value = models.FloatField()
    

class Configuration(models.Model):
    key = models.CharField(max_length=25)
    value = models.CharField(max_length=200)

