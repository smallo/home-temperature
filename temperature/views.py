from django import forms
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime, timedelta

from models import Temperature, Configuration
from services import set_mode, set_target_temperature


class SettingsForm(forms.Form):
    mode = forms.BooleanField(label='Mode', required=False)
    target_temperature = forms.FloatField(label='Target temperature')

    error_css_class = 'alert alert-danger'


def index(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return redirect('/temperature/login/?next=%s' % request.path)

        form = SettingsForm(request.POST)
        if form.is_valid():
            set_mode(Configuration.MODE_AUTO_SWITCH_OFF if form.cleaned_data['mode'] else Configuration.MODE_OFF, False)
            set_target_temperature(form.cleaned_data['target_temperature'], True)
    else:
        mode = Configuration.MODE_AUTO_SWITCH_OFF == Configuration.objects.filter(key=Configuration.MODE)[0].value
        target_temperature = Configuration.objects.filter(key=Configuration.TARGET_TEMPERATURE)[0].value
        form = SettingsForm(initial={'mode': mode, 'target_temperature': target_temperature})

    heater_status = Configuration.objects.filter(key=Configuration.HEATER_STATUS)[0].value
    current_temperature = Temperature.objects.order_by('-timestamp')[0]

    context = { 'current_temperature': current_temperature,
                'heater_status': heater_status,
                'form': form}

    return render(request, 'temperature/index.html', context)
