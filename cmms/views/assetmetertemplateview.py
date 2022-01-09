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
from cmms.forms import AssetMeterTemplateForm

###################################################################
def list_assetMeterTemplate(request,id=None):
    books = AssetMeterTemplate.objects.all()
    return render(request, 'cmms/asset_meter_template/assetMeterTemplateList.html', {'assetMeterTemplates': books})


###################################################################
def js_list_assetMeterTemplate(request,woId):
    data=dict()
    books=AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=woId).order_by('-id')

    data['html_assetMeterTemplate_list']= render_to_string('cmms/asset_meter_template/partialAssetMeterTemplateList.html', {
        'assetMeterTemplates': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_assetMeterTemplate_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=woId).order_by('-id')
            data['html_assetMeterTemplate_list'] = render_to_string('cmms/asset_meter_template/partialAssetMeterTemplateList.html', {
                'assetMeterTemplates': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_assetMeterTemplate_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def assetMeterTemplate_delete(request, id):
    comp1 = get_object_or_404(AssetMeterTemplate, id=id)
    data = dict()
    woId=comp1.assetMeterTemplateAsset

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=woId).order_by('-id')
        data['html_assetMeterTemplate_list'] = render_to_string('cmms/asset_meter_template/partialAssetMeterTemplateList.html', {
            'assetMeterTemplates': companies
        })
    else:
        context = {'assetMeterTemplate': comp1}
        data['html_assetMeterTemplate_form'] = render_to_string('cmms/asset_meter_template/partialAssetMeterTemplateDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetMeterTemplate_create(request):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['assetMeterTemplateAsset']=body['assetMeterTemplateAsset']
        data['assetMeterTemplateMeter']=body['assetMeterTemplateMeter']
        data['assetMeterTemplateDesc']=body['assetMeterTemplateDesc']

        woId=body['assetMeterTemplateAsset']

        form = AssetMeterTemplateForm(data)

    else:
        form = AssetMeterTemplateForm()
    return save_assetMeterTemplate_form(request, form, 'cmms/asset_meter_template/partialAssetMeterTemplateCreate.html',woId)
###################################################################

@csrf_exempt
def assetMeterTemplate_update(request, id):
    company= get_object_or_404(AssetMeterTemplate, id=id)
    woId=company.assetMeterTemplateAsset
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['assetMeterTemplateAsset']=body['assetMeterTemplateAsset']
        data['assetMeterTemplateMeter']=body['assetMeterTemplateMeter']
        data['assetMeterTemplateDesc']=body['assetMeterTemplateDesc']


        form = AssetMeterTemplateForm(data, instance=company)
    else:
        form = AssetMeterTemplateForm(instance=company)
    return save_assetMeterTemplate_form(request, form, 'cmms/asset_meter_template/partialAssetMeterTemplateUpdate.html',woId)
