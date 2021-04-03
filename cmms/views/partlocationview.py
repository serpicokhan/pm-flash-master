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
from cmms.models.Asset import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PartLocationForm

###################################################################
def list_partLocation(request,id=None):
    books = AssetPart.objects.all()
    return render(request, 'cmms/workorder_parts/partLocationList.html', {'partLocations': books})


###################################################################
def js_list_partLocation(request,woId):
    data=dict()
    query="select id as id,assetPartAssetid_id,sum(assetPartQnty) as assetPartQnty from assetpart where  assetPartPid_id group by assetPartAssetid_id,AssetPartPid_id".format(woId)
    #print(query)
    books=AssetPart.objects.raw(query)

    data['html_partLocation_list']= render_to_string('cmms/part_location/partialPartLocationList.html', {
        'partLocations': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_partLocation_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            query="select id as id,assetPartAssetid_id,sum(assetPartQnty) as assetPartQnty from assetpart where  assetPartPid_id group by assetPartAssetid_id,AssetPartPid_id".format(woId)

            books=AssetPart.objects.raw(query)
            data['html_partLocation_list'] = render_to_string('cmms/part_location/partialPartLocationList.html', {
                'partLocations': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_partLocation_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################


def partLocation_delete(request, id):
    comp1 = get_object_or_404(AssetPart, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        query="select id as id,assetPartAssetid_id,sum(assetPartQnty) as assetPartQnty from assetpart where  assetPartPid_id group by assetPartAssetid_id,AssetPartPid_id".format(woId)

        companies=AssetPart.objects.raw(query)
        data['html_partLocation_list'] = render_to_string('cmms/workorder_parts/partialPartLocationList.html', {
            'partLocation': companies
        })
    else:
        context = {'partLocation': comp1}
        data['html_partLocation_form'] = render_to_string('cmms/workorder_parts/partialPartLocationDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def partLocation_create(request):
    woId=-1


    if (request.method == 'POST'):

        body_unicode = request.body.decode('utf-8')

        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['assetPartAssetid']=body['assetPartAssetid']
        data['assetPartPid']=body['assetPartPid']
        data['assetPartQnty']=body['assetPartQnty']
        woId=body['assetPartPid']
        form = PartLocationForm(data)


    else:
        form = PartLocationForm()
    return save_partLocation_form(request, form, 'cmms/part_location/partialPartLocationCreate.html',woId)
###################################################################

@csrf_exempt
def partLocation_update(request, id):
    company= get_object_or_404(AssetPart, id=id)
    woId=company.assetPartPid
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['assetPartAssetid']=body['assetPartAssetid']
        data['assetPartPid']=body['assetPartPid']
        data['assetPartQnty']=body['assetPartQnty']
        form = PartLocationForm(data, instance=company)
    else:
        form = PartLocationForm(instance=company)
    return save_partLocation_form(request, form, 'cmms/part_location/partialPartLocationUpdate.html',woId)
