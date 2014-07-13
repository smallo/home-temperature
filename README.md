home-temperature
================
Use a Raspberry to read the temperature from a sensor, store it and show some graphs.


Installation
============
Load 1-wire bus kernel modules:
```shell
sudo modprobe w1_gpio 
sudo modprobe w1_therm
```

For loading the modules at boot time:
```shell
sudo vi /etc/modules
w1_gpio
w1_therm
```

Install python libraries and run the server
```shell
sudo apt-get install python-dev
sudo apt-get install python-rpi.gpio

sudo apt-get install python-pip
sudo pip install virtualenv

git clone https://github.com/smallo/home-temperature
cd home-temperature

virtualenv ./tmp/venv/home-temperature
source ./tmp/venv/home-temperature/bin/activate
pip install -r requirements.txt 
python manage.py syncdb
python manage.py runserver 0.0.0.0:8000 --noreload
python manage.py take_samples
```

--noreload: this option is used to avoid a continuous usage of CPU around 10%

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
