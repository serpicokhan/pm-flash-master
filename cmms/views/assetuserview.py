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
from cmms.forms import AssetUserForm

###################################################################
def list_assetUser(request,id=None):
    books = AssetUser.objects.all()
    return render(request, 'cmms/asset_user/assetUserList.html', {'assetUsers': books})


###################################################################
def js_list_assetUser(request,woId):
    data=dict()
    books=AssetUser.objects.filter(AssetUserAssetId=woId)

    data['html_assetUser_list']= render_to_string('cmms/asset_user/partialAssetUserList.html', {
        'assetUsers': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_assetUser_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = AssetUser.objects.filter(AssetUserAssetId=woId)
            data['html_assetUser_list'] = render_to_string('cmms/asset_user/partialAssetUserList.html', {
                'assetUsers': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_assetUser_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def assetUser_delete(request, id):
    comp1 = get_object_or_404(AssetUser, id=id)
    data = dict()
    woId=comp1.AssetUserAssetId
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = AssetUser.objects.filter(AssetUserAssetId=woId)
        data['html_assetUser_list'] = render_to_string('cmms/asset_user/partialAssetUserList.html', {
            'assetUsers': companies
        })
    else:
        context = {'assetUser': comp1}
        data['html_assetUser_form'] = render_to_string('cmms/asset_user/partialAssetUserDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetUser_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['AssetUserAssetId']=body['AssetUserAssetId']
        data['AssetUserUserId']=body['AssetUserUserId']


        woId=body['AssetUserAssetId']

        form = AssetUserForm(data)

    else:
        form = AssetUserForm()
    return save_assetUser_form(request, form, 'cmms/asset_user/partialAssetUserCreate.html',woId)
###################################################################

@csrf_exempt
def assetUser_update(request, id):
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)

    company= get_object_or_404(AssetUser, id=id)
    woId=company.AssetUserAssetId
    logging.debug(woId)
    print(woId)
    print("update")
    if (request.method == 'POST'):
        print("update")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['AssetUserAssetId']=body['AssetUserAssetId']
        data['AssetUserUserId']=body['AssetUserUserId']



        form = AssetUserForm(data, instance=company)
    else:
        form = AssetUserForm(instance=company)
    return save_assetUser_form(request, form, 'cmms/asset_user/partialAssetUserUpdate.html',woId)
