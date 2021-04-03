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



#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PartLocationForm

###################################################################

def js_list_projectScheduled(request,woId):
    data=dict()

    books=WorkOrder.objects.filter(Project=woId).filter(isScheduling=True)
    print(books)
    data['html_projectscheduled_list']= render_to_string('cmms/projectscheduled/partialProjectScheduledList.html', {
        'projectScheduleds': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
