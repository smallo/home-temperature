__author__ = 'sergiom'

from datetime import datetime, time, timedelta

from models import Configuration

class On():
    def __init__(self):
        pass

    @staticmethod
    def start():
        pass

    @staticmethod
    def is_on():
        return True


class Off():
    def __init__(self):
        pass

    @staticmethod
    def start():
        pass

    @staticmethod
    def is_on():
        return False


class AutoSwitchOff():
    def __init__(self):
        pass

    @staticmethod
    def start():
        # Get current date, autoswitchoff time and calculate next datetime for switching off
        current_datetime = datetime.now()
        current_time = current_datetime.time()
        auto_switch_off_time_str = Configuration.objects.filter(key=Configuration.MODE_SETTINGS_AUTO_SWITCH_OFF_TIME)[0].value
        auto_switch_off_time = time(
            int(auto_switch_off_time_str[0:2]),
            int(auto_switch_off_time_str[3:5]))

        auto_switch_off_datetime = current_datetime.combine(current_datetime, auto_switch_off_time)

        # When current_time is greater than auto switch off time we need to
        # add one day
        if current_time > auto_switch_off_time:
            auto_switch_off_datetime += timedelta(1)

        # Store the datetime
        auto_switch_off_datetime_obj = Configuration.objects.filter(key=Configuration.MODE_SETTINGS_AUTO_SWITCH_OFF_DATETIME)[0]
        auto_switch_off_datetime_obj.value = auto_switch_off_datetime.strftime("%Y-%m-%dT%H:%MZ")
        auto_switch_off_datetime_obj.save()

        print "AutoSwitchOff mode started, it will switch off at: {}".format(auto_switch_off_datetime)

        return

    @staticmethod
    def is_on():
        # True when current time is before auto switch off datetime
        current_time = datetime.now()
        auto_switch_off_datetime_str = Configuration.objects.filter(key=Configuration.MODE_SETTINGS_AUTO_SWITCH_OFF_DATETIME)[0].value
        auto_switch_off_datetime = datetime.strptime(auto_switch_off_datetime_str, "%Y-%m-%dT%H:%MZ")

        on = current_time < auto_switch_off_datetime
        if not on:
            mode = Configuration.objects.filter(key=Configuration.MODE)[0]
            mode.value = Configuration.MODE_OFF
            mode.save()

        return on
