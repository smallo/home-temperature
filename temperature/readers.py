'''
Created on 18/01/2014

@author: sergiom
'''

import random
from models import Temperature
from datetime import datetime

class TempReaderMock():
    MAX_TEMP = 40
    MIN_TEMP = -5

    # Try using Temperature model????
    def get_temp(self):
        t = round(random.random() * (self.MAX_TEMP - self.MIN_TEMP) + self.MIN_TEMP, 2)
        return t


def take_sample():
    reader = TempReaderMock()
    temp = reader.get_temp()
    time = datetime.now()
    Temperature.objects.create(timestamp=time, value=temp)
