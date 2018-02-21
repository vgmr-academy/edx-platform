import errno
import os
import re

from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from edxmako.shortcuts import render_to_response, render_to_string
from util.json_request import  JsonResponse, JsonResponseBadRequest

from django.views.decorators.csrf import ensure_csrf_cookie

from django.contrib.auth.models import User

from organizations.models import Organization
from microsite_configuration.models import (
    Microsite,
    MicrositeOrganizationMapping,
    MicrositeTemplate
)

from .models import MicrositeDetail , MicrositeAdminManager

from django.http import QueryDict

from .microsite_manager import microsite_manager

from django.views.decorators.http import require_GET, require_POST ,require_http_methods

from util.views import require_global_staff



@login_required
@ensure_csrf_cookie
@require_POST
@require_global_staff
def create_microsite(request):
    return microsite_manager().create(request)


@login_required
@ensure_csrf_cookie
@require_global_staff
def admin_microsite(request, microsite_id=None):
    if request.method == 'GET':
        #try:
        microsite_details = MicrositeDetail.objects.get(id=microsite_id)
        microsite_name = microsite_details.name
        microsite = Microsite.objects.get(key=microsite_name)
        microsite_value = microsite.values
        context = {}
        context['key'] = microsite_name
        context['microsite_value'] = microsite_value
        context['microsite_admin'] = microsite_manager().get_microsite_admin_manager(microsite)
        return render_to_response('admin_microsite.html',context)



def microsite_admin_manager(request, microsite_key):
    return microsite_manager().microsite_admin_manager(request, microsite_key)

@login_required
def update_microsite(request, microsite_id=None):
    if request.method == 'GET':
        return microsite_manager().manage_microsite_data(request, microsite_id)
    elif request.method == 'POST':
        return microsite_manager().update_microsite_data(request, microsite_id)

@login_required
@ensure_csrf_cookie
@require_global_staff
def disclaimer_microsite(request, microsite_key):
    return microsite_manager().microsite_disclaimer_update(request, microsite_key)
