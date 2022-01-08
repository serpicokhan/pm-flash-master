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
from cmms.forms import CauseCodeForm

###################################################################
def list_woCause(request,id=None):
    books = CauseCode.objects.all()
    return render(request, 'cmms/part_purchase/woCauseList.html', {'woCauses': books})


###################################################################
def js_list_woCause(request):
    data=dict()
    books=CauseCode.objects.filter()

    data['html_woCause_list']= render_to_string('cmms/settingpages/wo_cause_code/partialWoCauselist.html', {
        'woCauses': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_woCause_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = CauseCode.objects.all()
                data['html_woCause_list'] = render_to_string('cmms/settingpages/wo_cause_code/partialWoCauselist.html', {
                    'woCauses': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_woCause_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def woCause_delete(request, id):
    comp1 = get_object_or_404(CauseCode, id=id)
    data = dict()

    comp1.delete()
    data['form_is_valid'] = True  # This is just to play along with the existing code
    companies = CauseCode.objects.all()
    data['html_woCause_list'] = render_to_string('cmms/settingpages/wo_cause_code/partialWoCauselist.html', {
        'woCause': companies
    })
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woCause_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['causeCode']=body['causeCode']
        data['causeDescription']=body['causeDescription']
        data['causeIsActive']=True if body['causeDescription'] is 'true' else False
        form = CauseCodeForm(data)
    else:
        form = CauseCodeForm()

    return save_woCause_form(request, form, 'cmms/settingpages/wo_cause_code/partialWoCauseCreate.html')
###################################################################

@csrf_exempt
def woCause_update(request, id):
    company= get_object_or_404(CauseCode, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['causeCode']=body['causeCode']
        data['causeDescription']=body['causeDescription']


        form = CauseCodeForm(data, instance=company)
    else:
        form = CauseCodeForm(instance=company)
    return save_woCause_form(request, form, 'cmms/settingpages/wo_cause_code/partialWoCauseUpdate.html')
