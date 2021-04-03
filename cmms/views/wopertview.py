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
from cmms.models.Asset import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import WoPertForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper

###################################################################
def list_woPert(request,id=None):
    books = WorkorderPert.objects.all()
    return render(request, 'cmms/wo_pert/woPertList.html', {'woPerts': books})


###################################################################
@permission_required('cmms.view_workorderpert')
def js_list_woPert(request,woId):
    data=dict()
    books=WorkorderPert.objects.filter(woPertWorkorder=woId)

    data['html_woPert_list']= render_to_string('cmms/wo_pert/partialWoPertList.html', {
        'woPerts': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_woPert_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books=WorkorderPert.objects.filter(woPertWorkorder=woId)
            data['html_woPert_list'] = render_to_string('cmms/wo_pert/partialWoPertList.html', {
                'woPerts': books,
                'perms': PermWrapper(request.user)
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_woPert_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def woPert_delete(request, id):
    comp1 = get_object_or_404(WorkorderPert, id=id)
    data = dict()
    woId=comp1.woPertWorkorder
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkorderPert.objects.filter(woPertWorkorder=woId)
        data['html_woPert_list'] = render_to_string('cmms/wo_pert/partialWoPertList.html', {
            'woPerts': companies,
            'perms': PermWrapper(request.user)

        })
    else:
        context = {'woPert': comp1}
        data['html_woPert_form'] = render_to_string('cmms/wo_pert/partialWoPertDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woPert_create(request,id=None):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['woPertWorkorder']=body['woPertWorkorder']
        data['woPertPert']=body['woPertPert']
        data['wpPertTime']=body['wpPertTime']
        # data['assetPertPertReadingUnit']=body['woPertReadingPertReadingUnit']
        woId=body['woPertWorkorder']

        form = WoPertForm(data)

    else:
        # woId=WorkOrder.objects.get(id=id)
        form = WoPertForm()
    return save_woPert_form(request, form, 'cmms/wo_pert/partialWoPertCreate.html',woId)
###################################################################

@csrf_exempt
def woPert_update(request, id):
    company= get_object_or_404(WorkorderPert, id=id)
    woId=company.woPertWorkorder
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()

        data = request.POST.dict()
        data['woPertWorkorder']=body['woPertWorkorder']
        data['woPertPert']=body['woPertPert']
        data['wpPertTime']=body['wpPertTime']
        # data['assetPertPertReadingUnit']=body['woPertReadingPertReadingUnit']
        woId=body['woPertWorkorder']
        form = WoPertForm(data, instance=company)
    else:
        form = WoPertForm(instance=company)
    return save_woPert_form(request, form, 'cmms/wo_pert/partialWoPertUpdate.html',woId)
