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

from cmms.models.workorder import *

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetExceptionForm
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
###################################################################
def list_assetException(request,id=None):
    books = AssetException.objects.all()
    return render(request, 'cmms/part_purchase/assetExceptionList.html', {'assetExceptions': books})


###################################################################
def js_list_assetException(request):
    data=dict()
    books=AssetException.objects.filter()

    data['html_assetException_list']= render_to_string('cmms/settingpages/asset_exception/partialAssetExceptionList.html', {
        'assetExceptions': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_assetException_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = AssetException.objects.all()
                data['html_assetException_list'] = render_to_string('cmms/settingpages/asset_exception/partialAssetExceptionList.html', {
                    'assetExceptions': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_assetException_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def assetException_delete(request, id):
    comp1 = get_object_or_404(AssetException, id=id)
    data = dict()

    comp1.delete()
    data['form_is_valid'] = True  # This is just to play along with the existing code
    companies = AssetException.objects.all()
    data['html_assetException_list'] = render_to_string('cmms/settingpages/asset_exception/partialAssetExceptionList.html', {
        'assetExceptions': companies
    })
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetException_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['assetExceptionAsset']=body['assetExceptionAsset']
        # data['meterDescription']=body['meterDescription']
        # data['meterAbbr']=body['meterAbbr']

        form = AssetExceptionForm(data)
    else:
        form = AssetExceptionForm()

    return save_assetException_form(request, form, 'cmms/settingpages/asset_exception/partialAssetExceptionCreate.html')
###################################################################

@csrf_exempt
def assetException_update(request, id):
    company= get_object_or_404(AssetException, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['assetExceptionAsset']=body['assetExceptionAsset']
        # data['meterDescription']=body['meterDescription']
        # data['meterAbbr']=body['meterAbbr']


        form = AssetExceptionForm(data, instance=company)
    else:
        form = AssetExceptionForm(instance=company)
    return save_assetException_form(request, form, 'cmms/settingpages/asset_exception/partialAssetExceptionUpdate.html')
@api_view(['GET'])
def metercode_collection(request):
    if request.method == 'GET':
        posts = AssetException.objects.all()
        serializer = AssetExceptionSerializer(posts, many=True)
        return Response(serializer.data)
