'''
Created on 18/01/2014

@author: sergiom
'''

import kronos
import readers


@kronos.register('* * * * *')
def take_sample():
    readers.take_sample()
