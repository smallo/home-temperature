__author__ = 'sergiom'

from django.conf import settings
from datetime import datetime

from readers import TempReaderDS18B20, TempReaderMock
from activators import ActivatorRpiGpio, ActivatorMock
from models import Configuration, Temperature, TemperatureHourly, TemperatureDaily, TemperatureMonthly


if settings.USE_MOCK:
    _reader = TempReaderMock()
    _activator = ActivatorMock(int(settings.GPIO_HEATER_ACTIVATION_PIN))
else:
    _reader = TempReaderDS18B20()
    _activator = ActivatorRpiGpio(int(settings.GPIO_HEATER_ACTIVATION_PIN))


def set_mode(mode):
    #First let's validate input data
    if((mode != Configuration.MODE_ON) and (mode != Configuration.MODE_OFF)):
        raise ValueError('mode could only be on or off')

    c = Configuration.objects.filter(key=Configuration.MODE)[0]
    c.value = mode
    c.save()

    activate_heater_if_necessary()


def set_target_temperature(target_temperature):
    c = Configuration.objects.filter(key=Configuration.TARGET_TEMPERATURE)[0]
    c.value = target_temperature
    c.save()

    activate_heater_if_necessary()


def activate_heater_if_necessary():
    # Get the current mode
    mode = Configuration.objects.filter(key=Configuration.MODE)[0].value

    if mode == Configuration.MODE_OFF:
        return

    # Get current temperature
    current_temperature_obj = Temperature.objects.all().order_by('-timestamp')[0]
    #TODO: take into account timestamp, could be old!!!
    print 'Current temperature: {0}, measured at: {1}'.format(current_temperature_obj.value, current_temperature_obj.timestamp)
    current_temperature = current_temperature_obj.value

    # Get the target temperature
    target_temperature = float(Configuration.objects.filter(key=Configuration.TARGET_TEMPERATURE)[0].value)
    print 'Target temperature: {0}'.format(target_temperature)

    # Get hysteresis threshold
    hysteresis_threshold = float(Configuration.objects.filter(key=Configuration.HYSTERESIS_THRESHOLD)[0].value)
    print 'Hysteresis threshold: {0}'.format(hysteresis_threshold)

    # Get the current heater status
    heater_status_obj = Configuration.objects.filter(key=Configuration.HEATER_STATUS)[0]
    is_heater_on = Configuration.HEATER_ON == heater_status_obj.value
    print 'Heater status: {0}'.format(heater_status_obj.value)

    if is_heater_on:
        should_activate = (current_temperature < (target_temperature - hysteresis_threshold))
    else:
        should_activate = (current_temperature < (target_temperature + hysteresis_threshold))
    print 'Should activate: {0}'.format(should_activate)


    if (should_activate and not is_heater_on):
        _activator.activate()
        heater_status_obj.value = Configuration.HEATER_ON
        heater_status_obj.save()
    elif (not should_activate and is_heater_on):
        _activator.deactivate()
        heater_status_obj.value = Configuration.HEATER_OFF
        heater_status_obj.save()


def take_sample():
    temperature = _reader.get_temp()
    time = datetime.now()
    Temperature.objects.create(timestamp=time, value=temperature)

    activate_heater_if_necessary()

    # Update hourly aggregate
    hour = time.strftime('%Y%m%d%H')
    hour_obj = TemperatureHourly.objects.filter(hour=hour)
    if len(hour_obj) == 0:
        # This is the first measure we have for this hour
        TemperatureHourly.objects.create(hour=hour, n_samples=1, sum_value=temperature, min_value=temperature, max_value=temperature)
    else:
        # Let's update the value
        hour_obj = hour_obj[0]
        hour_obj.n_samples += 1
        hour_obj.sum_value += temperature
        if temperature < hour_obj.min_value:
            hour_obj.min_value = temperature
        if temperature > hour_obj.max_value:
            hour_obj.max_value = temperature
        hour_obj.save()

    # Update daily aggregate
    # TODO: this is duplicated code
    day = time.strftime('%Y%m%d')
    day_obj = TemperatureDaily.objects.filter(day=day)
    if len(day_obj) == 0:
        # This is the first measure we have for this day
        TemperatureDaily.objects.create(day=day, n_samples=1, sum_value=temperature, min_value=temperature, max_value=temperature)
    else:
        # Let's update the value
        day_obj = day_obj[0]
        day_obj.n_samples += 1
        day_obj.sum_value += temperature
        if temperature < day_obj.min_value:
            day_obj.min_value = temperature
        if temperature > day_obj.max_value:
            day_obj.max_value = temperature
        day_obj.save()

    # Update month aggregate
    # TODO: this is duplicated code
    month = time.strftime('%Y%m')
    month_obj = TemperatureMonthly.objects.filter(month=month)
    if len(month_obj) == 0:
        # This is the first measure we have for this month
        TemperatureMonthly.objects.create(month=month, n_samples=1, sum_value=temperature, min_value=temperature, max_value=temperature)
    else:
        # Let's update the value
        month_obj = month_obj[0]
        month_obj.n_samples += 1
        month_obj.sum_value += temperature
        if temperature < month_obj.min_value:
            month_obj.min_value = temperature
        if temperature > month_obj.max_value:
            month_obj.max_value = temperature
        month_obj.save()
