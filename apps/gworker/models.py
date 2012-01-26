from django.db import models
from apps.ghost.models import Host


class Worker(models.Model):
    hosts = models.ManyToManyField(Host, blank=True, null=True, through='WorkerToHost')#, db_table='gworker_workertohost'
    name = models.CharField(max_length=128)
    signature = models.CharField(max_length=128, null=True) # all available methods on worker are SH1 into a hash that is used to check when a worker changes its signature
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s' % (self.name)


class WorkerToHost(models.Model):
    worker = models.ForeignKey(Worker)
    host = models.ForeignKey(Host)
    startup_command = models.CharField(max_length=255)
    runas_user = models.CharField(max_length=64)
    num_proc = models.IntegerField(default=1)
    autostart = models.BooleanField(default=True)
    autorestart = models.BooleanField(default=True)
