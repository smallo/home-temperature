#! /bin/bash

source ./tmp/venv/home-temperature/bin/activate 
python manage.py runserver 0.0.0.0:8000 --noreload
