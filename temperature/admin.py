from django.contrib import admin
from temperature.models import Temperature, Configuration


class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'value')


admin.site.register(Temperature, TemperatureAdmin)
admin.site.register(Configuration)

