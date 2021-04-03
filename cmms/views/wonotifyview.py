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
from cmms.forms import WoNotifyForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper

###################################################################
def list_woNotify(request,id=None):
    books = WorkorderUserNotification.objects.all()
    return render(request, 'cmms/workorder_notification/woNotifyList.html', {'woNotifys': books})


###################################################################
@permission_required('cmms.view_workorderfile')
def js_list_woNotify(request,woId):
    data=dict()
    books=WorkorderUserNotification.objects.filter(woNotifWorkorder=woId)

    data['html_woNotify_list']= render_to_string('cmms/workorder_notification/partialWoNotifyList.html', {
        'woNotifys': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_woNotify_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            # fmt = getattr(settings, 'LOG_FORMAT', None)
            # lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            # logging.basicConfig(format=fmt, level=lvl)
            # logging.debug( woId)
            books = WorkorderUserNotification.objects.filter(woNotifWorkorder=woId)
            data['html_woNotify_list'] = render_to_string('cmms/workorder_notification/partialWoNotifyList.html', {
                'woNotifys': books,
                'perms': PermWrapper(request.user)
            })
          else:
              # fmt = getattr(settings, 'LOG_FORMAT', None)
              # lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              # logging.basicConfig(format=fmt, level=lvl)
              # logging.debug( form.errors)
              pass

    context = {'form': form}
    data['html_woNotify_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def woNotify_delete(request, id):
    comp1 = get_object_or_404(WorkorderUserNotification, id=id)
    data = dict()
    woId=comp1.woNotifWorkorder

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkorderUserNotification.objects.filter(woNotifWorkorder=woId)
        data['html_woNotify_list'] = render_to_string('cmms/workorder_notification/partialWoNotifyList.html', {
            'woNotifys': companies
        })

    else:
        context = {'woNotify': comp1}
        data['html_woNotify_form'] = render_to_string('cmms/workorder_notification/partialWoNotifyDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woNotify_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)
    logging.debug( "dasdsadasdsa")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()

        data['woNotifWorkorder']=body['woNotifWorkorder']
        data['woNotifUser']=body['woNotifUser']
        data['woNotifOnAssignment']=True if body['woNotifOnAssignment']=='true' else False
        data['woNotifOnStatusChange']=True if body['woNotifOnStatusChange']=='true' else False
        data['woNotifOnCompletion']=True if body['woNotifOnCompletion']=='true' else False
        data['woNotifOnTaskCompleted']=True if body['woNotifOnTaskCompleted']=='true' else False
        data['woNotifOnOnlineOffline']=True if body['woNotifOnOnlineOffline']=='true' else False

        woId=body['woNotifWorkorder']

        form = WoNotifyForm(data)

    else:
        form = WoNotifyForm()
    return save_woNotify_form(request, form, 'cmms/workorder_notification/partialWoNotifyCreate.html',woId)
###################################################################

@csrf_exempt
def woNotify_update(request, id):
    company= get_object_or_404(WorkorderUserNotification, id=id)
    woId=company.woNotifWorkorder
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()

        data['woNotifWorkorder']=body['woNotifWorkorder']
        data['woNotifUser']=body['woNotifUser']
        data['woNotifOnAssignment']=True if body['woNotifOnAssignment']=='true' else False
        data['woNotifOnStatusChange']=True if body['woNotifOnStatusChange']=='true' else False
        data['woNotifOnCompletion']=True if body['woNotifOnCompletion']=='true' else False
        data['woNotifOnTaskCompleted']=True if body['woNotifOnTaskCompleted']=='true' else False
        data['woNotifOnOnlineOffline']=True if body['woNotifOnOnlineOffline']=='true' else False



        form = WoNotifyForm(data, instance=company)
    else:
        form = WoNotifyForm(instance=company)
    return save_woNotify_form(request, form, 'cmms/workorder_notification/partialWoNotifyUpdate.html',woId)
