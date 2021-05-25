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

from cmms.models.eqcostsetting import *

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import DashAssetForm

###################################################################



###################################################################
def js_list_dashAsset(request):
    data=dict()
    books=AssetTypeSetting.objects.all()

    data['html_dashAsset_list']= render_to_string('cmms/settingpages/dash_asset/partialDashAssetList.html', {
        'dashAssets': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_dashAsset_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              # print("here!")
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                
                books = AssetTypeSetting.objects.all()
                data['html_dashAsset_list'] = render_to_string('cmms/settingpages/dash_asset/partialDashAssetList.html', {
                    'dashAssets': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_dashAsset_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def dashAsset_delete(request, id):
    comp1 = get_object_or_404(AssetTypeSetting, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = AssetTypeSetting.objects.all()
        data['html_dashAsset_list'] = render_to_string('cmms/settingpages/dash_asset/partialDashAssetList.html', {
            'dashAsset': companies
        })
    else:
        context = {'dashAsset': comp1}
        data['html_dashAsset_form'] = render_to_string('cmms/settingpages/dash_asset/partialDashAssetDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def dashAsset_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['settingEqAsset']=body['settingEqAsset']
        data['settingLocation']=body['settingLocation']
        print(data)
        form = DashAssetForm(data)
    else:
        form = DashAssetForm()

    return save_dashAsset_form(request, form, 'cmms/settingpages/dash_asset/partialDashAssetCreate.html')
###################################################################

@csrf_exempt
def dashAsset_update(request, id):
    company= get_object_or_404(AssetTypeSetting, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['settingEqAsset']=body['settingEqAsset']
        data['settingLocation']=body['settingLocation']


        form = DashAssetForm(data, instance=company)
    else:
        form = DashAssetForm(instance=company)
    return save_dashAsset_form(request, form, 'cmms/settingpages/dash_asset/partialDashAssetUpdate.html')
