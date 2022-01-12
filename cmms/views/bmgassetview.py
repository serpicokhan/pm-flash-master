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
from cmms.forms import BMGAssetForm

###################################################################


###################################################################
def js_list_bmgAsset(request,woId):
    data=dict()


    books=BMGAsset.objects.filter(BMGGroup=woId)

    data['html_bmgAsset_list']= render_to_string('cmms/bmg_assets/partialBMGAssetList.html', {
        'bmgAssets': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_bmgAsset_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True


            books=BMGAsset.objects.filter(BMGGroup=woId)

            data['html_bmgAsset_list'] = render_to_string('cmms/bmg_assets/partialBMGAssetList.html', {
                'bmgAssets': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)
              data['form_is_valid'] = False

    context = {'form': form}
    data['html_bmgAsset_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def bmgAsset_delete(request, id):
    comp1 = get_object_or_404(BMGAsset, id=id)
    data = dict()
    woId=comp1.BMGGroup

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code


        books=BMGAsset.objects.filter(BMGGroup=woId)

        data['html_bmgAsset_list'] = render_to_string('cmms/bmg_assets/partialBMGAssetList.html', {
            'bmgAssets': books
        })
    else:
        context = {'bmgAsset': comp1}
        data['html_bmgAsset_form'] = render_to_string('cmms/bmg_assets/partialBMGAssetDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def bmgAsset_create(request):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['BMGGroup']=body['BMGGroup']
        data['BMGAsset']=body['BMGAsset']


        woId=body['BMGGroup']

        form = BMGAssetForm(data)

    else:
        form = BMGAssetForm()
    return save_bmgAsset_form(request, form, 'cmms/bmg_assets/partialBMGAssetCreate.html',woId)
###################################################################

@csrf_exempt
def bmgAsset_update(request, id):
    company= get_object_or_404(BMGAsset, id=id)
    woId=company.BMGGroup
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['BMGGroup']=body['BMGGroup']
        data['BMGAsset']=body['BMGAsset']



        form = BMGAssetForm(data, instance=company)
    else:
        form = BMGAssetForm(instance=company,initial={'my_asset':company.BMGAsset.assetName})
    return save_bmgAsset_form(request, form, 'cmms/bmg_assets/partialBMGAssetUpdate.html',woId.id)
