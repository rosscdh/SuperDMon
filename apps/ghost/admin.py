from django.contrib import admin
from django.conf.urls.defaults import *
from models import *
from views import gearman_action, supervisor_system_action, supervisor_action, supervisor_overview, gearman_overview
from apps.gworker.models import Worker, WorkerToHost

from apps.gtask.views import get_logs


class WorkerInline(admin.TabularInline):
    model = WorkerToHost

class HostAdmin(admin.ModelAdmin):
    fields = ('host', 'gearman_port', 'supervisor_port',)
    # inlines = [
    #     WorkerInline,
    # ]

    def get_urls(self):
        urls = super(HostAdmin, self).get_urls()
        host_admin_urls = patterns('',
            url(r'(?P<host>.*)/overview/gearman/refresh/$', self.admin_site.admin_view(gearman_overview),name='admin_gearman_refresh',),
            url(r'(?P<host>.*)/overview/supervisor/refresh/$', self.admin_site.admin_view(supervisor_overview),name='admin_supervisor_refresh',),
            url(r'(?P<host>.*)/gearman/(?P<action>.*)/$', self.admin_site.admin_view(gearman_action),name='admin_gearman_action',),
            url(r'(?P<host>.*)/supervisor/system/(?P<action>.*)/$', self.admin_site.admin_view(supervisor_system_action),name='admin_supervisor_system_action',),
            url(r'(?P<host>.*)/supervisor/(?P<action>.*)/$', self.admin_site.admin_view(supervisor_action),name='admin_supervisor_action',),
#temp
            url(r'redis/(?P<key>.*)/$', self.admin_site.admin_view(get_logs),name='admin_gearman_get_logs',),
        )
        return host_admin_urls + urls

admin.site.register(Host, HostAdmin)