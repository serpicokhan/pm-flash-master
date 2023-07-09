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
from cmms.forms import BOMGroupAssetForm,BOMGroupAssetForm2
from django.db import IntegrityError
from django.db.models import Q
from cmms.business.AssetUtility import AssetUtility

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
    context={}
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True


            books=BOMGroupAsset.objects.filter(BOMGroupAssetBOMGroup=woId)

            data['html_bomGroupAsset_list'] = render_to_string('cmms/bomgroup_assets/partialBOMGroupAssetList.html', {
                'bomGroupAssets': books
            })
            context = {'form': form}
          else:

              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)
              data['form_is_valid'] = False
    else:
         assets=Asset.objects.all()[:10]
         context = {'form': form,'asset':assets}

    data['html_bomGroupAsset_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
@csrf_exempt
def save_bomGroupAsset_form2(request, forms, template_name,woId=None):
    data = dict()
    context={}
    err=[]
    if (request.method == 'POST'):
        for form in forms:
          if form.is_valid():
            try:

                form.save()
                data['form_is_valid'] = True
            except IntegrityError as e:
            # Handle the unique constraint violation error
            # Display an error message or perform any necessary action
                err="unique"

          else:

              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)
              data['form_is_valid'] = False
        books=BOMGroupAsset.objects.filter(BOMGroupAssetBOMGroup=woId)
        data['html_bomGroupAsset_list'] = render_to_string('cmms/bomgroup_assets/partialBOMGroupAssetList.html', {
                'bomGroupAssets': books
            })
        form=BOMGroupAssetForm()
        context = {'form': form,'err':err}
    else:
         assets=Asset.objects.all()[:10]
         context = {'form': forms,'asset':assets}

    data['html_bomGroupAsset_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################
def bomGroupAsset_asset_select(request):
    makan=request.GET.get("makan",False)
    asset_type=request.GET.get("assettype",False)
    srch=request.GET.get("srch",False)
    data=dict()
    assets=Asset.objects.none()

    if(makan !='-1'):
        assets=Asset.objects.filter(assetIsLocatedAt_id=makan)
        if(asset_type!='-1'):
            assets=assets.filter(assetCategory_id=asset_type)
        if(srch!='-1'):
            if(srch):
                assets=assets.filter(Q(assetName__icontains=srch)|Q(assetCode__icontains=srch))
            # Q(assetName__icontains=qstr,assetTypes=aType)
                                   # |Q(assetCode__icontains=qstr,assetTypes=aType)|Q(id=int(qstr),assetTypes=aType)|Q(assetCategory__name__icontains=qstr,assetTypes=aType)
        wos,page=AssetUtility.doPagingWithPage(request,assets)
        data['html']= render_to_string('cmms/bomgroup_assets/partialAssetList.html', {
            'asset': wos
        })
        data['page']= render_to_string('cmms/bomgroup_assets/asset_page.html', {
            'asset': wos,'main_asset':makan,'search':srch,'kvm':asset_type
        })

    return JsonResponse(data)

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
        form=[]
        for i in data['BOMGroupAssetAsset']:
            data2 = request.POST.dict()
            data2['BOMGroupAssetBOMGroup']=data['BOMGroupAssetBOMGroup']
            data2['BOMGroupAssetAsset']=i
            frm = BOMGroupAssetForm(data2)
            form.append(frm)
        return save_bomGroupAsset_form2(request, form, 'cmms/bomgroup_assets/partialBOMGroupAssetCreate.html',woId)


    else:
        # main_assets=Asset.objects.filter(assetTypes=1,assetIsLocatedAt__isnull=True)
        # data['main_assets']= render_to_string('cmms/bomgroup_assets/mainassets.html', {
        #     'main_assets': main_assets
        # })
        # print(data['main_assets'])
        form = BOMGroupAssetForm2()
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
def LoadPageAssetBomGroupAsset(request):
    makan=request.GET.get("makan",False)
    asset_type=request.GET.get("assettype",False)
    srch=request.GET.get("srch",False)
    data=dict()
    assets=Asset.objects.none()

    if(makan !='-1'):
        assets=Asset.objects.filter(assetIsLocatedAt_id=makan)
        if(asset_type!='-1'):
            assets=assets.filter(assetCategory_id=asset_type)
        if(srch!='-1'):
            if(srch):
                assets=assets.filter(Q(assetName__icontains=srch)|Q(assetCode__icontains=srch))
            # Q(assetName__icontains=qstr,assetTypes=aType)
                                   # |Q(assetCode__icontains=qstr,assetTypes=aType)|Q(id=int(qstr),assetTypes=aType)|Q(assetCategory__name__icontains=qstr,assetTypes=aType)
        wos,page=AssetUtility.doPagingWithPage(request,assets)
        data['html']= render_to_string('cmms/bomgroup_assets/partialAssetList.html', {
            'asset': wos
        })
        data['page']= render_to_string('cmms/bomgroup_assets/asset_page.html', {
            'asset': wos,'main_asset':makan,'search':srch,'kvm':asset_type
        })

    return JsonResponse(data)
