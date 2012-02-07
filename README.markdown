GearMon - Gearman Monitoring Application
==========================================

GearMon has been developed after discovering a need for a simple monitoring system for Gearman.

Gearman is best monitored/managed using Supervisord which provides an xmlrpc interface to allow you to stop/start gearman as well as gearman workers (which becomes quite a task in distributed system)

You must install:
------

* Gearman
* libgearman - php/python/ruby libraries
* supervisord
* redis
* Django python etc (easy_install) pip install -r requirements.txt

At the moment, the system simply connects to the gearman instance and the supervisord instance as defined by the appropriate port setting and then allows you to stop/start/restart/tail the logs of all systems registered with supervisord. Advanced logging is supplied via redis (which you will need to write an interface to in your workers

1. Install supervisord and read its get started docs http://supervisord.org/
2. Register Gearman with supervisord
3. Register your Gearman Workers with supervisord
4. Install requirements.txt (pip) 
5. Django python manage.py syncdb (uses sqlite3 by default)
6. Log into /admin
7. Add a host + Gearman & Supervisord Ports
8. Enjoy

# The system defines:

Hosts
------
* Which you must specify a ip/name
* And a Gearman Port
* As well as a Supervisord Port


Tasks
------
* Coming Soon
