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

from cmms.models.parts import *
from cmms.models.waranty import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PartWarantyForm

###################################################################
def list_partWaranty(request,id=None):
    books = PartWaranty.objects.all()
    return render(request, 'cmms/part_waranty/partWarantyList.html', {'partWarantys': books})


###################################################################
def js_list_partWaranty(request,woId):
    data=dict()
    books=PartWaranty.objects.filter(warantyStockItem=woId)

    data['html_partWaranty_list']= render_to_string('cmms/part_waranty/partialPartWarantyList.html', {
        'partWarantys': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_partWaranty_form(request, form, template_name,woId=None):
        data = dict()


        if (request.method == 'POST'):
              # print(request.POST)
              # print("here is good")

              if form.is_valid():

                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                logging.debug( woId)
                books = PartWaranty.objects.filter(warantyStockItem=woId)
                data['html_partWaranty_list'] = render_to_string('cmms/part_waranty/partialPartWarantyList.html', {
                    'partWarantys': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_partWaranty_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################

@csrf_exempt
def partWaranty_delete(request, id):
    comp1 = get_object_or_404(PartWaranty, id=id)
    data = dict()
    woId=comp1.warantyStockItem

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = PartWaranty.objects.filter(warantyStockItem=woId)
        data['html_partWaranty_list'] = render_to_string('cmms/part_waranty/partialPartWarantyList.html', {
            'partWarantys': companies
        })
    else:
        context = {'partWaranty': comp1}
        data['html_partWaranty_form'] = render_to_string('cmms/part_waranty/partialPartWarantyDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def partWaranty_create(request):
    woId=-1
    # print("enter:")
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
        data['warantyStockItem']=body['warantyStockItem']
        if(str(body["warantyUsageTermType"])=="2"):
            data['warantyMeterReadingValueLimit']=body['warantyMeterReadingValueLimit']
            data['warantyMeterReadingUnit']=body['warantyMeterReadingUnit']
        elif(str(body["warantyUsageTermType"])=="3"):
             data['warantyMeterReadingValueLimit']=body['warantyMeterReadingValueLimit']
             data['warantyMeterReadingUnit']=body['warantyMeterReadingUnit']



        woId=body['warantyStockItem']



        form = PartWarantyForm(data)



    else:
        form = PartWarantyForm()
    # print(form)
    return save_partWaranty_form(request, form, 'cmms/part_waranty/partialPartWarantyCreate.html',woId)
###################################################################

@csrf_exempt
def partWaranty_update(request, id):
    company= get_object_or_404(PartWaranty, id=id)
    woId=company.warantyStockItem
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
        data['warantyStockItem']=body['warantyStockItem']
        if(str(body["warantyUsageTermType"])=="2"):
            data['warantyMeterReadingValueLimit']=body['warantyMeterReadingValueLimit']
            data['warantyMeterReadingUnit']=body['warantyMeterReadingUnit']
        elif(str(body["warantyUsageTermType"])=="3"):
             data['warantyMeterReadingValueLimit']=body['warantyMeterReadingValueLimit']
             data['warantyMeterReadingUnit']=body['warantyMeterReadingUnit']


        form = PartWarantyForm(data, instance=company)
    else:
        form = PartWarantyForm(instance=company)
    return save_partWaranty_form(request, form, 'cmms/part_waranty/partialPartWarantyUpdate.html',woId)
