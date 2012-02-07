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
from apps.gtask import RedisServer



def get_logs(request, key):
#    host = get_object_or_404(Host, pk=host)
    r = RedisServer()
    logs = r.get_task_logs(key)

    return render_to_response(
        'admin/gtask/log.html', {
          'is_ajax': request.is_ajax,
          'logs': logs,
          'key': r.key,
      },
      context_instance=RequestContext(request)
    )
