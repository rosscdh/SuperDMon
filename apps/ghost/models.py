from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
import gearman
import simplejson as json
import xmlrpclib


class Host(models.Model):
    host = models.CharField(max_length=128)
    gearman_port = models.IntegerField()
    supervisor_port = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s:%d/%d' % (self.host,self.gearman_port,self.supervisor_port)

    @property
    def gearman_server_uri(self):
        return '%s:%d' % (self.host,self.gearman_port)

    @property
    def supervisor_server_uri(self):
        return '%s:%d' % (self.host,self.supervisor_port)

    @property
    def gearman(self):
        return GearmanInterface(self.gearman_server_uri)

    @property
    def supervisor(self):
        try:
            return SupervisordInterface()
        except:
            pass

    def ping_server(self):
	    return self.gearman.ping_server()

    def get_version(self):
	    return self.gearman.get_version()

    def get_status(self):
        status = []
        for s in self.gearman.get_status():
            status.append( s )
        return status

    def get_workers(self):
        workers = []
        for w in self.gearman.get_workers():
            if w['tasks']:
                if w['client_id'] == '-' or not w['client_id']:
                    """stupid stupid php extensions"""
                    client_id_fix = [i for i in w['tasks']]
                    client_id_fix = "-".join(client_id_fix)
                    w['client_id'] = '%s.php' % (slugify(client_id_fix),)
                workers.append( w )
        return workers


class GearmanInterface(object):
    def __init__(self, broker_host=None):
        self.broker_host = broker_host
        self.server = gearman.admin_client.GearmanAdminClient([self.broker_host], 5)
        self.get_server()

    def get_server(self):
        try:
            self.server.ping_server()
        except:
            self.server = None
        return self.server

    def ping_server(self):
	    return self.server.ping_server() if self.get_server() else None

    def get_version(self):
	    return self.server.get_version() if self.get_server() else None

    def get_status(self):
        return self.server.get_status() if self.get_server() else None

    def get_workers(self):
        return self.server.get_workers() if self.get_server() else None


class SupervisordInterface(object):
    def __init__(self, server_url=None):
        supervisor = settings.GHOST_SETTINGS['supervisor']
        supervisor['url'] = server_url if server_url is not None else supervisor['url']

        self.username = supervisor['username']
        self.password = supervisor['password']
        user_info = '%s:%s@' % (self.username, self.password,) if self.username and self.password else ''
        self.server = 'http://%s%s' % (user_info, supervisor['url'],)


        # conn is what you query the actual service on
        self.conn = server = xmlrpclib.ServerProxy(self.server)
        # system is what you use to get info abotu the server
        self.system = self.conn.system

    def is_valid_process(self, process_name):
        methods = self.get_sys('listMethods')
        if process_name in methods:
            return True
        else:
            return False

    def getAllProcessInfo(self):
        return self.get_rpc('supervisor.getAllProcessInfo')

    def get_rpc(self, method='supervisor.getState', **kwargs):
        """ Valid Methods
        ['supervisor.addProcessGroup', 'supervisor.clearAllProcessLogs', 'supervisor.clearLog', 'supervisor.clearProcessLog', 
        'supervisor.clearProcessLogs', 'supervisor.getAPIVersion', 'supervisor.getAllConfigInfo', 'supervisor.getAllProcessInfo', 
        'supervisor.getIdentification', 'supervisor.getPID', 'supervisor.getProcessInfo', 'supervisor.getState', 
        'supervisor.getSupervisorVersion', 'supervisor.getVersion', 'supervisor.readLog', 'supervisor.readMainLog', 
        'supervisor.readProcessLog', 'supervisor.readProcessStderrLog', 'supervisor.readProcessStdoutLog', 
        'supervisor.reloadConfig', 'supervisor.removeProcessGroup', 'supervisor.restart', 'supervisor.sendProcessStdin', 
        'supervisor.sendRemoteCommEvent', 'supervisor.shutdown', 'supervisor.startAllProcesses', 'supervisor.startProcess', 
        'supervisor.startProcessGroup', 'supervisor.stopAllProcesses', 'supervisor.stopProcess', 'supervisor.stopProcessGroup', 
        'supervisor.tailProcessLog', 'supervisor.tailProcessStderrLog', 'supervisor.tailProcessStdoutLog']
        """
        function = getattr(self.conn, method)
        if kwargs:
            return function(kwargs)
        else:
            return function()

    def get_sys(self, method, **kwargs):
        """ Valid Methods
        ['system.listMethods', 'system.methodHelp', 'system.methodSignature', 'system.multicall'
        """
        function = getattr(self.system, method)
        if kwargs:
            return function(kwargs)
        else:
            return function()

