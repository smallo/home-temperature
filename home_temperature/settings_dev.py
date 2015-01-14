__author__ = 'sergiom'

from settings import *

# Override some of the settings here for the development environment
USE_MOCK = True
GPIO_HEATER_ACTIVATION_PIN = 88 # This is just to see a different number here

# When developing sqlite is enough and easier to set up
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': './home_temperature.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
