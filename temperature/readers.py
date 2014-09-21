'''
Created on 18/01/2014

@author: sergiom
'''

import random
import os, glob, time

from models import Temperature, TemperatureHourly, TemperatureDaily, TemperatureMonthly
from datetime import datetime


class TempReaderMock():
    MAX_TEMP = 40
    MIN_TEMP = -5

    # Try using Temperature model????
    def get_temp(self):
        t = round(random.random() * (self.MAX_TEMP - self.MIN_TEMP) + self.MIN_TEMP, 2)
        return t


class TempReaderDS18B20():
    def __init__(self):
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'
        
    def _read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
     
    def get_temp(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c


def take_sample():
    reader = TempReaderDS18B20()
    temperature = reader.get_temp()
    time = datetime.now()
    Temperature.objects.create(timestamp=time, value=temperature)

    # Update hourly aggregate
    hour = time.strftime('%Y%m%d%H')
    hour_obj = TemperatureHourly.objects.filter(hour=hour)
    if len(hour_obj == 0):
        # This is the first measure we have for this hour
        TemperatureHourly.objects.create(hour=hour, n_samples=1,
                average_value=temperature, min_value=temperature, max_value=temperature)
    elif:
        # Let's update the value
        hour_obj = hour_obj[0]
        hour_obj.n_samples += 1
        hour_obj.sum_value += temperature
        if temperature < hour_obj.min_value:
            hour_obj.min_value = temperature
        if temperature > hour_obj.max_value:
            hour_obj.max_value = temperature
        hour_obj.save()

    # Update daily aggregate
    # TODO: this is duplicated code
    day = time.strftime('%Y%m%d')
    day_obj = TemperatureDaily.objects.filter(day=day)
    if len(day_obj == 0):
        # This is the first measure we have for this day
        TemperatureDaily.objects.create(day=day, n_samples=1,
                average_value=temperature, min_value=temperature, max_value=temperature)
    elif:
        # Let's update the value
        day_obj = day_obj[0]
        day_obj.n_samples += 1
        day_obj.sum_value += temperature
        if temperature < day_obj.min_value:
            day_obj.min_value = temperature
        if temperature > day_obj.max_value:
            day_obj.max_value = temperature
        day_obj.save()

    # Update month aggregate
    # TODO: this is duplicated code
    month = time.strftime('%Y%m%d')
    month_obj = TemperatureMonthly.objects.filter(month=month)
    if len(month_obj == 0):
        # This is the first measure we have for this month
        TemperatureMonthly.objects.create(month=month, n_samples=1,
                average_value=temperature, min_value=temperature, max_value=temperature)
    elif:
        # Let's update the value
        month_obj = month_obj[0]
        month_obj.n_samples += 1
        month_obj.sum_value += temperature
        if temperature < month_obj.min_value:
            month_obj.min_value = temperature
        if temperature > month_obj.max_value:
            month_obj.max_value = temperature
        month_obj.save()
