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
    month = models.CharField(max_length=6)
    n_samples = models.IntegerField()
    sum_value = models.FloatField()
    min_value = models.FloatField()
    max_value = models.FloatField()

class Configuration(models.Model):
    MODE = 'mode'
    TARGET_TEMPERATURE = 'target_temperature'
    HYSTERESIS_THRESHOLD = 'hysteresis_threshold'
    HEATER_STATUS = 'heater_status' # This is not realy a configuration field, this is for keeping the status of the heater
    MODE_ON = 'on'
    MODE_OFF = 'off'
    HEATER_ON = 'on'
    HEATER_OFF = 'off'
    key = models.CharField(max_length=25, unique=True)
    value = models.CharField(max_length=200)
