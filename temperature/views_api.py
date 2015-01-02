from models import Temperature, TemperatureHourly, TemperatureDaily, TemperatureMonthly, Configuration
from services import set_mode, set_target_temperature
from rest_framework import viewsets
from serializers import TemperatureSerializer, TemperatureHourlySerializer, TemperatureDailySerializer,\
                        TemperatureMonthlySerializer, ConfigurationSerializer


class TemperatureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TemperatureSerializer

    def get_queryset(self):
        queryset = Temperature.objects.all()

        current_param = self.request.QUERY_PARAMS.get('current', None)
        if current_param == 'true':
            queryset = queryset.order_by('-timestamp')[:1]
            return queryset
        
        from_param = self.request.QUERY_PARAMS.get('from', None)
        to_param = self.request.QUERY_PARAMS.get('to', None)
        if from_param is not None:
            queryset = queryset.filter(timestamp__gte=from_param)
        if to_param is not None:
            queryset = queryset.filter(timestamp__lte=to_param)
        return queryset

class TemperatureHourlyViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'hour'
    serializer_class = TemperatureHourlySerializer

    def get_queryset(self):
        queryset = TemperatureHourly.objects.all()
        from_param = self.request.QUERY_PARAMS.get('from', None)
        to_param = self.request.QUERY_PARAMS.get('to', None)
        if from_param is not None:
            queryset = queryset.filter(hour__gte=from_param)
        if to_param is not None:
            queryset = queryset.filter(hour__lte=to_param)
        return queryset

class TemperatureDailyViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'day'
    serializer_class = TemperatureDailySerializer

    def get_queryset(self):
        queryset = TemperatureDaily.objects.all()
        from_param = self.request.QUERY_PARAMS.get('from', None)
        to_param = self.request.QUERY_PARAMS.get('to', None)
        if from_param is not None:
            queryset = queryset.filter(day__gte=from_param)
        if to_param is not None:
            queryset = queryset.filter(day__lte=to_param)
        return queryset

class TemperatureMonthlyViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'month'
    serializer_class = TemperatureMonthlySerializer

    def get_queryset(self):
        queryset = TemperatureMonthly.objects.all()
        from_param = self.request.QUERY_PARAMS.get('from', None)
        to_param = self.request.QUERY_PARAMS.get('to', None)
        if from_param is not None:
            queryset = queryset.filter(month__gte=from_param)
        if to_param is not None:
            queryset = queryset.filter(month__lte=to_param)
        return queryset

class ConfigurationViewSet(viewsets.ModelViewSet):
    lookup_field = 'key'
    serializer_class = ConfigurationSerializer
    queryset = Configuration.objects.all()

    def perform_update(self, serializer):
        if self.request.data['key'] == Configuration.MODE:
            set_mode(serializer.validated_data['value'])
        elif self.request.data['key'] == Configuration.TARGET_TEMPERATURE:
            set_target_temperature(float(serializer.validated_data['value']))
        elif self.request.data['key'] == Configuration.HEATER_STATUS:
            # This is an internal status, so we don't want it to be modified through the API
            return

        serializer.save() #TODO: for mode and target_temperature we are saving twice; I needed to do for the doc API to be correctly updated