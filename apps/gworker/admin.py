from django.contrib import admin
from models import *
from apps.ghost.models import Host

class HostInline(admin.TabularInline):
    model = Worker.hosts.through

class WorkerAdmin(admin.ModelAdmin):
    inlines = [
        HostInline,
    ]

admin.site.register(Worker, WorkerAdmin)