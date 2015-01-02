from rest_framework import serializers

from models import Temperature, TemperatureHourly, TemperatureDaily, TemperatureMonthly, Configuration

class TemperatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Temperature
        fields = ('timestamp', 'value')

class TemperatureHourlySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TemperatureHourly
        fields = ('hour', 'n_samples', 'sum_value', 'min_value', 'max_value')

class TemperatureDailySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TemperatureDaily
        fields = ('day', 'n_samples', 'sum_value', 'min_value', 'max_value')

class TemperatureMonthlySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TemperatureMonthly
        fields = ('month', 'n_samples', 'sum_value', 'min_value', 'max_value')

class ConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Configuration
        fields = ('key', 'value')
