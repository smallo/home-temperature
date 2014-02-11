home-temperature
================
Use a Raspberry to read the temperature from a sensor, store it and show some graphs.


Installation
============
```shell
git clone https://github.com/smallo/home-temperature
sudo apt-get install python-pip
sudo pip install -r requirements.txt 
python manage.py syncdb
python manage.py runserver 0.0.0.0:8000
python manage.py take_samples
```

FIX
---
Need to fix django-chartit (at least required for python 2.7.3 in Raspbian,
not required for python 2.7.5 in OSX):

```shell
pi@raspberrypi /usr/local/lib/python2.7/dist-packages/chartit/templatetags $ sudo vi chartit.py
```
 - in line 70: remove "use_decimal=True" 


URLs
====
 - http://erio.dyndns.org/temperature/graph
 - http://localhost:8000/temperature/graph/
 - http://localhost:8000/temperature/
 - http://localhost:8000/admin
