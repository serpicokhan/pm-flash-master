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
from cmms.models.waranty import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetWarantyForm

###################################################################
def list_assetWaranty(request,id=None):
    books = Waranty.objects.all()
    return render(request, 'cmms/asset_waranty/assetWarantyList.html', {'assetWarantys': books})


###################################################################
def js_list_assetWaranty(request,woId):
    data=dict()
    books=Waranty.objects.filter(warantyLocation=woId)

    data['html_assetWaranty_list']= render_to_string('cmms/asset_waranty/partialAssetWarantyList.html', {
        'assetWarantys': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_assetWaranty_form(request, form, template_name,woId=None):
        data = dict()


        if (request.method == 'POST'):
              print(request.POST)
              print("here is good")

              if form.is_valid():

                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                logging.debug( woId)
                books = Waranty.objects.filter(warantyLocation=woId)
                data['html_assetWaranty_list'] = render_to_string('cmms/asset_waranty/partialAssetWarantyList.html', {
                    'assetWarantys': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_assetWaranty_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################

@csrf_exempt
def assetWaranty_delete(request, id):
    comp1 = get_object_or_404(Waranty, id=id)
    data = dict()
    woId=comp1.warantyLocation
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = Waranty.objects.filter(warantyLocation=woId)
        data['html_assetWaranty_list'] = render_to_string('cmms/asset_waranty/partialAssetWarantyList.html', {
            'assetWarantys': companies
        })
    else:
        context = {'assetWaranty': comp1}
        data['html_assetWaranty_form'] = render_to_string('cmms/asset_waranty/partialAssetWarantyDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetWaranty_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['warantyType']=body['warantyType']
        data['warantyProvider']=body['warantyProvider']
        data['warantyUsageTermType']=body['warantyUsageTermType']

        data['warantyExpirationDate']=body['warantyExpirationDate']
        data['warantyCertificationNumber']=body['warantyCertificationNumber']
        data['warantyDescription']=body['warantyDescription']
        data['warantyLocation']=body['warantyLocation']
        if(str(body["warantyUsageTermType"])=="2"):
            data['warantyMeterReadingValueLimit']=body['warantyMeterReadingValueLimit']
            data['warantyMeterReadingUnit']=body['warantyMeterReadingUnit']
        elif(str(body["warantyUsageTermType"])=="3"):
             data['warantyMeterReadingValueLimit']=body['warantyMeterReadingValueLimit']
             data['warantyMeterReadingUnit']=body['warantyMeterReadingUnit']



        woId=body['warantyLocation']



        form = AssetWarantyForm(data)



    else:
        form = AssetWarantyForm()
    print(form)
    return save_assetWaranty_form(request, form, 'cmms/asset_waranty/partialAssetWarantyCreate.html',woId)
###################################################################

@csrf_exempt
def assetWaranty_update(request, id):
    company= get_object_or_404(Waranty, id=id)
    woId=company.warantyLocation
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['warantyType']=body['warantyType']
        data['warantyProvider']=body['warantyProvider']
        data['warantyUsageTermType']=body['warantyUsageTermType']

        data['warantyExpirationDate']=body['warantyExpirationDate']
        data['warantyCertificationNumber']=body['warantyCertificationNumber']
        data['warantyDescription']=body['warantyDescription']
        data['warantyLocation']=body['warantyLocation']
        if(str(body["warantyUsageTermType"])=="2"):
            data['warantyMeterReadingValueLimit']=body['warantyMeterReadingValueLimit']
            data['warantyMeterReadingUnit']=body['warantyMeterReadingUnit']
        elif(str(body["warantyUsageTermType"])=="3"):
             data['warantyMeterReadingValueLimit']=body['warantyMeterReadingValueLimit']
             data['warantyMeterReadingUnit']=body['warantyMeterReadingUnit']


        form = AssetWarantyForm(data, instance=company)
    else:
        form = AssetWarantyForm(instance=company)
    return save_assetWaranty_form(request, form, 'cmms/asset_waranty/partialAssetWarantyUpdate.html',woId)
