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
from cmms.forms import AssetMeterForm
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response

###################################################################
def list_assetMeter(request,id=None):
    books = AssetMeterReading.objects.all()
    return render(request, 'cmms/asset_meter/assetMeterList.html', {'assetMeters': books})


###################################################################
def js_list_assetMeter(request,woId):
    data=dict()
    #books=AssetMeterReading.objects.filter(assetMeterLocation=woId)
    # print("select a.id, a.assetMeterMeterReading,a.assetMeterMeterReadingUnit,a.timestamp,a.assetMeterLocation_id from assetmeterreading a INNER JOIN ( select id,assetMeterMeterReadingUnit,assetMeterLocation_id,max(id) as maxid from assetmeterreading where assetMeterLocation_id="+woId+"  GROUP BY assetMeterLocation_id,assetMeterMeterReadingUnit ) b on b.maxid=a.id")
    # books=AssetMeterReading.objects.raw("select a.id, a.assetMeterMeterReading,a.assetMeterMeterReadingUnit,a.timestamp,a.assetMeterLocation_id from assetmeterreading a INNER JOIN ( select id,assetMeterMeterReadingUnit,assetMeterLocation_id,max(id) as maxid from assetmeterreading where assetMeterLocation_id="+woId+"  GROUP BY assetMeterLocation_id,assetMeterMeterReadingUnit ) b on b.maxid=a.id")
    books=AssetMeterReading.objects.filter(assetMeterLocation=woId).order_by('-id')
    data['html_assetMeter_list']= render_to_string('cmms/asset_meter/partialAssetMeterList.html', {
        'assetMeters': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################

def save_assetMeter_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            # fmt = getattr(settings, 'LOG_FORMAT', None)
            # lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            # logging.basicConfig(format=fmt, level=lvl)
            # logging.debug( woId)
            # books=AssetMeterReading.objects.raw("select a.id, a.assetMeterMeterReading,a.assetMeterMeterReadingUnit,a.timestamp,a.assetMeterLocation_id from assetmeterreading a INNER JOIN ( select id,assetMeterMeterReadingUnit,assetMeterLocation_id,max(id) as maxid from assetmeterreading where assetMeterLocation_id="+str(woId)+"  GROUP BY assetMeterLocation_id,assetMeterMeterReadingUnit ) b on b.maxid=a.id")
            books=AssetMeterReading.objects.filter(assetMeterLocation=woId).order_by('-id')
            data['html_assetMeter_list'] = render_to_string('cmms/asset_meter/partialAssetMeterList.html', {
                'assetMeters': books
            })
            print("form is valid")
          else:
              print("error occore in line 69");
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_assetMeter_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def assetMeter_delete(request, id):
    comp1 = get_object_or_404(AssetMeterReading, id=id)
    data = dict()
    woId=comp1.assetMeterLocation
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        # companies = AssetMeterReading.objects.raw("select a.id, a.assetMeterMeterReading,a.assetMeterMeterReadingUnit,a.timestamp,a.assetMeterLocation_id from assetmeterreading a INNER JOIN ( select id,assetMeterMeterReadingUnit,assetMeterLocation_id,max(id) as maxid from assetmeterreading where assetMeterLocation_id={0}  GROUP BY assetMeterLocation_id,assetMeterMeterReadingUnit ) b on b.maxid=a.id".format(woId))
        companies=AssetMeterReading.objects.filter(assetMeterLocation=woId).order_by('-id')
        data['html_assetMeter_list'] = render_to_string('cmms/asset_meter/partialAssetMeterList.html', {
            'assetMeters': companies
        })
    else:
        context = {'assetMeter': comp1}
        data['html_assetMeter_form'] = render_to_string('cmms/asset_meter/partialAssetMeterDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetMeter_create(request,id=None):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['assetMeterLocation']=body['assetMeterLocation']
        data['assetMeterMeterReading']=body['assetMeterMeterReading']
        data['assetMeterMeterReadingUnit']=body['assetMeterMeterReadingUnit']

        if(body['assetWorkorderMeterReading']!=-1):

            data['assetWorkorderMeterReading']=body['assetWorkorderMeterReading']
        else:

            data['assetWorkorderMeterReading']=None

        woId=body['assetMeterLocation']


        form = AssetMeterForm(data=data,asset_id=body['assetMeterLocation'])

    else:

        # assets=Asset.objects.get(pk=id)
        # form = AssetMeterForm(asset=id)
        form = AssetMeterForm(asset_id=id)
    return save_assetMeter_form(request, form, 'cmms/asset_meter/partialAssetMeterCreate.html',woId)
###################################################################

@csrf_exempt
def assetMeter_update(request, id):
    company= get_object_or_404(AssetMeterReading, id=id)
    woId=company.assetMeterLocation
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['assetMeterLocation']=body['assetMeterLocation']
        data['assetMeterMeterReading']=body['assetMeterMeterReading']
        data['assetMeterMeterReadingUnit']=body['assetMeterMeterReadingUnit']
        if(body['assetWorkorderMeterReading']!=-1):

                data['assetWorkorderMeterReading']=body['assetWorkorderMeterReading']
        else:

                data['assetWorkorderMeterReading']=None


        form = AssetMeterForm(data=data,instance=company,asset_id=int(data['assetMeterLocation']))
    else:
        # assets=Asset.objects.get(pk=company.assetMeterLocation.id)
        # form = AssetMeterForm(asset=company.assetMeterLocation,instance=company,initial={'assetWorkorderMeterReading': company.assetWorkorderMeterReading})
        form = AssetMeterForm(asset_id=company.assetMeterLocation.id,instance=company)
    return save_assetMeter_form(request, form, 'cmms/asset_meter/partialAssetMeterUpdate.html',woId)
@api_view(['GET'])
def assetmeter_collection(request,id):
    if request.method == 'GET':
        print("reached task")
        posts = AssetMeterReading.objects.filter(assetMeterLocation=id)
        serializer = AssetMeterReadingSerializer(posts, many=True)

        return Response(serializer.data)
@api_view(['GET'])
def assetmeter_detail_collection(request,id):
    if request.method == 'GET':
        # print("!23")
        posts = AssetMeterReading.objects.get(id=id)
        serializer = AssetMeterReadingSerializer(posts)

        return Response(serializer.data)
