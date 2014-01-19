'''
Created on 18/01/2014

@author: sergiom
'''

from temperature import readers

from django.core.management.base import NoArgsCommand
import datetime, time, threading

next_call = time.time()

class Command(NoArgsCommand):
    help = 'Takes a temperature sample every minute'

    def handle_noargs(self, **options):
        print datetime.datetime.now()
        readers.take_sample()

        global next_call
        next_call = next_call + 1
        threading.Timer(next_call - time.time(), self.handle).start()
