from django.shortcuts import render

from models import Temperature

def index(request):
    temperature_samples = Temperature.objects.order_by('-timestamp')
    context = { 'temperature_samples': temperature_samples }
    return render(request, 'temperature/index.html', context)
