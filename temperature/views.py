from django.shortcuts import render, render_to_response
from chartit import DataPool, Chart

from models import Temperature

def index(request):
    temperature_samples = Temperature.objects.order_by('-timestamp')
    context = { 'temperature_samples': temperature_samples }
    return render(request, 'temperature/index.html', context)


def graph(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    temperature_data = \
        DataPool(
           series=
            [{'options': {
               'source': Temperature.objects.all()},
              'terms': [
                'id',
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
                  'id': [
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
