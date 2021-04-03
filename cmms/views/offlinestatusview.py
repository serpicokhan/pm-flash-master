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
from cmms.forms import OfflineStatusForm

###################################################################
def list_offlineStatus(request,id=None):
    books = OfflineStatus.objects.all()
    return render(request, 'cmms/part_purchase/offlineStatusList.html', {'offlineStatuss': books})


###################################################################
def js_list_offlineStatus(request):
    data=dict()
    books=OfflineStatus.objects.filter()

    data['html_offlineStatus_list']= render_to_string('cmms/settingpages/offline_status/partialOfflineStatuslist.html', {
        'offlineStatuss': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_offlineStatus_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = OfflineStatus.objects.all()
                data['html_offlineStatus_list'] = render_to_string('cmms/settingpages/offline_status/partialOfflineStatuslist.html', {
                    'offlineStatuss': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_offlineStatus_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def offlineStatus_delete(request, id):
    comp1 = get_object_or_404(OfflineStatus, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = OfflineStatus.objects.all()
        data['html_offlineStatus_list'] = render_to_string('cmms/settingpages/offline_status/partialOfflineStatuslist.html', {
            'offlineStatus': companies
        })
    else:
        context = {'offlineStatus': comp1}
        data['html_offlineStatus_form'] = render_to_string('cmms/settingpages/offline_status/partialOfflineStatusDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def offlineStatus_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['Code']=body['Code']
        data['name']=body['name']
        data['description']=body['description']
        form = OfflineStatusForm(data)
    else:
        form = OfflineStatusForm()

    return save_offlineStatus_form(request, form, 'cmms/settingpages/offline_status/partialOfflineStatusCreate.html')
###################################################################

@csrf_exempt
def offlineStatus_update(request, id):
    company= get_object_or_404(OfflineStatus, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['Code']=body['Code']
        data['name']=body['name']
        data['description']=body['description']


        form = OfflineStatusForm(data, instance=company)
    else:
        form = OfflineStatusForm(instance=company)
    return save_offlineStatus_form(request, form, 'cmms/settingpages/offline_status/partialOfflineStatusUpdate.html')
