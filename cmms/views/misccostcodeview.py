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
from cmms.forms import MiscCostCodeForm

###################################################################
def list_miscCostCode(request,id=None):
    books = MiscCostCode.objects.all()
    return render(request, 'cmms/part_purchase/miscCostCodeList.html', {'miscCostCodes': books})


###################################################################
def js_list_miscCostCode(request):
    data=dict()
    books=MiscCostCode.objects.filter()

    data['html_miscCostCode_list']= render_to_string('cmms/settingpages/misccost_code/partialMiscCostCodeList.html', {
        'miscCostCodes': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_miscCostCode_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = MiscCostCode.objects.all()
                data['html_miscCostCode_list'] = render_to_string('cmms/settingpages/misccost_code/partialMiscCostCodeList.html', {
                    'miscCostCodes': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_miscCostCode_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def miscCostCode_delete(request, id):
    comp1 = get_object_or_404(MiscCostCode, id=id)
    data = dict()

    comp1.delete()
    data['form_is_valid'] = True  # This is just to play along with the existing code
    companies = MiscCostCode.objects.all()
    data['html_miscCostCode_list'] = render_to_string('cmms/settingpages/misccost_code/partialMiscCostCodeList.html', {
        'miscCostCodes': companies
    })
    return JsonResponse(data)
###################################################################
@csrf_exempt
def miscCostCode_create(request):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['miscCostCode']=body['miscCostCode']
        data['miscCostDescription']=body['miscCostDescription']

        form = MiscCostCodeForm(data)
    else:
        form = MiscCostCodeForm()

    return save_miscCostCode_form(request, form, 'cmms/settingpages/misccost_code/partialMiscCostCodeCreate.html')
###################################################################

@csrf_exempt
def miscCostCode_update(request, id):
    company= get_object_or_404(MiscCostCode, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['miscCostCode']=body['actionCode']
        data['miscCostDescription']=body['actionDescription']


        form = MiscCostCodeForm(data, instance=company)
    else:
        form = MiscCostCodeForm(instance=company)
    return save_miscCostCode_form(request, form, 'cmms/settingpages/misccost_code/partialMiscCostCodeUpdate.html')
