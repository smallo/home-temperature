from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'home_temperature.views.home', name='home'),
    # url(r'^home_temperature/', include('home_temperature.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^temperature/', include('temperature.urls', namespace='temperature')),

    # ex: /temperature/login
    url(r'^temperature/login/$', 'django.contrib.auth.views.login', {'template_name': 'temperature/login.html'}),
)
