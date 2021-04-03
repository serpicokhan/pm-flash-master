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
from cmms.forms import ActionCodeForm

###################################################################
def list_woAction(request,id=None):
    books = ActionCode.objects.all()
    return render(request, 'cmms/part_purchase/woActionList.html', {'woActions': books})


###################################################################
def js_list_woAction(request):
    data=dict()
    books=ActionCode.objects.filter()

    data['html_woAction_list']= render_to_string('cmms/settingpages/wo_action_code/partialWoActionlist.html', {
        'woActions': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_woAction_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = ActionCode.objects.all()
                data['html_woAction_list'] = render_to_string('cmms/settingpages/wo_action_code/partialWoActionlist.html', {
                    'woActions': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_woAction_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def woAction_delete(request, id):
    comp1 = get_object_or_404(ActionCode, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = ActionCode.objects.all()
        data['html_woAction_list'] = render_to_string('cmms/settingpages/wo_action_code/partialWoActionlist.html', {
            'woAction': companies
        })
    else:
        context = {'woAction': comp1}
        data['html_woAction_form'] = render_to_string('cmms/settingpages/wo_action_code/partialWoActionDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woAction_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['actionCode']=body['actionCode']
        data['actionDescription']=body['actionDescription']
        data['actionIsActive']=True if body['actionDescription'] is 'true' else False
        form = ActionCodeForm(data)
    else:
        form = ActionCodeForm()

    return save_woAction_form(request, form, 'cmms/settingpages/wo_action_code/partialWoActionCreate.html')
###################################################################

@csrf_exempt
def woAction_update(request, id):
    company= get_object_or_404(ActionCode, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['actionCode']=body['actionCode']
        data['actionDescription']=body['actionDescription']


        form = ActionCodeForm(data, instance=company)
    else:
        form = ActionCodeForm(instance=company)
    return save_woAction_form(request, form, 'cmms/settingpages/wo_action_code/partialWoActionUpdate.html')
