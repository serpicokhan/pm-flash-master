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
from dateutil.relativedelta import relativedelta
import dateutil.parser

import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from cmms.business.DateJob import *
from cmms.models.Asset import *

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetLifeForm
from cmms.business.updateAssetStatus import *
###################################################################
@csrf_exempt
def list_assetLife(request,id=None):
    books = AssetLife.objects.all()
    return render(request, 'cmms/asset_life/assetLifeList.html', {'assetLifes': books})


###################################################################
@csrf_exempt
def js_list_assetLife(request,woId):
    data=dict()
    books=AssetLife.objects.filter(assetLifeAssetid=woId).order_by('-id')[:5]

    data['html_assetLife_list']= render_to_string('cmms/asset_life/partialAssetLifeList.html', {
        'assetLifes': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_assetLife_form(request, form, template_name,woId=None,assetStatus=None):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                books = AssetLife.objects.filter(assetLifeAssetid_id=woId).order_by('-id')[:5]
                data['html_assetLife_list'] = render_to_string('cmms/asset_life/partialAssetLifeList.html', {
                    'assetLifes': books
                })
              else:
                  print(form.errors)

        context = {'form': form,'assetstatus':assetStatus}
        data['html_assetLife_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################

@csrf_exempt
def assetLife_delete(request, id):
    comp1 = get_object_or_404(AssetLife, id=id)
    woId=comp1.assetLifeAssetid
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = AssetLife.objects.filter(assetLifeAssetid=woId)
        data['html_assetLife_list'] = render_to_string('cmms/asset_life/partialAssetLifeList.html', {
            'assetLifes': companies
        })
    else:
        context = {'assetLife': comp1}
        data['html_assetLife_form'] = render_to_string('cmms/asset_life/partialAssetLifeDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def assetLife_create(request,assetId=None):
    woId=-1
    if(assetId!=None):
        woId=assetId

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # print(body)



        data = request.POST.dict()
        data['assetLifeAssetid']=body['assetLifeAssetid']
        data['assetOfflineFrom']=DateJob.getDate2(body['assetOfflineFrom'])
        data['assetSetOfflineByUser']=body['assetSetOfflineByUser']
        # data['assetOfflineStatus']=body['assetOfflineStatus']
        data['assetWOAssoc']=body['assetWOAssoc']
        data['assetOfflineAdditionalInfo']=body['assetOfflineAdditionalInfo']
        data['assetEventType']=body['assetEventType']
        data['assetEventDescription']=body['assetEventDescription']
        data['assetCheckEvent']=body['assetCheckEvent']
        data['assetStopCode']=body['assetStopCode']

        data['assetOfflineFromTime']=body['assetOfflineFromTime']
        woId=body['assetLifeAssetid']
        data['assetOnlineFrom']=data['assetOfflineFrom']
        data['assetOnlineFromTime']=data['assetOfflineFromTime']
        data['assetCauseCode']=body['assetCauseCode']

        # print("dsadsadsa%%%%%%%"+str(body['assetOnlineStatus']))
        # asset1=Asset.objects.get(pk=int(woId))

        if ("assetOnlineStatus" in body and body['assetOnlineStatus']!=-1):


            data['assetOnlineFrom']=DateJob.getDate2(body['assetOnlineFrom'])
            data['assetSetOnlineByUser']=body['assetSetOnlineByUser']
            data['assetOnlineStatus']=body['assetOnlineStatus']
            data['assetOnlineAdditionalInfo']=body['assetOnlineAdditionalInfo']
            data['assetOnlineProducteHourAffected']=body['assetOnlineProducteHourAffected']
            data['assetOnlineFromTime']=body['assetOnlineFromTime']
            # time1 = data['assetOfflineFromTime']
            # time2 = data['assetOnlineFromTime']
            # format = "%H:%M"
            # t1 = datetime.strptime(time1, format)
            # t2 = datetime.strptime(time2, format)
            # asset1.assetStatus=True
            # asset1.save()
            # print(asset1,"if#####################")
        else:
            pass






        if(data['assetCheckEvent']==True):
            AssetEvent.objects.create(AssetEventAssetId_id=woId,AssetEventEventId_id=data['assetEventType'])
        # else:
        #     af=AssetEvent.objects.filter(AssetEventAssetId_id=woId,AssetEventEventId_id=data['assetEventType'])
        #     if(af):
        #         af.delete();

        form = AssetLifeForm(data)
        # AssetStatus.ReverseAssetStatus(woId)




    else:
        # al=AssetLife.objects.filter(assetLifeAssetid=assetId)
        asset_name=Asset.objects.get(id=assetId).assetName
        form = AssetLifeForm(initial={'asset_name':asset_name,'assetLifeAssetid':assetId,'assetSetOfflineByUser':SysUser.objects.get(userId=request.user)})

    return save_assetLife_form(request, form, 'cmms/asset_life/partialAssetLifeCreate.html',woId,False)
###################################################################

@csrf_exempt
def assetLife_update(request, id):
    company= get_object_or_404(AssetLife, id=id)
    woId=company.assetLifeAssetid
    asset_name=company.assetLifeAssetid.assetName
    print("{}".format(woId.assetStatus))
    assetStatus=False
    #parrent asset
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['assetLifeAssetid']=body['assetLifeAssetid']
        data['assetOfflineFrom']=DateJob.getDate2(body['assetOfflineFrom'])#DateJob.getDate(body['assetOfflineFrom'])
        data['assetSetOfflineByUser']=body['assetSetOfflineByUser']
        # data['assetOfflineStatus']=body['assetOfflineStatus']
        data['assetWOAssoc']=body['assetWOAssoc']
        data['assetOfflineAdditionalInfo']=body['assetOfflineAdditionalInfo']
        data['assetEventType']=body['assetEventType']
        data['assetEventDescription']=body['assetEventDescription']
        data['assetCheckEvent']=body['assetCheckEvent']
        data['assetStopCode']=body['assetStopCode']
        data['assetOfflineFromTime']=body['assetOfflineFromTime']
        data['assetCauseCode']=body['assetCauseCode']

        if ("assetOnlineStatus" in body and body['assetOnlineStatus']!=-1):
            data['assetOnlineFrom']=DateJob.getDate2(body['assetOnlineFrom'])#DateJob.getDate(body['assetOnlineFrom'])
            data['assetSetOnlineByUser']=body['assetSetOnlineByUser']
            data['assetOnlineStatus']=body['assetOnlineStatus']
            data['assetOnlineAdditionalInfo']=body['assetOnlineAdditionalInfo']
            data['assetOnlineProducteHourAffected']=body['assetOnlineProducteHourAffected']
            # print("assetOnlineStatus :"+str(body['assetOnlineStatus']))
            data['assetOnlineFromTime']=body['assetOnlineFromTime']
            assetStatus=True
            woId.assetStatus=True
            woId.save()
            # print("{}".format(woId.assetStatus))
        else:
            woId.assetStatus=False;
            woId.save()



        if(company.assetCheckEvent==False):
            if(data['assetCheckEvent']==True):
                AssetEvent.objects.create(AssetEventAssetId=woId,AssetEventEventId_id=data['assetEventType'])
            # else:

        else:
            if(data['assetCheckEvent']==False):
                    af=AssetEvent.objects.filter(AssetEventAssetId=woId,AssetEventEventId_id=data['assetEventType'])
                    if(af):
                        af.delete();



        form = AssetLifeForm(data, instance=company)
        woId.save()
    else:
         form = AssetLifeForm(instance=company,initial={'asset_name':asset_name,'woName':company.assetWOAssoc,'assetSetOnlineByUser':SysUser.objects.get(userId=request.user)})
    return save_assetLife_form(request, form, 'cmms/asset_life/partialAssetLifeUpdate.html',woId.id,assetStatus)
###################################################################    ###################################################################
@csrf_exempt
def findLastOpenAssetLife(request,assetId):

    lastAssetLife=AssetLife.objects.filter(assetLifeAssetid=assetId).filter(assetOnlineStatus__isnull=True).order_by('-id')
    if not lastAssetLife:
        return assetLife_create(request,assetId)
    else:
        return assetLife_update(request,lastAssetLife[0].id)
