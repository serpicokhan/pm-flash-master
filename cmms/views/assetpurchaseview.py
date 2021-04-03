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
from cmms.forms import AssetPurchaseForm

###################################################################
def list_assetPurchase(request,id=None):
    books = Purchase.objects.all()
    return render(request, 'cmms/asset_purchase/assetPurchaseList.html', {'assetPurchases': books})


###################################################################
def js_list_assetPurchase(request,woId):
    data=dict()
    books=Purchase.objects.filter(purchaseAssetId=woId)

    data['html_assetPurchase_list']= render_to_string('cmms/asset_purchase/partialAssetPurchaseList.html', {
        'assetPurchases': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_assetPurchase_form(request, form, template_name,woId=None):
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
                books = Purchase.objects.filter(purchaseAssetId=woId)
                data['html_assetPurchase_list'] = render_to_string('cmms/asset_purchase/partialAssetPurchaseList.html', {
                    'assetPurchases': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_assetPurchase_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################

@csrf_exempt
def assetPurchase_delete(request, id):
    comp1 = get_object_or_404(Purchase, id=id)
    data = dict()
    woId=comp1.purchaseAssetId
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = Purchase.objects.filter(purchaseAssetId=woId)
        data['html_assetPurchase_list'] = render_to_string('cmms/asset_purchase/partialAssetPurchaseList.html', {
            'assetPurchases': companies
        })
    else:
        context = {'assetPurchase': comp1}
        data['html_assetPurchase_form'] = render_to_string('cmms/asset_purchase/partialAssetPurchaseDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetPurchase_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['purchaseAssetId']=body['purchaseAssetId']
        data['purchaseDateOrdered']=body['purchaseDateOrdered']
        data['purchasePriceTotla']=body['purchasePriceTotla']

        data['purchaseCurrency']=body['purchaseCurrency']
        data['purchaseDateRecieved']=body['purchaseDateRecieved']
        data['purchaseDateofExpire']=body['purchaseDateofExpire']
        data['purchasedFrom']=body['purchasedFrom']
        data['purchaseUser']=body['purchaseUser']





        woId=body['purchaseAssetId']



        form = AssetPurchaseForm(data)



    else:
        form = AssetPurchaseForm()
    # print(form)
    return save_assetPurchase_form(request, form, 'cmms/asset_purchase/partialAssetPurchaseCreate.html',woId)
###################################################################

@csrf_exempt
def assetPurchase_update(request, id):
    company= get_object_or_404(Purchase, id=id)
    woId=company.purchaseAssetId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['purchaseAssetId']=body['purchaseAssetId']
        data['purchaseDateOrdered']=body['purchaseDateOrdered']
        data['purchasePriceTotla']=body['purchasePriceTotla']

        data['purchaseCurrency']=body['purchaseCurrency']
        data['purchaseDateRecieved']=body['purchaseDateRecieved']
        data['purchaseDateofExpire']=body['purchaseDateofExpire']
        data['purchasedFrom']=body['purchasedFrom']
        data['purchaseUser']=body['purchaseUser']

        form = AssetPurchaseForm(data, instance=company)
    else:
        form = AssetPurchaseForm(instance=company)
    return save_assetPurchase_form(request, form, 'cmms/asset_purchase/partialAssetPurchaseUpdate.html',woId)
