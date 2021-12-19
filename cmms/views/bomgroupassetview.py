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
from cmms.forms import BOMGroupAssetForm

###################################################################


###################################################################
def js_list_bomGroupAsset(request,woId):
    data=dict()


    books=BOMGroupAsset.objects.filter(BOMGroupAssetBOMGroup=woId)

    data['html_bomGroupAsset_list']= render_to_string('cmms/bomgroup_assets/partialBOMGroupAssetList.html', {
        'bomGroupAssets': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_bomGroupAsset_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True


            books=BOMGroupAsset.objects.filter(BOMGroupAssetBOMGroup=woId)

            data['html_bomGroupAsset_list'] = render_to_string('cmms/bomgroup_assets/partialBOMGroupAssetList.html', {
                'bomGroupAssets': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)
              data['form_is_valid'] = False

    context = {'form': form}
    data['html_bomGroupAsset_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def bomGroupAsset_delete(request, id):
    comp1 = get_object_or_404(BOMGroupAsset, id=id)
    data = dict()
    woId=comp1.BOMGroupAssetBOMGroup

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code


        books=BOMGroupAsset.objects.filter(BOMGroupAssetBOMGroup=woId)

        data['html_bomGroupAsset_list'] = render_to_string('cmms/bomgroup_assets/partialBOMGroupAssetList.html', {
            'bomGroupAssets': books
        })
    else:
        context = {'bomGroupAsset': comp1}
        data['html_bomGroupAsset_form'] = render_to_string('cmms/bomgroup_assets/partialBOMGroupAssetDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def bomGroupAsset_create(request):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['BOMGroupAssetBOMGroup']=body['BOMGroupAssetBOMGroup']
        data['BOMGroupAssetAsset']=body['BOMGroupAssetAsset']


        woId=body['BOMGroupAssetBOMGroup']

        form = BOMGroupAssetForm(data)

    else:
        form = BOMGroupAssetForm()
    return save_bomGroupAsset_form(request, form, 'cmms/bomgroup_assets/partialBOMGroupAssetCreate.html',woId)
###################################################################

@csrf_exempt
def bomGroupAsset_update(request, id):
    company= get_object_or_404(BOMGroupAsset, id=id)
    woId=company.BOMGroupAssetBOMGroup
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['BOMGroupAssetBOMGroup']=body['BOMGroupAssetBOMGroup']
        data['BOMGroupAssetAsset']=body['BOMGroupAssetAsset']



        form = BOMGroupAssetForm(data, instance=company)
    else:
        form = BOMGroupAssetForm(instance=company,initial={'my_asset':company.BOMGroupAssetAsset.assetName})
    return save_bomGroupAsset_form(request, form, 'cmms/bomgroup_assets/partialBOMGroupAssetUpdate.html',woId.id)
