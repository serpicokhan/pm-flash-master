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

from cmms.models.Asset import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetEventForm

###################################################################
def list_assetEvent(request,id=None):
    books = AssetEvent.objects.all()
    return render(request, 'cmms/asset_event/assetEventList.html', {'assetEvents': books})


###################################################################
def js_list_assetEvent(request,woId):
    data=dict()
    books=AssetEvent.objects.filter(AssetEventAssetId=woId).order_by('-id')

    data['html_assetEvent_list']= render_to_string('cmms/asset_event/partialAssetEventList.html', {
        'assetEvents': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_assetEvent_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = AssetEvent.objects.filter(AssetEventAssetId=woId).order_by('-id')
            data['html_assetEvent_list'] = render_to_string('cmms/asset_event/partialAssetEventList.html', {
                'assetEvents': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_assetEvent_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def assetEvent_delete(request, id):
    comp1 = get_object_or_404(AssetEvent, id=id)
    data = dict()
    woId=comp1.AssetEventAssetId

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = AssetEvent.objects.filter(AssetEventAssetId=woId).order_by('-id')
        data['html_assetEvent_list'] = render_to_string('cmms/asset_event/partialAssetEventList.html', {
            'assetEvents': companies
        })
    else:
        context = {'assetEvent': comp1}
        data['html_assetEvent_form'] = render_to_string('cmms/asset_event/partialAssetEventDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetEvent_create(request):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['AssetEventAssetId']=body['AssetEventAssetId']
        data['AssetEventEventId']=body['AssetEventEventId']
        data['AssetEventAdditionalDescription']=body['AssetEventAdditionalDescription']

        woId=body['AssetEventAssetId']

        form = AssetEventForm(data)

    else:
        form = AssetEventForm()
    return save_assetEvent_form(request, form, 'cmms/asset_event/partialAssetEventCreate.html',woId)
###################################################################

@csrf_exempt
def assetEvent_update(request, id):
    company= get_object_or_404(AssetEvent, id=id)
    woId=company.AssetEventAssetId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['AssetEventAssetId']=body['AssetEventAssetId']
        data['AssetEventEventId']=body['AssetEventEventId']
        data['AssetEventAdditionalDescription']=body['AssetEventAdditionalDescription']


        form = AssetEventForm(data, instance=company)
    else:
        form = AssetEventForm(instance=company)
    return save_assetEvent_form(request, form, 'cmms/asset_event/partialAssetEventUpdate.html',woId)
