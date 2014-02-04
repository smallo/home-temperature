'''
Created on 18/01/2014

@author: sergiom
'''

import random
import os, glob, time

from models import Temperature
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
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'
        
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
     
    def get_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c


def take_sample():
    reader = TempReaderDS18B20()
    temp = reader.get_temp()
    time = datetime.now()
    Temperature.objects.create(timestamp=time, value=temp)
