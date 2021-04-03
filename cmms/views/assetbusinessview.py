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
from cmms.forms import AssetBusinessForm

###################################################################
def list_assetBusiness(request,id=None):
    books = BusinessAsset.objects.all()
    return render(request, 'cmms/asset_business/assetBusinessList.html', {'assetBusinesss': books})


###################################################################
def js_list_assetBusiness(request,woId):
    data=dict()
    books=BusinessAsset.objects.filter(BusinessAssetAsset=woId)

    data['html_assetBusiness_list']= render_to_string('cmms/asset_business/partialAssetBusinessList.html', {
        'assetBusinesss': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_assetBusiness_form(request, form, template_name,woId=None):
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
                books = BusinessAsset.objects.filter(BusinessAssetAsset=woId)
                data['html_assetBusiness_list'] = render_to_string('cmms/asset_business/partialAssetBusinessList.html', {
                    'assetBusinesss': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_assetBusiness_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################

@csrf_exempt
def assetBusiness_delete(request, id):
    comp1 = get_object_or_404(BusinessAsset, id=id)
    data = dict()
    woId=comp1.BusinessAssetAsset
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = BusinessAsset.objects.filter(BusinessAssetAsset=woId)
        data['html_assetBusiness_list'] = render_to_string('cmms/asset_business/partialAssetBusinessList.html', {
            'assetBusinesss': companies
        })
    else:
        context = {'assetBusiness': comp1}
        data['html_assetBusiness_form'] = render_to_string('cmms/asset_business/partialAssetBusinessDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetBusiness_create(request):
    woId=-1
    # print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['BusinessAssetAsset']=body['BusinessAssetAsset']
        data['businessAssetBusiness']=body['businessAssetBusiness']
        data['businessAssetBusinessType']=body['businessAssetBusinessType']

        data['businessAssetSupplierPartNumber']=body['businessAssetSupplierPartNumber']
        data['businessAssetCatalog']=body['businessAssetCatalog']
        data['businessAssetisDefault']=True if body['businessAssetisDefault']=='true' else False





        woId=body['BusinessAssetAsset']



        form = AssetBusinessForm(data)



    else:
        form = AssetBusinessForm()
    # print(form)
    return save_assetBusiness_form(request, form, 'cmms/asset_business/partialAssetBusinessCreate.html',woId)
###################################################################

@csrf_exempt
def assetBusiness_update(request, id):
    company= get_object_or_404(BusinessAsset, id=id)
    woId=company.BusinessAssetAsset
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['BusinessAssetAsset']=body['BusinessAssetAsset']
        data['businessAssetBusiness']=body['businessAssetBusiness']
        data['businessAssetBusinessType']=body['businessAssetBusinessType']

        data['businessAssetSupplierPartNumber']=body['businessAssetSupplierPartNumber']
        data['businessAssetCatalog']=body['businessAssetCatalog']
        data['businessAssetisDefault']=True if body['businessAssetisDefault']=='true' else False



        form = AssetBusinessForm(data, instance=company)
    else:
        form = AssetBusinessForm(instance=company)
    return save_assetBusiness_form(request, form, 'cmms/asset_business/partialAssetBusinessUpdate.html',woId)
