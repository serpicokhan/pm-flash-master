'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(newobject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from cmms.models.workorder import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict

from django.db.models import Q
from django.contrib.admin.models import LogEntry

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper



###################################################################
# @permission_required('cmms.view_logentry')
def js_list_woLog(request,woId):
    try:
        data=dict()
        books=LogEntry.objects.filter(object_repr='workorder',object_id=woId)
        print(books,"######################")
        data['html_wolog_list']= render_to_string('cmms/workorder_log/partialWoLogList.html', {
            'wolog': books
        })
        data['form_is_valid']=True
        return JsonResponse(data)
    except Exception as e:
        print(e)
        return JsonResponse({'a':1})
