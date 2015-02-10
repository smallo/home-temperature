from django.contrib import admin
from temperature.models import Temperature, TemperatureHourly, TemperatureDaily, TemperatureMonthly, Configuration


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')

class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'value')

class TemperatureHourlyAdmin(admin.ModelAdmin):
    list_display = ('hour', 'n_samples', 'sum_value', 'min_value', 'max_value')

class TemperatureDailyAdmin(admin.ModelAdmin):
    list_display = ('day', 'n_samples', 'sum_value', 'min_value', 'max_value')

class TemperatureMonthlyAdmin(admin.ModelAdmin):
    list_display = ('month', 'n_samples', 'sum_value', 'min_value', 'max_value')


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Temperature, TemperatureAdmin)
admin.site.register(TemperatureHourly, TemperatureHourlyAdmin)
admin.site.register(TemperatureDaily, TemperatureDailyAdmin)
admin.site.register(TemperatureMonthly, TemperatureMonthlyAdmin)

