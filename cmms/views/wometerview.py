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
from cmms.models.Asset import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import WoMeterForm,AssetMeterForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper

###################################################################
def list_woMeter(request,id=None):
    books = WorkorderMeterReading.objects.all()
    return render(request, 'cmms/wo_meter/woMeterList.html', {'woMeters': books})


###################################################################
@permission_required('cmms.view_workordermeterreading')
def js_list_woMeter(request,woId):
    data=dict()
    books=AssetMeterReading.objects.filter(assetWorkorderMeterReading=woId)

    data['html_woMeter_list']= render_to_string('cmms/wo_meter/partialWoMeterList.html', {
        'woMeters': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_woMeter_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books=AssetMeterReading.objects.filter(assetWorkorderMeterReading=woId)
            data['html_woMeter_list'] = render_to_string('cmms/wo_meter/partialWoMeterList.html', {
                'woMeters': books,
                'perms': PermWrapper(request.user)
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_woMeter_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def woMeter_delete(request, id):
    comp1 = get_object_or_404(AssetMeterReading, id=id)
    data = dict()
    woId=comp1.assetWorkorderMeterReading
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = AssetMeterReading.objects.filter(assetWorkorderMeterReading=woId)
        data['html_woMeter_list'] = render_to_string('cmms/wo_meter/partialWoMeterList.html', {
            'woMeters': companies
        })
    else:
        context = {'woMeter': comp1}
        data['html_woMeter_form'] = render_to_string('cmms/wo_meter/partialWoMeterDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woMeter_create(request,id=None):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['assetWorkorderMeterReading']=body['woMeterReadingworkorder']
        data['assetMeterLocation']=body['woMeterReadingLocation']
        data['assetMeterMeterReading']=body['woMeterReadingMeterReading']
        data['assetMeterMeterReadingUnit']=body['woMeterReadingMeterReadingUnit']
        woId=body['woMeterReadingworkorder']

        form = AssetMeterForm(data,asset_id=int(data['assetMeterLocation']))

    else:
        a_id=WorkOrder.objects.get(id=id)
        form = AssetMeterForm(asset_id=a_id.woAsset.id)
    return save_woMeter_form(request, form, 'cmms/wo_meter/partialWoMeterCreate.html',woId)
###################################################################

@csrf_exempt
def woMeter_update(request, id):
    company= get_object_or_404(AssetMeterReading, id=id)
    woId=company.assetWorkorderMeterReading
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()

        data['assetWorkorderMeterReading']=body['woMeterReadingworkorder']
        data['assetMeterLocation']=body['woMeterReadingLocation']
        data['assetMeterMeterReading']=body['woMeterReadingMeterReading']
        data['assetMeterMeterReadingUnit']=body['woMeterReadingMeterReadingUnit']
        woId=body['woMeterReadingworkorder']
        form = AssetMeterForm(data, instance=company,asset_id=company.assetMeterLocation)
    else:
        form = AssetMeterForm(instance=company,asset_id=company.assetMeterLocation.id)
    return save_woMeter_form(request, form, 'cmms/wo_meter/partialWoMeterUpdate.html',woId)
