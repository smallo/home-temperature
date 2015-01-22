'''
Created on 18/01/2014

@author: sergiom
'''

import random
import glob, time


class TempReaderMock():
    def __init__(self):
        self.last_temp = 20
        self.max_step = 0.5

    def get_temp(self):
        self.last_temp += (random.random()-0.5) * self.max_step
        return self.last_temp


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
