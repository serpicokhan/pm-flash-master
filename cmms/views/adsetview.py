from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings


#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import BusinessForm
from django.urls import reverse_lazy
from django.db import transaction
from cmms.models import *

###################################################################
def not_found(request):
    # data=dict()
    # books=[]
    # books=AdminSetting.objects.all()

    # data['html_adminSetting_list']= render_to_string('cmms/AdminSetting/partialAdminSettinglist.html', {
    #     'adminSettings': books
    # })
    # data['form_is_valid']=True
    # books = Business.objects.all()
    return render(request, 'cmms/404.html', {'business':123 })
    # form = AdSetForm()
    #return JsonResponse(data)
    # return render(request, 'cmms/a123/businessList.html', {'form': form})

###################################################################    ###################################################################
# @csrf_exempt
# def save_adminSetting_form(request, form, template_name):
#         data = dict()
#         if (request.method == 'POST'):
#               if form.is_valid():
#                 form.save()
#                 # books = BusinessAsset.objects.filter(BusinessAssetAsset=woId)
#                 data['html_adminSetting_list'] = render_to_string('cmms/asset_business/partialAdminSettinglist.html', {
#                     'adminSettings': books
#                 })
#               else:
#                   pass
#                   # fmt = getattr(settings, 'LOG_FORMAT', None)
#                   # lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
#                   # logging.basicConfig(format=fmt, level=lvl)
#                   # logging.debug(form.errors)
#
#         context = {'form': form}
#         data['html_adminSetting_form'] = render_to_string(template_name, context, request=request)
#         return JsonResponse(data)
#
# ###################################################################
# ###################################################################
# @csrf_exempt
# def adminSetting_create(request):
#     # woId=-1
#     print("enter:")
#     if (request.method == 'POST'):
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#
#
#         data = request.POST.dict()
#         # data['BusinessAssetAsset']=body['BusinessAssetAsset']
#         # data['businessAdminSetting']=body['businessAdminSetting']
#         # data['businessAdminSettingType']=body['businessAdminSettingType']
#         #
#         # data['businessAssetSupplierPartNumber']=body['businessAssetSupplierPartNumber']
#         # data['businessAssetCatalog']=body['businessAssetCatalog']
#         # data['businessAssetisDefault']=True if body['businessAssetisDefault']=='true' else False
#         #
#         #
#         #
#         #
#         #
#         # woId=body['BusinessAssetAsset']
#         #
#
#
#         form = AdminSettingForm(data)
#
#
#
#     else:
#         form = AdminSettingForm()
#     print(form)
#     return save_adminSetting_form(request, form, 'cmms/adminsetting/partialAdminSettingCreate.html')
# ###################################################################
#
# @csrf_exempt
# def adminSetting_update(request, id):
#     company= get_object_or_404(AdminSetting, id=id)
#     # woId=company.BusinessAssetAsset
#     if (request.method == 'POST'):
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#
#
#         data = request.POST.dict()
#         # data['BusinessAssetAsset']=body['BusinessAssetAsset']
#         # data['businessAdminSetting']=body['businessAdminSetting']
#         # data['businessAdminSettingType']=body['businessAdminSettingType']
#         #
#         # data['businessAssetSupplierPartNumber']=body['businessAssetSupplierPartNumber']
#         # data['businessAssetCatalog']=body['businessAssetCatalog']
#         # data['businessAssetisDefault']=True if body['businessAssetisDefault']=='true' else False
#
#
#
#         form = AdminSettingForm(data, instance=company)
#     else:
#         form = AdminSettingForm(instance=company)
#     return save_adminSetting_form(request, form, 'cmms/asset_business/partialAdminSettingUpdate.html')
