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


###################################################################

def js_list_projectWo(request,woId):
    data=dict()

    books=WorkOrder.objects.filter(Project=woId).filter(isScheduling=False)
    print(books)
    data['html_projectWo_list']= render_to_string('cmms/projectwo/partialProjectWoList.html', {
        'projectWos': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
