from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from temperature import views, views_api

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'temperatures', views_api.TemperatureViewSet, base_name='temperatures')
router.register(r'temperaturehourlys', views_api.TemperatureHourlyViewSet, base_name='temperaturehourlys')
router.register(r'temperaturedailys', views_api.TemperatureDailyViewSet, base_name='temperaturedailys')
router.register(r'temperaturemonthlys', views_api.TemperatureMonthlyViewSet, base_name='temperaturemonthlys')

# API endpoints
urlpatterns = [
    # ex: /temperature
    url(r'^$', views.index, name='index'),
    # ex: /temperature/graph/
    url(r'^graph/$', views.graph, name='graph'),
    # ex: /temperature/api
    url(r'^api/', include(router.urls)),
]
