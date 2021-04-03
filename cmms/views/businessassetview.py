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
from cmms.forms import BusinessAssetForm

###################################################################
def list_businessAsset(request,id=None):
    books = BusinessAsset.objects.all()
    return render(request, 'cmms/business_asset/businessAssetList.html', {'businessAssets': books})


###################################################################
def js_list_businessAsset(request,woId):
    data=dict()
    books=BusinessAsset.objects.filter(businessAssetBusiness=woId)

    data['html_businessAsset_list']= render_to_string('cmms/business_asset/partialBusinessAssetList.html', {
        'businessAssets': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_businessAsset_form(request, form, template_name,woId=None):
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
                books = BusinessAsset.objects.filter(businessAssetBusiness=woId)
                data['html_businessAsset_list'] = render_to_string('cmms/business_asset/partialBusinessAssetList.html', {
                    'businessAssets': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_businessAsset_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def businessAsset_delete(request, id):
    comp1 = get_object_or_404(BusinessAsset, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = BusinessAsset.objects.all()
        data['html_businessAsset_list'] = render_to_string('cmms/business_asset/partialBusinessAssetList.html', {
            'businessAsset': companies
        })
    else:
        context = {'businessAsset': comp1}
        data['html_businessAsset_form'] = render_to_string('cmms/business_asset/partialBusinessAssetDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def businessAsset_create(request):
    woId=-1
    # print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['businessAssetBusiness']=body['businessAssetBusiness']
        data['BusinessAssetAsset']=body['BusinessAssetAsset']
        data['businessAssetBusinessType']=body['businessAssetBusinessType']

        data['businessAssetSupplierPartNumber']=body['businessAssetSupplierPartNumber']
        data['businessAssetCatalog']=body['businessAssetCatalog']
        data['businessAssetisDefault']=True if body['businessAssetisDefault']=='true' else False





        woId=body['businessAssetBusiness']



        form = BusinessAssetForm(data)



    else:
        form = BusinessAssetForm()
    # print(form)
    return save_businessAsset_form(request, form, 'cmms/business_asset/partialBusinessAssetCreate.html',woId)
###################################################################

@csrf_exempt
def businessAsset_update(request, id):
    company= get_object_or_404(BusinessAsset, id=id)
    woId=company.businessAssetBusiness
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['businessAssetBusiness']=body['businessAssetBusiness']
        data['BusinessAssetAsset']=body['BusinessAssetAsset']
        data['businessAssetBusinessType']=body['businessAssetBusinessType']

        data['businessAssetSupplierPartNumber']=body['businessAssetSupplierPartNumber']
        data['businessAssetCatalog']=body['businessAssetCatalog']
        data['businessAssetisDefault']=True if body['businessAssetisDefault']=='true' else False



        form = BusinessAssetForm(data, instance=company)
    else:
        form = BusinessAssetForm(instance=company)
    return save_businessAsset_form(request, form, 'cmms/business_asset/partialBusinessAssetUpdate.html',woId)
