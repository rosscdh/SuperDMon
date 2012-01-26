from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gearmon.views.home', name='home'),
    # url(r'^gearmon/', include('gearmon.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
