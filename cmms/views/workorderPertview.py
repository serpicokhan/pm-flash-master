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
from cmms.forms import PertCodeForm

###################################################################
def list_workorderPert(request,id=None):
    books = PertCode.objects.all()
    return render(request, 'cmms/part_purchase/woPertList.html', {'woPerts': books})


###################################################################
def js_list_workorderPert(request):
    data=dict()
    books=PertCode.objects.filter()

    data['html_woPert_list']= render_to_string('cmms/settingpages/wo_pert_code/partialWoPertlist.html', {
        'woPerts': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_workorderPert_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = PertCode.objects.all()
                data['html_woPert_list'] = render_to_string('cmms/settingpages/wo_pert_code/partialWoPertlist.html', {
                    'woPerts': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_woPert_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def workorderPert_delete(request, id):
    comp1 = get_object_or_404(PertCode, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = PertCode.objects.all()
        data['html_woPert_list'] = render_to_string('cmms/settingpages/wo_pert_code/partialWoPertlist.html', {
            'woPert': companies
        })
    else:
        context = {'woPert': comp1}
        data['html_woPert_form'] = render_to_string('cmms/settingpages/wo_pert_code/partialWoPertDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def workorderPert_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['pertCode']=body['pertCode']
        data['pertDescription']=body['pertDescription']
        data['pertIsActive']=True if body['pertDescription'] is 'true' else False
        form = PertCodeForm(data)
    else:
        form = PertCodeForm()

    return save_workorderPert_form(request, form, 'cmms/settingpages/wo_pert_code/partialWoPertCreate.html')
###################################################################

@csrf_exempt
def workorderPert_update(request, id):
    company= get_object_or_404(PertCode, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['pertCode']=body['pertCode']
        data['pertDescription']=body['pertDescription']


        form = PertCodeForm(data, instance=company)
    else:
        form = PertCodeForm(instance=company)
    return save_workorderPert_form(request, form, 'cmms/settingpages/wo_pert_code/partialWoPertUpdate.html')
