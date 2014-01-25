from django.conf.urls import patterns, url

from temperature import views

urlpatterns = patterns('',
    # ex: /temperature
    url(r'^$', views.index, name='index'),
    # ex: /temperature/graph/
    url(r'^graph/$', views.graph, name='graph'),
)
