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
from cmms.forms import StopCodeForm

###################################################################
def list_woStop(request,id=None):
    books = StopCode.objects.all()
    return render(request, 'cmms/part_purchase/woStopList.html', {'woStops': books})


###################################################################
def js_list_woStop(request):
    data=dict()
    books=StopCode.objects.filter()

    data['html_woStop_list']= render_to_string('cmms/settingpages/wo_stop_code/partialWoStoplist.html', {
        'woStops': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_woStop_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = StopCode.objects.all()
                data['html_woStop_list'] = render_to_string('cmms/settingpages/wo_stop_code/partialWoStoplist.html', {
                    'woStops': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_woStop_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def woStop_delete(request, id):
    comp1 = get_object_or_404(StopCode, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = StopCode.objects.all()
        data['html_woStop_list'] = render_to_string('cmms/settingpages/wo_stop_code/partialWoStoplist.html', {
            'woStop': companies
        })
    else:
        context = {'woStop': comp1}
        data['html_woStop_form'] = render_to_string('cmms/settingpages/wo_stop_code/partialWoStopDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woStop_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['stopCode']=body['stopCode']
        data['stopDescription']=body['stopDescription']
        data['stopIsActive']=True if body['stopDescription'] is 'true' else False
        form = StopCodeForm(data)
    else:
        form = StopCodeForm()

    return save_woStop_form(request, form, 'cmms/settingpages/wo_stop_code/partialWoStopCreate.html')
###################################################################

@csrf_exempt
def woStop_update(request, id):
    company= get_object_or_404(StopCode, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['stopCode']=body['stopCode']
        data['stopDescription']=body['stopDescription']


        form = StopCodeForm(data, instance=company)
    else:
        form = StopCodeForm(instance=company)
    return save_woStop_form(request, form, 'cmms/settingpages/wo_stop_code/partialWoStopUpdate.html')
