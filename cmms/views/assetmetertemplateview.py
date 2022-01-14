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
from cmms.forms import AssetMeterTemplateForm

###################################################################
def list_assetMeterTemplate(request,id=None):
    books = AssetMeterTemplate.objects.all()
    return render(request, 'cmms/asset_meter_template/assetMeterTemplateList.html', {'assetMeterTemplates': books,'section':'list_assetMeterTemplate'})


###################################################################
def js_list_assetMeterTemplate(request,woId):
    # data=dict()
    # books=AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=woId).order_by('-id')
    #
    # data['html_assetMeterTemplate_list']= render_to_string('cmms/asset_meter_template/partialAssetMeterTemplateList.html', {
    #     'assetMeterTemplates': books
    # })
    # data['form_is_valid']=True
    # return JsonResponse(data)
        data=dict()
        bg_groups=BMGAsset.objects.filter(BMGAsset__id=woId).values_list('BMGGroup',flat=True)
        tmp_=BMGTemplate.objects.filter(BMGGroup__in=bg_groups).values_list('BMGTemplate',flat=True)
        books=AssetMeterTemplate.objects.filter(id__in=tmp_).order_by('-id')

        data['html_assetMeterTemplate_list']= render_to_string('cmms/asset_amt/partialAssetAMTList.html', {
            'assetAMTs': books
        })
        data['form_is_valid']=True
        return JsonResponse(data)


###################################################################    ###################################################################
def save_assetMeterTemplate_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = AssetMeterTemplate.objects.all().order_by('-id')
            data['html_assetMeterTemplate_list'] = render_to_string('cmms/asset_meter_template/partialAssetMeterTemplateList.html', {
                'assetMeterTemplates': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_assetMeterTemplate_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################


def assetMeterTemplate_delete(request, id):
    comp1 = get_object_or_404(AssetMeterTemplate, id=id)
    data = dict()
    # woId=comp1.assetMeterTemplateAsset

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        # companies = AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=woId).order_by('-id')
        companies = AssetMeterTemplate.objects.all().order_by('-id')
        data['html_assetMeterTemplate_list'] = render_to_string('cmms/asset_meter_template/partialAssetMeterTemplateList.html', {
            'assetMeterTemplates': companies
        })
    else:
        context = {'assetMeterTemplate': comp1}
        data['html_assetMeterTemplate_form'] = render_to_string('cmms/asset_meter_template/partialAssetMeterTemplateDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
def assetMeterTemplate_create(request):
    woId=-1

    if (request.method == 'POST'):




        form = AssetMeterTemplateForm(request.POST)
        return save_assetMeterTemplate_form(request, form, 'cmms/asset_meter_template/partialAssetMeterTemplateCreate.html')

    else:
        form = AssetMeterTemplateForm()
    return save_assetMeterTemplate_form(request, form, 'cmms/asset_meter_template/partialAssetMeterTemplateCreate.html')
###################################################################

def assetMeterTemplate_update(request, id):
    company= get_object_or_404(AssetMeterTemplate, id=id)
    if (request.method == 'POST'):

        form = AssetMeterTemplateForm(request.POST, instance=company)
    else:
        form = AssetMeterTemplateForm(instance=company)
    return save_assetMeterTemplate_form(request, form, 'cmms/asset_meter_template/partialAssetMeterTemplateUpdate.html')
##########################
def GetAssetMeterTemplates(request):

    # print(request.GET['q'])
    searchStr= request.GET['qry'] if request.GET['qry'] else ''
    x=AssetMeterTemplate.objects.filter(assetMeterTemplateDesc__icontains=searchStr).order_by('-id').values('id', 'assetMeterTemplateDesc','assetMeterTemplateMeter')
    # if(len(x)==0):
    #     print("dasdsa")
    #     x=[{'id':-1,'partName':'قطعه یافت نشد'}]


    # response_data = {}
    # response_data['result'] = '[dsadas,dasdasdas]'
    return JsonResponse(list(x), safe=False)
