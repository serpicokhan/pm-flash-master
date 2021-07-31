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
from cmms.forms import MeterCodeForm

###################################################################
def list_meterCode(request,id=None):
    books = ActionCode.objects.all()
    return render(request, 'cmms/part_purchase/meterCodeList.html', {'meterCodes': books})


###################################################################
def js_list_meterCode(request):
    data=dict()
    books=ActionCode.objects.filter()

    data['html_meterCode_list']= render_to_string('cmms/settingpages/meter_code/partialMeterCodelist.html', {
        'meterCodes': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_meterCode_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = ActionCode.objects.all()
                data['html_meterCode_list'] = render_to_string('cmms/settingpages/meter_code/partialMeterCodelist.html', {
                    'meterCodes': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_meterCode_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def meterCode_delete(request, id):
    comp1 = get_object_or_404(ActionCode, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = ActionCode.objects.all()
        data['html_meterCode_list'] = render_to_string('cmms/settingpages/meter_code/partialMeterCodelist.html', {
            'meterCode': companies
        })
    else:
        context = {'meterCode': comp1}
        data['html_meterCode_form'] = render_to_string('cmms/settingpages/meter_code/partialMeterCodeDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def meterCode_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['meterCode']=body['meterCode']
        data['meterDescription']=body['meterDescription']

        form = MeterCodeForm(data)
    else:
        form = MeterCodeForm()

    return save_meterCode_form(request, form, 'cmms/settingpages/meter_code/partialMeterCodeCreate.html')
###################################################################

@csrf_exempt
def meterCode_update(request, id):
    company= get_object_or_404(ActionCode, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['meterCode']=body['actionCode']
        data['meterDescription']=body['actionDescription']


        form = MeterCodeForm(data, instance=company)
    else:
        form = MeterCodeForm(instance=company)
    return save_meterCode_form(request, form, 'cmms/settingpages/meter_code/partialMeterCodeUpdate.html')
