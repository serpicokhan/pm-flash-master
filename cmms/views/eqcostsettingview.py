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
from cmms.forms import EquipmentCostSettingForm

###################################################################
def list_equipCost(request,id=None):
    books = EquipmentCostSetting.objects.all()
    return render(request, 'cmms/equip_cost/equipCostList.html', {'equipCosts': books})


###################################################################
def js_list_equipCost(request):
    data=dict()
    books=EquipmentCostSetting.objects.filter()

    data['html_equipCost_list']= render_to_string('cmms/settingpages/equip_cost/partialEquipCostlist.html', {
        'equipCosts': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_equipCost_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()

                books = EquipmentCostSetting.objects.all()
                data['html_equipCost_list'] = render_to_string('cmms/settingpages/equip_cost/partialEquipCostlist.html', {
                    'equipCosts': books
                })
                data['form_is_valid']=True
              else:
                  pass

        context = {'form': form}
        data['html_equipCost_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def equipCost_delete(request, id):
    comp1 = get_object_or_404(EquipmentCostSetting, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = EquipmentCostSetting.objects.all()
        data['html_equipCost_list'] = render_to_string('cmms/settingpages/equip_cost/partialEquipCostlist.html', {
            'equipCost': companies
        })
    else:
        context = {'equipCost': comp1}
        data['html_equipCost_form'] = render_to_string('cmms/settingpages/equip_cost/partialEquipCostDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def equipCost_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['settingEqAsset']=body['settingEqAsset']
        # data['causeDescription']=body['causeDescription']
        # data['causeIsActive']=True if body['causeDescription'] is 'true' else False
        form = EquipmentCostSettingForm(data)
    else:
        form = EquipmentCostSettingForm()

    return save_equipCost_form(request, form, 'cmms/settingpages/equip_cost/partialEquipCostCreate.html')
###################################################################

@csrf_exempt
def equipCost_update(request, id):
    company= get_object_or_404(EquipmentCostSetting, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['settingEqAsset']=body['settingEqAsset']
        # data['causeDescription']=body['causeDescription']


        form = EquipmentCostSettingForm(data, instance=company)
    else:
        form = EquipmentCostSettingForm(instance=company)
    return save_equipCost_form(request, form, 'cmms/settingpages/equip_cost/partialEquipCostUpdate.html')
