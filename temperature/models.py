from django.db import models

class Temperature(models.Model):
    timestamp = models.DateTimeField('Temperature sample time')
    value = models.FloatField()
    
class TemperatureHourly(models.Model):
    hour = models.CharField(max_length=10)
    n_samples = models.IntegerField()
    sum_value = models.FloatField()
    min_value = models.FloatField()
    max_value = models.FloatField()
    
class TemperatureDaily(models.Model):
    day = models.CharField(max_length=8)
    n_samples = models.IntegerField()
    sum_value = models.FloatField()
    min_value = models.FloatField()
    max_value = models.FloatField()
    
class TemperatureMonthly(models.Model):
    day = models.CharField(max_length=6)
    n_samples = models.IntegerField()
    sum_value = models.FloatField()
    min_value = models.FloatField()
    max_value = models.FloatField()

class Configuration(models.Model):
    key = models.CharField(max_length=25)
    value = models.CharField(max_length=200)
