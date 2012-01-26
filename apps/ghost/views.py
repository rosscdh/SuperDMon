from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from models import Host


@login_required
def gearman_overview(request, host):
    host = get_object_or_404(Host, pk=host)

    return render_to_response(
        'admin/ghost/host/overview_gearman.html', {
          'is_ajax': request.is_ajax,
          'original': host, # must use original here as its a shared admin template
      },
      context_instance=RequestContext(request)
    )

@login_required
def gearman_action(request, host, action):
    """
    Method to allow interaction with gearman services
    """
    host = get_object_or_404(Host, pk=host)

    return render_to_response(
        'ghost/gearman.html', {
          'is_ajax': request.is_ajax,
          'host': host,
      },
      context_instance=RequestContext(request)
    )

@login_required
def supervisor_overview(request, host):
    host = get_object_or_404(Host, pk=host)

    return render_to_response(
        'admin/ghost/host/overview_supervisor.html', {
          'is_ajax': request.is_ajax,
          'original': host, # must use original here as its a shared admin template
      },
      context_instance=RequestContext(request)
    )

@login_required
def supervisor_system_action(request, host, action):
    """
    Method to allow interaction with supervisor services
    """
    host = get_object_or_404(Host, pk=host)

    method = 'system.%s' % (action,)
    process_name = request.GET.get('name') or None

    if host.supervisor.is_valid_process(method):
        function = getattr(host.supervisor.system, method)
        if process_name:
            result = function(process_name)
        else:
            result = function()
    else:
        print "boo"

    return render_to_response(
      'ghost/supervisor.html', {
        'is_ajax': request.is_ajax,
        'host': host,
        'method': method,
        'process_name': process_name,
        'result': result,
      },
      context_instance=RequestContext(request)
    )

@login_required
def supervisor_action(request, host, action):
    """
    Method to allow interaction with supervisor services
    """
    host = get_object_or_404(Host, pk=host)
    
    method = 'supervisor.%s' % (action,)
    process_name = request.GET.get('name') or None
    offset = request.GET.get('offset') or None
    length = request.GET.get('length') or None

    if host.supervisor.is_valid_process(method):
        function = getattr(host.supervisor.conn, method)

        if offset >= 0 and length > 0:
            result = function(process_name, 0, 1024)
        else:
            if process_name:
                result = function(process_name)
            else:
                result = function()
    else:
        print "boo"
    
    return render_to_response(
      'ghost/supervisor.html', {
        'is_ajax': request.is_ajax,
        'host': host,
        'method': method,
        'process_name': process_name,
        'result': result,
      },
      context_instance=RequestContext(request)
    )    