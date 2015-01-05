from django import forms
from django.shortcuts import render, render_to_response
from chartit import DataPool, Chart
from datetime import datetime, timedelta

from models import Temperature, Configuration
from services import set_mode, set_target_temperature


class SettingsForm(forms.Form):
    mode = forms.CharField(label='Mode', max_length=3)
    target_temperature = forms.FloatField(label='Target temperature')

    error_css_class = 'alert alert-danger'


def index(request):
    heater_status = Configuration.objects.filter(key=Configuration.HEATER_STATUS)[0].value
    current_temperature = Temperature.objects.order_by('-timestamp')[0]

    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            set_mode(form.cleaned_data['mode'])
            set_target_temperature(form.cleaned_data['target_temperature'])
    else:
        mode = Configuration.objects.filter(key=Configuration.MODE)[0].value
        target_temperature = Configuration.objects.filter(key=Configuration.TARGET_TEMPERATURE)[0].value
        form = SettingsForm(initial={'mode': mode, 'target_temperature': target_temperature})

    context = { 'current_temperature': current_temperature,
                'heater_status': heater_status,
                'form': form}

    return render(request, 'temperature/index.html', context)


def graph(request):
    #Step 1: Create a DataPool with the data we want to retrieve.

    # Only get temperature from last day
    begin_time = datetime.now() - timedelta(days=1)

    # date are not supported by chartit, so I change the timestamp to be a string
    t_samples = Temperature.objects.filter(timestamp__gt=begin_time).extra(select={'timestamp': 'datetime(timestamp)'})
    
    temperature_data = \
        DataPool(
           series=
            [{'options': {
               'source': t_samples},
              'terms': [
                'timestamp',
                'value']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = temperature_data,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'timestamp': [
                    'value']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Home temperature evolution'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response('temperature/graph.html', {'temperature_chart': cht})
