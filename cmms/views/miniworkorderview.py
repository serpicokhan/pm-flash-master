'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neminiWorkorderbject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
from cmms.models.workorder import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import MiniWorkorderForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from django.db.models import Q
from cmms.business.WOUtility import *
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here

@permission_required('cmms.view_miniworkorder')
def list_miniWorkorder(request,id=None):
    #
    books = WorkOrder.objects.filter(isScheduling=False,visibile=True)
    books=filterUser(request,books)
    wos=WOUtility.doPaging(request,list(books))
    return render(request, 'cmms/miniworkorder/miniWorkorderList.html', {'miniWorkorder': wos,'section':'list_miniWorkorder'})


##########################################################
def filterUser(request,books):
    if(request.user.username!="admin"):
        books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))|Q(RequestedUser__userId=request.user)).order_by('-datecreated','-timecreated')
    else:
        books=books.order_by('-datecreated','-timecreated')
    return books

def save_miniWorkorder_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):

        if form.is_valid():
            form.save()
            RequestedUser=SysUser.objects.get(userId=request.user)
            form.instance.RequestedUser=RequestedUser
            WOUtility.create_task_when_wo_created_fromAPI(request,form.instance.id)
            WOUtility.create_notification(request,form.instance.id)
            form.instance.save()
            # if(id):
            #     LogEntry.objects.log_action(
            #         user_id         = request.user.pk,
            #         content_type_id = ContentType.objects.get_for_model(form.instance).pk,
            #         object_id       = form.instance.id,
            #         object_repr     = 'workorder',
            #         action_flag     = CHANGE,
            #         change_message= request.META.get('REMOTE_ADDR')
            #     )
            # else:
            #     LogEntry.objects.log_action(
            #         user_id         = request.user.pk,
            #         content_type_id = ContentType.objects.get_for_model(form.instance).pk,
            #         object_id       = form.instance.id,
            #         object_repr     = 'workorder',
            #         action_flag     = ADDITION,
            #         change_message= request.META.get('REMOTE_ADDR')
            #     )
            data['form_is_valid'] = True
            books = WorkOrder.objects.filter(isScheduling=False,visibile=True)
            books=filterUser(request,books)
            wos=WOUtility.doPaging(request,list(books))
            data['html_miniWorkorder_list'] = render_to_string('cmms/miniworkorder/partialMiniWorkorderList.html', {
                'miniWorkorder': wos,
                'perms': PermWrapper(request.user)
            })
        else:
            print(form.errors)
            print("!@#")
            data['form_is_valid'] = False

    context = {'form': form}


    data['html_miniWorkorder_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def miniWorkorder_delete(request, id):
    comp1 = get_object_or_404(WorkOrder, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  WorkOrder.objects.filter(isScheduling=False,visibile=True)
        companies=filterUser(request,companies)
        wos=WOUtility.doPaging(request,list(companies))
        #Tasks.objects.filter(miniWorkorderId=id).update(miniWorkorder=id)
        data['html_miniWorkorder_list'] = render_to_string('cmms/miniworkorder/partialMiniWorkorderList.html', {
            'miniWorkorder': wos,
            'perms': PermWrapper(request.user)
        })
    else:
        if(comp1.woStatus==1):
            context = {'miniWorkorder': comp1}
            data['html_miniWorkorder_form'] = render_to_string('cmms/miniworkorder/partialMiniWorkorderDelete.html',
                context,
                request=request,
            )
        else:
            context = {'miniWorkorder': comp1}
            data['html_miniWorkorder_form'] = render_to_string('cmms/miniworkorder/partialMiniWorkorderCantDelete.html',
                context,
                request=request,
            )

    return JsonResponse(data)

##########################################################

##########################################################
def miniWorkorder_create(request):
    if (request.method == 'POST'):
        form = MiniWorkorderForm(request.POST)
        # print("here!!!!!!")

        return save_miniWorkorder_form(request, form, 'cmms/miniworkorder/partialMiniWorkorderCreate.html')
    else:

        form = MiniWorkorderForm()
        return save_miniWorkorder_form(request, form, 'cmms/miniworkorder/partialMiniWorkorderCreate.html')




##########################################################
def miniWorkorder_update(request, id):
    company= get_object_or_404(WorkOrder, id=id)
    template=""
    if (request.method == 'POST'):
        form = MiniWorkorderForm(request.POST, instance=company)
    else:
        form = MiniWorkorderForm(instance=company)


    return save_miniWorkorder_form(request, form,"cmms/miniworkorder/partialMiniWorkorderUpdate.html",id)
##########################################################
def miniWorkorder_view(request, id):
    # print(id,"id")
    comp1 = get_object_or_404(WorkOrder, id=id)
    data = dict()


    data['form_is_valid'] = True  # This is just to play along with the existing code

    data['html_miniWorkorder_form'] = render_to_string('cmms/miniworkorder/partialMiniWorkorderForm2.html', {
            'c': comp1,
            'perms': PermWrapper(request.user)
        })



    return JsonResponse(data)

##########################################################
