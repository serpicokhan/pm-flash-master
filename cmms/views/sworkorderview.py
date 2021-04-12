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
from django.db.models import Sum
import jdatetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from cmms.models.workorder import *
from cmms.models.task import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import WorkOrderForm
from django.urls import reverse_lazy
from cmms.business.SWOUtility import SWOUtility
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType

def filterUser(request,books):
    if(request.user.username!="admin"):
        books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
    else:
        books=books.order_by('-datecreated','-timecreated')
    return books
##########################################################
# @permission_required('cmms.view_workorder')
def list_swo(request,id=None):
    books = WorkOrder.objects.filter(isScheduling=True)
     #paging
    books=filterUser(request,books).order_by('-running')
    wos=SWOUtility.doPaging(request,books)
    return render(request, 'cmms/sworkorder/woList.html', {'wo': wos})

##########################################################
##########################################################
##########################################################
# نمای کاربر عادی و کاربر معمولی تفاوت داشته باشد
###############



#################################################################

def save_swo_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():




            form.save()
            if(request.user):
                 requestedUser=SysUser.objects.get(userId=request.user)
                 form.instance.RequestedUser=requestedUser
                 form.instance.save()
            #print("id:"+str(id))
            data['form_is_valid'] = True
            books = WorkOrder.objects.filter(isScheduling=True)
            books=filterUser(request,books)
            wos=SWOUtility.doPaging(request,books)
            if(id):
                LogEntry.objects.log_action(
                    user_id         = request.user.pk,
                    content_type_id = ContentType.objects.get_for_model(form.instance).pk,
                    object_id       = form.instance.id,
                    object_repr     = 'sworkorder',
                    action_flag     = CHANGE,
                    change_message= request.META.get('REMOTE_ADDR')
                )
            else:
                LogEntry.objects.log_action(
                    user_id         = request.user.pk,
                    content_type_id = ContentType.objects.get_for_model(form.instance).pk,
                    object_id       = form.instance.id,
                    object_repr     = 'sworkorder',
                    action_flag     = ADDITION,
                    change_message= request.META.get('REMOTE_ADDR')
                )


            data['html_wo_list'] = render_to_string('cmms/sworkorder/partialWolist.html', {
                'wo': wos,
                'perms': PermWrapper(request.user)
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form,'lId':id}


    data['html_wo_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def swo_delete(request, id):
    comp1 = get_object_or_404(WorkOrder, id=id)

    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkOrder.objects.filter(isScheduling=True)
        companies=filterUser(request,companies)
        #Tasks.objects.filter(woId=id).update(workorder=id)
        data['html_wo_list'] = render_to_string('cmms/sworkorder/partialWolist.html', {
            'wo': companies,
            'perms': PermWrapper(request.user)
        })
        LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(form.instance).pk,
        object_id       = form.instance.id,
        object_repr     = 'workorder',
        action_flag     = DELETION
    )
    else:
        context = {'wo': comp1}
        data['html_wo_form'] = render_to_string('cmms/sworkorder/partialWoDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################
def swo_create(request):
    if (request.method == 'POST'):
        form = WorkOrderForm(request.POST)
        LogEntry.objects.log_action(
         user_id         = request.user.pk,
         content_type_id = ContentType.objects.get_for_model(form.instance).pk,
         object_id       = form.instance.id,
         object_repr     = 'workorder',
         action_flag     = ADDITION
     )
        return save_swo_form(request, form, 'cmms/sworkorder/partialWoCreate.html')
    else:
        woInstance=WorkOrder.objects.create(isScheduling=True,creatNewWO=False,woStatus=1,woPriority=2,isPm=False)

        form = WorkOrderForm(instance=woInstance,initial={'isScheduling':'True'})
        return save_swo_form(request, form, 'cmms/sworkorder/partialWoCreate.html',woInstance.id)


##########################################################
def swo_update(request, id):
    company= get_object_or_404(WorkOrder, id=id)
    print(company)
    if (request.method == 'POST'):
        form = WorkOrderForm(request.POST, instance=company)
        LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(form.instance).pk,
        object_id       = form.instance.id,
        object_repr     = 'workorder',
        action_flag     = CHANGE
    )
    else:
        form = WorkOrderForm(instance=company)

    return save_swo_form(request, form,'cmms/sworkorder/partialWoUpdate.html',id)
##########################################################
def swo_deleteChildren(requst,id):
    #Tasks.objects.filter( woId=id).delete()
    dic=dict()
    dic['html-delete-success']=1
    return JsonResponse(dic)
    '''fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)
    logging.debug(comp1)

    comp1.delete()
    '''
###############################################
def SWOupdateRunning(request,id):
    obj=WorkOrder.objects.get(id=id)
    obj.running=not obj.running
    obj.save()
    data=dict()
    data['result']=obj.running
    return JsonResponse(data)
def swo_setAsset(request,wid,aid):
    wo=WorkOrder.objects.get(id=wid)
    wo.woAsset_id=aid
    wo.save()
    data=dict()
    data['result']=wo.woAsset_id
    return JsonResponse(data)
#######################Search By tags#####################
def swo_searchworkOrderByTags(request,searchStr):
    data=dict()

    searchStr=searchStr.replace('empty_','')
    searchStr=searchStr.replace('_',' ')
    books=(SWOUtility.seachSWoByTags(searchStr))
    books=filterUser(request,books)

    wos=SWOUtility.doPaging(request,books)
    if(not searchStr):
        searchStr='empty_'
    data['html_swo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {'wo': wos, 'perms': PermWrapper(request.user)   })
    data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination.html', {'wo': wos,'pageType':'swo_searchworkOrderByTags','pageArgs':searchStr            })
    data['form_is_valid'] = True
    return JsonResponse(data)

@csrf_exempt
def swo_cancel(request,id):
    data=dict()
    if(request.method=='POST'):
        wo=WorkOrder.objects.get(pk=id)

        if(not wo.summaryofIssue):
            # print(wo)
            wo.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            # companies = WorkOrder.objects.filter(isScheduling=True)
            # companies=filterUser(request,companies)
            # # page=request.GET.get('page',1)
            # wos=WOUtility.doPaging(request,companies)
            # #Tasks.objects.filter(woId=id).update(workorder=id)
            # data['html_wo_list'] = render_to_string('cmms/sworkorder/partialWolist.html', {
            #     'wo': wos
            # })

    return JsonResponse(data)
##########################
#########show runnign swo in woList
def swo_show_swo_by_type(request,status):
    data=dict()
    books=WorkOrder.objects.none()
    if(status=='1'):
        books=WorkOrder.objects.filter(running=True,isScheduling=True).order_by('-id')
    elif(status=='2'):
        books=WorkOrder.objects.filter(running=False,isScheduling=True).order_by('-id')
    else:
        books=WorkOrder.objects.filter(isScheduling=True).order_by('-id')
    books=filterUser(request,books).order_by('-running')
    wos=SWOUtility.doPaging(request,books)
    data['html_swo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {'wo': wos, 'perms': PermWrapper(request.user)   })
    data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination.html', {'wo': wos,'pageType':'swo_show_swo_by_type','pageArgs':status            })
    data['form_is_valid'] = True
    return JsonResponse(data)
###############################################
def swo_show_swo_by_schedule_type(request,status):
    data=dict()
    books=WorkOrder.objects.none()
    if(status=='1'):
        books=WorkOrder.objects.filter(isScheduling=True,id__in=Schedule.objects.filter(schChoices=0).values_list('workOrder',flat=True)).order_by('-id')
    elif(status=='2'):
        books=WorkOrder.objects.filter(id__in=Schedule.objects.filter(schChoices=1).values_list('workOrder',flat=True),isScheduling=True).order_by('-id')
    elif(status=='3'):
        books=WorkOrder.objects.filter(isScheduling=True,id__in=Schedule.objects.filter(schChoices=2).values_list('workOrder',flat=True)).order_by('-id')
    else:
        books=WorkOrder.objects.filter(isScheduling=True).order_by('-id')
    books=filterUser(request,books).order_by('-running')
    wos=SWOUtility.doPaging(request,books)
    data['html_swo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {'wo': wos, 'perms': PermWrapper(request.user)   })
    data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination.html', {'wo': wos,'pageType':'swo_show_swo_by_schedule_type','pageArgs':status            })
    data['form_is_valid'] = True
    return JsonResponse(data)
