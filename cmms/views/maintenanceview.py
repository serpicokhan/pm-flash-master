'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(newobject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
import django.core.serializers
import logging
from django.conf import settings
from cmms.models.workorder import *
from cmms.models.task import *
from cmms.models.users import *

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import WorkOrderForm,WorkOrderForm2,CopyAssetForm
from django.urls import reverse_lazy
from django.db import transaction
from cmms.business.mail import Mail
from django.contrib.auth.decorators import login_required
from cmms.business.DateJob import *
from django.core.paginator  import *
from cmms.business.WOUtility import WOUtility
from cmms.business.AssetUtility import *
from cmms.business.taskUtility import TaskUtility
from django.db.models import Q
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
import linecache
from django.forms import formset_factory
import sys
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
from rest_framework import status
from cmms.utils import *
from django.db.models import F
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

def filterUser(request,books):
    if(request.user.username!="admin" and  not request.user.groups.filter(name='operator').exists()):
        books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
    else:
        books=books.order_by('-datecreated','-timecreated')
    return books
##########################################################
# @login_require

@permission_required('cmms.view_workorder',login_url='/not_found')
def list_wo(request,id=None):
    try:
        books=[]
        groups=[]

        if(request.user.username!="admin" and  not request.user.groups.filter(name='operator').exists()):
            books = WorkOrder.objects.filter(isScheduling=False,visibile=True).filter(Q(RequestedUser__userId=request.user)|Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
            usid=SysUser.objects.get(userId=request.user.id)

            groups=UserGroup.objects.filter(id__in=UserGroups.objects.filter(userUserGroups__id=usid.id).values_list('groupUserGroups',flat=True))

        else:
            books = WorkOrder.objects.filter(isScheduling=False,visibile=True).order_by('-datecreated','-timecreated','-id')
            groups=UserGroup.objects.all()
        #paging
        # books = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True)#.order_by('-datecreated','-timecreated')
        # groups=UserGroup.objects.all(id__in=UserGroups.objects.filter(userUserGroups__id=request.user.id).values_list('groupUserGroups',flat=True))
        # groups=UserGroup.objects.all()
        #
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        user1=SysUser.objects.get(userId=request.user)
        # print(user1)
        # print(user1.profileImage,'$$$$$$$$$$')
        wos,page=WOUtility.doPagingWithPage(request,books)
        return render(request, 'cmms/maintenance/woList.html', {'wo': wos,'groups':groups,'user2':user1,'section':'list_wo','status':Status,'page':page})
    except Exception as ex:
        print(ex)
        return render(request, 'cmms/404.html', {'to':123})
@permission_required('cmms.view_workorder',login_url='/not_found')
def list_wo_by_status(request,woStatus):
    try:
        books=[]
        groups=[]

        if(request.user.username!="admin" and not request.user.groups.filter(name='operator').exists()):
            books = WorkOrder.objects.filter(isScheduling=False,visibile=True).filter(Q(RequestedUser__userId=request.user)|Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
            usid=SysUser.objects.get(userId=request.user.id)

            groups=UserGroup.objects.filter(id__in=UserGroups.objects.filter(userUserGroups__id=usid.id).values_list('groupUserGroups',flat=True))

        else:
            books = WorkOrder.objects.filter(isScheduling=False,visibile=True).order_by('-datecreated','-timecreated','-id')
            groups=UserGroup.objects.all()
        if(int(woStatus)<1000):
            books=books.filter(woStatus=int(woStatus))

        user1=SysUser.objects.get(userId=request.user)

        wos=WOUtility.doPaging(request,books)
        return render(request, 'cmms/maintenance/woList.html', {'wo': wos,'groups':groups,'user2':user1,
        'section':'list_wo','status':Status,'selected_status':int(woStatus)})
    except Exception as ex:
        print(ex)
        return render(request, 'cmms/404.html', {'to':123})


##########################################################
@permission_required('cmms.view_workorder',login_url='/not_found')
def wo_detail(request,id=None):
    try:
        books=[]
        groups=[]

        if(request.user.username!="admin" and not request.user.groups.filter(name='operator').exists()):
            books = WorkOrder.objects.filter(isScheduling=False,visibile=True).filter(Q(RequestedUser__userId=request.user)|Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
            usid=SysUser.objects.get(userId=request.user.id)

            groups=UserGroup.objects.filter(id__in=UserGroups.objects.filter(userUserGroups__id=usid.id).values_list('groupUserGroups',flat=True))

        else:
            books = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True).order_by('-datecreated','-timecreated')
            groups=UserGroup.objects.all()
        #paging
        # books = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True)#.order_by('-datecreated','-timecreated')
        # groups=UserGroup.objects.all(id__in=UserGroups.objects.filter(userUserGroups__id=request.user.id).values_list('groupUserGroups',flat=True))
        # groups=UserGroup.objects.all()
        #
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        user1=SysUser.objects.get(userId=request.user)
        # print(user1)
        # print(user1.profileImage,'$$$$$$$$$$')
        wos=WOUtility.doPaging(request,books)
        return render(request, 'cmms/maintenance/woList.html', {'wo': wos,'groups':groups,'user2':user1})
    except Exception as ex:
        print(ex)
        return render(request, 'cmms/404.html', {'to':123})


##########################################################
##########################################################
# نمای کاربر عادی و کاربر معمولی تفاوت داشته باشد
###############

@login_required
def list_lastday_wo(request):
    data=dict()
    books=WOUtility.getlastWorkorder()
    books=filterUser(request,books)
    wos=WOUtility.doPaging(request,list(books))
    data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {               'wo': wos  ,'perms': PermWrapper(request.user)          })
    data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPagination2.html', {               'wo': wos,'pageType':'list_lastday_wo'                       })
    data['form_is_valid'] = True
    return JsonResponse(data)

@login_required
def list_lastweek_wo(request):
    data=dict()
    books=WOUtility.getListWorkorderLastWeek(request)
    # books=filterUser(request,books)
    wos=WOUtility.doPaging(request,list(books))

    data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {               'wo': wos  ,'perms': PermWrapper(request.user)                     })
    data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPagination2.html', {               'wo': wos,'pageType':'list_lastweek_wo'           })
    data['form_is_valid'] = True
    return JsonResponse(data)

@login_required
def list_lastmonth_wo(request):
    data=dict()
    books=WOUtility.getListWorkorderLastMonth(request)
    # books=filterUser(request,books)
    wos=WOUtility.doPaging(request,list(books))
    #cant paging beacuase page number woudlnt be updated

    data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {               'wo': wos ,'perms': PermWrapper(request.user)          })
    data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPagination2.html', {               'wo': wos  ,'pageType':'list_lastmonth_wo'           })
    data['form_is_valid'] = True
    return JsonResponse(data)


##########################################################
##########################################################
# validVal=[0,0,0]
# validVal[0]=(WOUtility.checkTaskDateRange(form.instance))
# validVal[1]=(WOUtility.checkWODateRange(form.instance))
# validVal[2]=(WOUtility.wst_vs_tst(form.instance))
# print("###################",validVal)
# err_code,err_msg=WOUtility.checkErr(*validVal)

def save_wo_form(request, form, template_name,id=None,iscreated=None,page=None):


    # try:
        data = dict()
        if (request.method == 'POST'):
            q=request.GET.get('q',False)
            page=request.GET.get('page',False)
            print('page',page)
            if form.is_valid():

                err_code=0
                if(not form.instance.assignedToUser):
                    err_code=1
                    err_msg="کاربر را مشخص نمایید"
                if(not form.instance.maintenanceType):
                    err_code=1
                    err_msg="نوع نگهداری را تعیین کنید"
                # if(WOUtility.find_wos_created_within_5_days(form.instance)):
                #     error_code=100
                #     err_msg="دستور کاری مشابه در یستم باز است"
                if(err_code==0):

                    form.save()
                    #Asset life section
                    WOUtility.manageStopCode(request,form)
                    #End of asset life section
                    data['first_task_created']=WOUtility.create_task_when_wo_created(request,form)
                    ####################
                    form.instance.save()
                    ####################
                    WOUtility.log(request,form,id)
                    ######################
                    data['form_is_valid'] = True
                    books=None
                    if(q):
                        books=WOUtility.seachWoByTags(q).order_by('-datecreated','-timecreated','-id')
                    else:
                        books=WOUtility.refreshView(request)

                    wos,page=WOUtility.doPagingWithPage(request,books)
                    data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {
                        'wo': wos,
                        'perms': PermWrapper(request.user),
                        'page':page if page != None and iscreated != 1 else 1,
                        'q':q
                    })
                else:
                    data['form_is_valid'] = False
                    data['form_err_code'] = err_code
                    data['form_err_msg'] = err_msg

            else:
                data['form_is_valid'] = False

                print(form.errors)


        # consider id = 0 when you wanna create new wo
        context = {'form': form,'lId':id if id != None else 0,'page':page if page != None and iscreated != 1 else 1}
        if(form.instance):
            data['id']=form.instance.id
        data['html_wo_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)


##########################################################


def wo_delete(request, id):
    comp1 = get_object_or_404(WorkOrder, id=id)
    page=request.GET.get('page',1)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies=WOUtility.refreshView(request)
        wos,page=WOUtility.doPagingWithPage(request,companies)
        #Tasks.objects.filter(woId=id).update(workorder=id)
        data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {
            'wo': wos,
            'perms': PermWrapper(request.user),
            'page':page
        })
    else:
        context = {'wo': comp1,'page':page}
        data['html_wo_form'] = render_to_string('cmms/maintenance/partialWoDelete.html',
            context,
            request=request,
        )

    return JsonResponse(data)

##########################################################
def wo_create(request):
    if (request.method == 'POST'):


        form = WorkOrderForm(DateJob.clean_workorderdate(request))
        if(int(form.data['lastWorkOrderid'])>0):
            return wo_update(request, int(form.data['lastWorkOrderid']))
        else:
            return save_wo_form(request, form, 'cmms/maintenance/partialWoCreate.html',iscreated=1)
    else:
        # woInstance=WorkOrder.objects.create(isScheduling=False,creatNewWO=False,woStatus=1,woPriority=2,isPm=False)
        # form = WorkOrderForm(instance=woInstance)
        RequestedUser=SysUser.objects.get(userId=request.user)
        form = WorkOrderForm(initial={'isScheduling':False,'creatNewWO':False,'woStatus':1,'woPriority':2,'isPm':False,'RequestedUser':RequestedUser})
        # print(request.user)
        return save_wo_form(request, form, 'cmms/maintenance/partialWoCreate.html',iscreated=1)





        #     LogEntry.objects.log_action(
        #     user_id         = request.user.pk,
        #     content_type_id = ContentType.objects.get_for_model(form.instance).pk,
        #     object_id       = form.instance.id,
        #     object_repr     = 'workorder',
        #     action_flag     = ADDITION
        # )
            # print("$$$$$$$$$$$$$$$$$$$$")


##########################################################
def wo_update(request, id):
    company= get_object_or_404(WorkOrder, id=id)
    page=request.GET.get('page',1)
    print(request.build_absolute_uri())

    if (request.method == 'POST'):


        form = WorkOrderForm(DateJob.clean_workorderdate(request), instance=company)

    else:
        form = WorkOrderForm(instance=company,initial={'isUpdating':'True','woasset_':company.woAsset})


    return save_wo_form(request, form,'cmms/maintenance/partialWoUpdate.html',id,iscreated=2,page=page)
##########################################################

@login_required
def woGetHighPriority(request,startHijri,endHijri,loc=None):
    #paging is ok


            start,end=DateJob.convert2Date(startHijri,endHijri)
            # print(WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9)).query)

            if(not loc):
                books = WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9),visibile=True)
            else:
                books = WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9),woAsset__assetIsLocatedAt__id=loc,visibile=True)
            # if(request.user.username!="admin"):
            #     books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated')
            # books=filterUser(request,books)



            books=books.order_by('-datecreated','-timecreated')
            wos=WOUtility.doPaging(request,books)
            return render(request, 'cmms/maintenance/dash_woList.html', {'wo': wos})
@login_required
def woGetWoReqNumber(request,startHijri,endHijri,loc=None):
    #paging is ok


            start,end=DateJob.convert2Date(startHijri,endHijri)
            # print(WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9)).query)

            if(not loc):
                books = WorkOrder.objects.filter(visibile=True,isScheduling=False, datecreated__range=(start, end))
            else:
                books = WorkOrder.objects.filter(visibile=True,isScheduling=False, datecreated__range=(start, end),woAsset__assetIsLocatedAt__id=loc)
            # if(request.user.username!="admin"):
            #     books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated')
            # books=filterUser(request,books)

            books=books.order_by('-datecreated','-timecreated')


            wos=WOUtility.doPaging(request,books)
            return render(request, 'cmms/maintenance/dash_woList.html', {'wo': wos})
@login_required
def K_WoDueDate2(request,startHijri,endHijri):
    #paging is ok

            loc=request.GET.get("loc",False)

            start,end=DateJob.convert2Date(startHijri,endHijri)
            n1=WorkOrder.objects.none()
            # print(WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9)).query)

            # n1=n1.filter(datecreated__range=(start,F('requiredCompletionDate')))


            if(not loc):
                n1=WorkOrder.objects.filter(woStatus__in=(1,2,4,5,6,9),woStatus__isnull=False,isPm=True,isScheduling=False,visibile=True)
            else:
                n1=WorkOrder.objects.filter(woStatus__in=(1,2,4,5,6,9),woStatus__isnull=False,isPm=True,isScheduling=False,visibile=True,woAsset__assetIsLocatedAt__id=loc)
            # if(request.user.username!="admin"):
            #     books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated')
            # books=filterUser(request,books)
            n1=n1.filter(datecreated__gte=start,datecreated__lt=F('requiredCompletionDate'))

            books=n1.order_by('-datecreated','-timecreated')


            wos=WOUtility.doPaging(request,books)
            return render(request, 'cmms/maintenance/dash_woList.html', {'wo': wos})
@login_required
def WoDueNumber(request,startHijri,endHijri):
    #paging is ok

            loc=request.GET.get("loc",False)

            start,end=DateJob.convert2Date(startHijri,endHijri)
            n1=WorkOrder.objects.none()
            # print(WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9)).query)

            # n1=n1.filter(datecreated__range=(start,F('requiredCompletionDate')))


            if(not loc):
                n1=WorkOrder.objects.filter(woStatus__in=(1,2,4,5,6,9),woStatus__isnull=False,isPm=True,isScheduling=False,visibile=True)
            else:
                n1=WorkOrder.objects.filter(woStatus__in=(1,2,4,5,6,9),woStatus__isnull=False,isPm=True,isScheduling=False,visibile=True,woAsset__assetIsLocatedAt__id=loc)
            # if(request.user.username!="admin"):
            #     books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated')
            # books=filterUser(request,books)
            n1=n1.filter(datecreated__gte=start,requiredCompletionDate__gte=datetime.datetime.now())

            books=n1.order_by('-datecreated','-timecreated')


            wos=WOUtility.doPaging(request,books)
            return render(request, 'cmms/maintenance/dash_woList.html', {'wo': wos})



@login_required
def woGetOpenWO(request,startHijri,endHijri):


            start,end=DateJob.convert2Date(startHijri,endHijri)
            books = WorkOrder.objects.filter(isScheduling=False, datecreated__range=(start, end))
            books=filterUser(request,books)
            wos=WOUtility.doPaging(request,books)
            return render(request, 'cmms/maintenance/woList.html', {'wo': wos})


@login_required
def woGetCloseWO(request,startHijri,endHijri):
        if(request.user.username=="admin"):
            start,end=DateJob.convert2Date(startHijri,endHijri)
            books = WorkOrder.objects.filter(woStatus=7,isScheduling=False, datecreated__range=(start, end))
            books=filterUser(request,books)
            wos=WOUtility.doPaging(request,books)
            return render(request, 'cmms/maintenance/woList.html', {'wo': wos})
        return render(request, 'cmms/maintenance/woList.html', )

@login_required
def woGetOverdueWO(request,startHijri,endHijri):
                if(request.user.username=="admin"):
                    start,end=DateJob.convert2Date(startHijri,endHijri)
                    # print("SELECT   *  from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and current_date>requiredCompletionDate and isScheduling=0 and datecreated between '{0}' and '{1}'".format(start,end))
                    books = list(WorkOrder.objects.raw("SELECT   *  from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and current_date>requiredCompletionDate and isScheduling=0 and datecreated between '{0}' and '{1}'".format(start,end)))
                    books=filterUser(request,books)
                    wos=WOUtility.doPaging(request,books)
                    #data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {               'wo': wos            })
                    #data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPagination.html', {               'wo': wos,'pageType':'list_lastday_wo'                       })

                    return render(request, 'cmms/maintenance/woList.html', {'wo': wos})
                return render(request, 'cmms/maintenance/woList.html', )

##change asset
@permission_required('cmms.add_workorder',login_url='/not_found')
def wo_setAsset(request,wid,aid):
    data=dict()
    try:
        data['asset_user']=AssetUser.objects.filter(AssetUserAssetId__id=aid)[0].AssetUserUserId.id
    except :
        print("error")
        pass
    try:
        wo=WorkOrder.objects.get(id=wid)
        wo.woAsset_id=aid
        wo.save()

        data['result']=wo.woAsset_id



        books=AssetMeterReading.objects.filter(assetWorkorderMeterReading=wo)
        for book in books:
            book.assetMeterLocation=Asset.objects.get(id=aid)
            book.save()

        data['form_is_valid']=True
    except Exception as error:
        print(error)
        data['form_is_valid']=False

    return JsonResponse(data)

def wo_deleteChildren(requst,id):

    dic=dict()
    dic['html-delete-success']=1
    return JsonResponse(dic)

def wo_work_hour(request,id):
    data=dict()
    data['work_hour_result']=TaskUtility.getWorkOrderHour(id)
    return JsonResponse(data)
def wo_getProblem(request):
    # print(request.GET['q'])
    searchStr= request.GET['q'] if request.GET['q'] else ''
    books=WOUtility.getProblems(searchStr)


    # books=filterUser(request,books)
    # response_data = {}
    # response_data['result'] = '[dsadas,dasdasdas]'
    return JsonResponse(list(books), safe=False)
#######################Search By tags#####################
def wo_searchWorkOrderByTags(request):
    data=dict()
    searchStr=request.GET.get('q','')
    page=request.GET.get('page',False)
    searchStr=searchStr.replace('empty_','')
    searchStr=searchStr.replace('_',' ')
    books=WOUtility.seachWoByTags(searchStr)
    books=filterUser(request,books)
    if(not searchStr):
        searchStr='empty_'
    # print(searchStr)
    wos=WOUtility.doPaging(request,list(books))
    data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {               'wo': wos,       'perms': PermWrapper(request.user)               })
    data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPaginationsearch.html', {'wo': wos,'pageType':'wo_searchWorkOrderByTags','pageArgs':searchStr})
    data['form_is_valid'] = True
    data['page']=page
    return JsonResponse(data)


def woTypes(request,id):
    data=dict()
    books=[]
    if(id=='1'):
        books=WorkOrder.objects.filter(isScheduling=False,visibile=True).order_by('-id')
    elif(id=='2'):
        books=WorkOrder.objects.filter(isScheduling=False,visibile=True,isPartOf__isnull=False).order_by('-id')
        # print(WorkOrder.objects.filter(isScheduling=False,visibile=True,isPartOf__isnull=False).order_by('-id').query)
    else:
        books=WorkOrder.objects.filter(isScheduling=False,visibile=True,isPartOf__isnull=True).order_by('-id')
        # print(WorkOrder.objects.filter(isScheduling=False,visibile=True,isPartOf__isnull=False).order_by('-id').query)

    books=filterUser(request,books)
    wos=WOUtility.doPaging(request,books)
    data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {               'wo': wos,'perms': PermWrapper(request.user)                       })

    data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPagination.html', {'wo': wos,'pageType':'woTypes','pageArgs':id})
    data['form_is_valid'] = True
    return JsonResponse(data)


def woGroups(request,id):
    data=dict()
    books=[]
    if(id=='-1'):
        books=WorkOrder.objects.filter(isScheduling=False,visibile=True).order_by('-id')

    else:
        books=WorkOrder.objects.filter(isScheduling=False,visibile=True,assignedToUser__in=UserGroups.objects.filter(groupUserGroups__id=id).values_list('userUserGroups__id',flat=True)).order_by('-datecreated')
        # print(WorkOrder.objects.filter(isScheduling=False,visibile=True,isPartOf__isnull=False).order_by('-id').query)

    books=filterUser(request,books)
    wos=WOUtility.doPaging(request,books)
    data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {               'wo': wos,'perms': PermWrapper(request.user)                       })

    data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPagination.html', {'wo': wos,'pageType':'woGroups','pageArgs':id})
    data['form_is_valid'] = True
    return JsonResponse(data)
def wo_getwos(request):

        # print(request.GET['q'])
        searchStr= request.GET['qry'] if request.GET['qry'] else ''
        data=dict()
        print(searchStr,'###############')
        # books=list(WOUtility.seachWoByTags(searchStr))
        x=list(WorkOrder.objects.filter(visibile=True,isScheduling=False,id=int(searchStr)).values('id','summaryofIssue'))
        # response_data = {}
        # response_data['result'] = '[dsadas,dasdasdas]'
        return JsonResponse(x, safe=False)
@csrf_exempt
def wo_cancel(request,id):
    data=dict()
    if(request.method=='POST'):

        try:
            wo=WorkOrder.objects.get(pk=id)
            wo.delete()
        except:
            pass
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True)
        companies=filterUser(request,companies)
        # # page=request.GET.get('page',1)
        wos=WOUtility.doPaging(request,companies)
        #Tasks.objects.filter(woId=id).update(workorder=id)
        data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {
            'wo': wos,
            'perms': PermWrapper(request.user),
        })

    return JsonResponse(data)
@csrf_exempt
@permission_required('cmms.view_workorder',login_url='/not_found')
def formset_view(request):
    context ={}
    form = WorkOrderForm2()

    # creating a formset and 5 instances of GeeksForm
    if(request.user.username!="admin" and not request.user.groups.filter(name="operator").exists()):
        books = WorkOrder.objects.filter(isScheduling=False,visibile=True).filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
        usid=SysUser.objects.get(userId=request.user.id)

        groups=UserGroup.objects.filter(id__in=UserGroups.objects.filter(userUserGroups__id=usid.id).values_list('groupUserGroups',flat=True))

    else:
        books = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True).order_by('-datecreated','-timecreated')
        groups=UserGroup.objects.all()
    user1=SysUser.objects.get(userId=request.user)
        # print(user1)
        # print(user1.profileImage,'$$$$$$$$$$')
    wos=WOUtility.doPaging(request,books)

    # Add the formset to context dictionary
    context['form']= form
    context['woList']=wos
    context['section']='formset_view'
    return render(request, "cmms/maintenance/formset.html", context)
@csrf_exempt
def save_formset(request):
    #add try catch
    #add stopcause to asset life
    data = request.POST.dict()
    data2=dict()
    try:
        if (request.method == 'POST'):
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            data['datecreated']=DateJob.getDate2(body['datecreated'])
            data['requiredCompletionTime']=body['timeCompleted']
            data['RequestedUser']=body['RequestedUser']
            data['maintenanceType']=body['maintenanceType']
            data['woAsset']=body['woAsset']
            data['summaryofIssue']=body['summaryofIssue']
            data['completionNotes']=body['completionNotes']
            data['woCauseCode']=body['woCauseCode']
            data['Project']=body['Project']
            data['dateCompleted']=DateJob.getDate2(body['dateCompleted'])
            data['timeCompleted']=body['timeCompleted']
            data['assignedToUser_1']=body['assignedToUser']
            data['assignedToUser']=body['assignedToUser'][0]
            data['woStopCode']=body['woStopCode']
            data['woPart']=body['woPart']
            # print("woPart in view",data['woPart'])
            data['woPartQty']=body['woPartQty'] if body['woPartQty'] else 0
            data['isEM']=body['isEM'] #if body['isEM']=="true" else False
            data['pertTime']=body['pertTime']
            data['timecreated']=body['timecreated']
            data['woStatus']=body['woStatus']
            form = WorkOrderForm2(data)
            if form.is_valid():
                form.save(commit=False)
                form.instance.timecreated=datetime.datetime.strptime(data["timecreated"], '%H:%M:%S').time()
                form.instance.woPriority=3
                f2=form.save()
                LogEntry.objects.log_action(
                    user_id         = request.user.pk,
                    content_type_id = ContentType.objects.get_for_model(form.instance).pk,
                    object_id       = form.instance.id,
                    object_repr     = 'دستور کار موردی',
                    action_flag     = ADDITION,
                    change_message= request.META.get('REMOTE_ADDR')
                )
                qty=0

                if(data['woPartQty']):
                    qty=str(data['woPartQty']).split(',')

                i=0
                if(data['woPart']):
                    for k in list(data['woPart']):
                        stk=Stock.objects.get(id=k)
                        print(qty)
                        WorkorderPart.objects.create(woPartWorkorder=f2,woPartStock=stk,woPartActulaQnty=qty[i])
                        i=i+1
                if(data['assignedToUser_1']):
                    for k in list(data['assignedToUser_1']):
                        Tasks.objects.create(taskTypes=1,taskDescription=data['summaryofIssue'],taskAssignedToUser=SysUser.objects.get(id=k),taskStartDate=data['datecreated'],taskStartTime=data['timecreated'],taskDateCompleted=data['dateCompleted'],taskTimeCompleted=data['timeCompleted'],workOrder=f2)
                if(data['woStopCode'] and int(data['woStopCode'])!=15):
                    # try:
                        dd1="{0} {1}".format(f2.datecreated,f2.timecreated)
                        print(dd1)
                        dd2="{0} {1}".format(f2.dateCompleted,f2.timeCompleted)
                        d1=datetime.datetime.strptime(dd1, '%Y-%m-%d %H:%M:%S')#datetime.datetime.combine(f2.datecreated,f2.timecreated)
                        d2=datetime.datetime.strptime(dd2, '%Y-%m-%d %H:%M:%S')#datetime.datetime.combine(f2.datecreated,f2.timecreated)
                        # d2=datetime.datetime.combine(f2.dateCompleted,f2.timeCompeleted)
                        product= ((d2-d1).total_seconds()/3600)
                        ########Assetlife############
                        AssetLife.objects.create(assetLifeAssetid=form.instance.woAsset,assetOfflineFrom=form.instance.datecreated,assetOfflineFromTime='00:00:00',assetSetOfflineByUser=SysUser.objects.get(id=data['assignedToUser']),assetStopCode=form.instance.woStopCode,assetWOAssoc=form.instance,assetOnlineFrom=form.instance.dateCompleted,assetOnlineFromTime=form.instance.timeCompleted,assetSetOnlineByUser=form.instance.assignedToUser,assetOnlineProducteHourAffected=product)
                    # //except Except//ion as ex:
                        # print(ex)
                if(request.user.username!="admin"):
                    books = WorkOrder.objects.filter(isScheduling=False,visibile=True).filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')

                else:
                    books = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True).order_by('-datecreated','-timecreated')
                # Pert Time
                if(data['pertTime']):

                    try:
                        pcode=PertCode.objects.none()
                        pcode=PertCode.objects.get(pertCode="سایر")
                        if(pcode):
                            WorkorderPert.objects.create(woPertWorkorder=f2,woPertPert=pcode,wpPertTime=data["pertTime"])

                    except  Exception as e :
                        print(e)
                # print(data["pertTime"])
                page=request.GET.get('page',1)
                wos=WOUtility.doPaging(request,books)

                # print("dsadsa")
                data2['html_formset_list'] = render_to_string('cmms/maintenance/partialFormsetList.html', {'woList': wos,'perms': PermWrapper(request.user)})

                data2['form_is_valid']=True
                # print("here!!!!!!!!!!!")
            else:
                print(form.errors)
                data2['form_is_valid']=False
                data2["error"]=form.errors
    except Exception as e:
            data2['form_is_valid']=False
            # data2["error"]=e
            # print(e,"!@#!@")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
    # print(data2)

    return JsonResponse(data2)
####################################################
@csrf_exempt
def formset_bulk_deletion(request,ids):
    comp1=1
    # comp1 = get_object_or_404(WorkOrder, id=id)
    data = dict()
    clean_data=[int(i)  for i in ids.split(',')]





    cmps=WorkOrder.objects.filter(id__in=clean_data)

    if (request.method == 'POST'):

        for cmp in cmps:
            cmp.delete();


        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies=[]
        if(request.user.username!="admin"):
            companies = WorkOrder.objects.filter(isScheduling=False,visibile=True).filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')

        else:
            companies = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True).order_by('-datecreated','-timecreated')

        wos=WOUtility.doPaging(request,companies)
        #Tasks.objects.filter(woId=id).update(workorder=id)
        data['html_formset_list'] = render_to_string('cmms/maintenance/partialFormsetList.html', {
            'woList': wos,
            'perms': PermWrapper(request.user)
        })
    else:

        context = {'wo': ids}
        data['html_wo_form'] = render_to_string('cmms/maintenance/partialFormsetDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)















@api_view(['GET'])
def workorder_collection(request):
    if request.method == 'GET':
        # print("!23")
        posts = WorkOrder.objects.filter(isScheduling=False,summaryofIssue__isnull=False).order_by('-datecreated')[:100]
        serializer = WOSerializer(posts, many=True)
        for k in serializer.data:
            # k.datecreated=DateJob.getDate2(k.datecreated)
            k["datecreated"]= str(jdatetime.datetime.fromgregorian(date=datetime.datetime.strptime(k["datecreated"], "%Y-%m-%d").date()).date()).replace('-','/')
        return Response(serializer.data)
@csrf_exempt
def work_order_test_api(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        # asset = request.POST.get('asset')
        wo=WorkOrder.objects.get(id=id)
        tasks=wo.CompleteUserTask.all()
        for task in tasks:
            if(not task.taskTimeEstimate):
                task.taskTimeEstimate=0.1
            dt_start=datetime.datetime.combine(task.taskStartDate,task.taskStartTime)
            dt_end=dt_start+timedelta(hours=task.taskTimeEstimate)
            task.taskDateCompleted=dt_end.date()
            task.taskTimeCompleted=dt_end.time()
            wo.dateCompleted=task.taskDateCompleted
            wo.timeCompleted=task.taskTimeCompleted
            # task.time
            task.save()
        wo.woStatus=7

        wo.save()
        # Perform any necessary processing or validations

        # Save the work order or perform any other operations

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request method'})
@api_view(['GET'])
def workorder_collection2(request):
    if request.method == 'GET':
        # print("!23")
        asset=request.GET.get('assetID',False)
        if(asset==False or asset=='0'):
            posts = WorkOrder.objects.filter(isScheduling=False,summaryofIssue__isnull=False).order_by('-datecreated')[:100]
        else:
            print(asset,'!!!!!!!')
            assets=AssetUtility.get_sub_assets(Asset.objects.get(id=asset))
            posts = WorkOrder.objects.filter(isScheduling=False,summaryofIssue__isnull=False,woAsset__in=assets).order_by('-datecreated')[:100]
        serializer = WOSerializer2(posts, many=True)
        for k in serializer.data:
            pass
            # k.datecreated=DateJob.getDate2(k.datecreated)
            # k["datecreated"]= str(jdatetime.datetime.togregorian(date=datetime.datetime.strptime(k["datecreated"], "%Y-%m-%d").date()).date()).replace('-','/')
        return Response(serializer.data)
@api_view(['GET'])
def workorder_api_detail(request,id):
    if request.method == 'GET':
        print("!23")
        posts = WorkOrder.objects.get(id=id)
        serializer = WOSerializerDetaile(posts)
        # for k in serializer.data:
            # k.datecreated=DateJob.getDate2(k.datecreated)
        serializer.data["datecreated"]= str(jdatetime.datetime.fromgregorian(date=datetime.datetime.strptime(serializer.data["datecreated"], "%Y-%m-%d").date()).date()).replace('-','/')
        return Response(serializer.data)


def wo_filter(request,startHijri,endHijri,wotype,ordercol,ordertype):
            data=dict();
    #paging is ok


            start,end=DateJob.convert2Date(startHijri,endHijri)
            # print(WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9)).query)
            books=None
            ordercode=None
            filter_wo=request.GET.getlist("q",False)
            if(ordertype == "0"):
                ordercode={"0":"id","1":"datecreated","2":"woAsset","3":"woStatus"}
            else:
                ordercode={"0":"-id","1":"-datecreated","2":"-woAsset","3":"-woStatus"}

            if(wotype=='0'):

                books = WorkOrder.objects.filter(isScheduling=False,visibile=True, datecreated__range=(start, end))
            else:
                books = WorkOrder.objects.filter(isScheduling=True, datecreated__range=(start, end))
            if(filter_wo!=["False"]):

                if(filter_wo!='null' and filter_wo ):


                    filter_wo=','.join([str(i) for i in filter_wo])
                    filter_wo=filter_wo.split(',')
                    books=books.filter(woStatus__in=filter_wo)


            # if(request.user.username!="admin"):
            #     books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated')
            books=filterUser(request,books)
            # print(books)




            wos=WOUtility.doPaging(request,books.order_by(ordercode[ordercol]))
            data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {
                       'wo': wos,'perms': PermWrapper(request.user)                       })

            data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPagination3.html',
                                                         {'wo': wos,'pageType':'wo_filter','sdt1':startHijri,
                                                          'sdt2':endHijri,'ptype':wotype,'ordercol':ordercol,'ordertype':ordertype,'q':request.GET.get('q',False)})
            data['form_is_valid'] = True
            return JsonResponse(data)
            return render(request, 'cmms/maintenance/woList.html', {'wo': wos})
#EM
def showEM(request,startHijri,endHijri,loc=None):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=0
    if(not loc):
        n1=WOUtility.getEms(start,end)
    else:
        n1=WOUtility.getEms(start,end,loc)
    wos=WOUtility.doPaging(request,n1)
    return render(request,"cmms/maintenance/dash_woList.html",{"wo" : wos})
def showtaviz(request,startHijri,endHijri,loc=None):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=0
    n2=0
    s1=[]
    s2=[]
    if(not loc):
        n1=WOUtility.getTaviz(start,end)
        n2=WorkorderPart.objects.values('woPartWorkorder__datecreated').filter(woPartWorkorder__datecreated__range=(start,end),woPartActulaQnty__gt=0,woPartWorkorder__visibile=True,woPartWorkorder__isScheduling=False).annotate(part_total=Sum('woPartActulaQnty')).order_by('woPartWorkorder__datecreated')
        for i in n2:
            s1.append(str(jdatetime.date.fromgregorian(date=i['woPartWorkorder__datecreated'])))
            s2.append(i['part_total'])
        # print(n2.query)
    else:
        n1=WOUtility.getTaviz(start,end,loc)
        n2=WorkorderPart.objects.values('woPartWorkorder__datecreated').filter(woPartWorkorder__datecreated__range=(start,end),woPartActulaQnty__gt=0).filter(Q(woPartWorkorder__woAsset__id=loc)|Q(woPartWorkorder__woAsset__assetIsLocatedAt__id=loc)).annotate(part_total=Sum('woPartActulaQnty')).order_by('woPartWorkorder__datecreated')
        for i in n2:
            s1.append(str(jdatetime.date.fromgregorian(date=i['woPartWorkorder__datecreated'])))
            s2.append(i['part_total'])
    wos=WOUtility.doPaging(request,n1)
    return render(request,"cmms/maintenance/dash_woList.html",{"wo" : wos,"taviz":1,"s1":s1,"s2":s2})
def showtavaghof(request,startHijri,endHijri,loc=None):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=0

    if(loc is None):
        n1=WOUtility.getTavaghof(start,end,None)
    else:
        n1=WOUtility.getTavaghof(start,end,loc)
    n1=n1.order_by('assetLifeAssetid__assetTavali','-assetOfflineFrom')
    total=0
    for i in n1:
        total+=i.getAffectedHour_digits()
    final_total='{0:02.0f}:{1:02.0f}'.format(*divmod(total * 60, 60))
    wos=WOUtility.doPaging(request,n1)
    return render(request,"cmms/asset_life_main/assetLifeMainList.html",{"assetLifes" : wos,'total_time':final_total})
def showmonghazi(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=list(WOUtility.getOverDueWoDetail(start,end))
    wos=WOUtility.doPaging(request,n1)
    return render(request,"cmms/maintenance/dash_woList.html",{"wo" : wos})
def shownewwo(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.getNewWO(start,end)
    wos=WOUtility.doPaging(request,n1)
    return render(request,"cmms/maintenance/dash_woList.html",{"wo" : wos})
@csrf_exempt
def set_wo_to_em(request,ids):
        clean_data=[int(i)  for i in ids.split(',')]

        data=dict()
        '''render_to_string('cmms/asset/temp.txt')'''
    # if (request.method == 'POST'):
        wos=WorkOrder.objects.filter(id__in=clean_data)

        for s in wos:
            s.isEM=not s.isEM
            s.save()
        books=[]
        books=[]


        if(request.user.username!="admin"):
            books = WorkOrder.objects.filter(isScheduling=False,visibile=True).filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')

        else:
            books = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True).order_by('-datecreated','-timecreated')

        page=request.GET.get('page',1)
        wos=WOUtility.doPaging(request,books)
        data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {
            'wo': wos,
            'perms': PermWrapper(request.user)
        })
        data['form_is_valid']=True
        data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {
            'wo': wos,
            'perms': PermWrapper(request.user)
        })


    # else:
    #
    #     # m=AssetUtility.getCategory()
    #     # m=m.replace('"',"'")
    #     context={'perms': PermWrapper(request.user),'ids':ids}
    #     data["modalem"]=render_to_string('cmms/maintenance/partialWobulkEM.html',
    #     context,
    #     request=request)
        return JsonResponse(data)
# for changing em val in formset
def updateEm(request,id,val):
    data=dict()
    wo=WorkOrder.objects.get(id=id)
    if(val=="0"):
        wo.isEM=True
    else:
        wo.isEM=False
    wo.save()
    data["isvalid"]=True
    return JsonResponse(data)
def load_dynamic_Asset(request):
    assets=Asset.objects.all()
    data=dict()
    data["html_assets_dynamics"]=render_to_string('cmms/maintenance/partialWOAssetDynamics.html',
        {'assets':assets})
    data["form_is_valid"]=True
    return JsonResponse(data)
def wo_Update_Task_User(request,woid,uid):
    data=dict()
    tasks=Tasks.objects.filter(workOrder=woid)
    for t in tasks:
        t.taskAssignedToUser=SysUser.objects.get(pk=uid)
        t.save()
    tasks2=Tasks.objects.filter(workOrder__in=WorkOrder.objects.filter(isScheduling=False,visibile=False,isPartOf=woid))
    for t in tasks2:
            t.taskAssignedToUser=SysUser.objects.get(pk=uid)
            t.save()
    data['html_data_tasks']=data['html_task_list']= render_to_string('cmms/tasks/partialTaskList.html', {
        'task': tasks,
        'perms': PermWrapper(request.user),
        'ispm':False
        })
    data['form_is_valid']=True
    return JsonResponse(data)
@csrf_exempt
def bulk_delete_wo(request,ids):
    clean_data=[int(i)  for i in ids.split(',')]
    foo=WorkOrder.objects.filter(id__in=clean_data)
    for i in foo:
        i.delete()
    data=dict()
    # books = WorkOrder.objects.filter(isScheduling=False,visibile=True).order_by('-datecreated','-timecreated')
    # page=request.GET.get('page',1)
    # wos=WOUtility.doPaging(request,books)
    # data['html_wo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {
    #     'wo': wos,
    #     'perms': PermWrapper(request.user)
    # })
    #
    # data['html_wo_paginator'] = render_to_string('cmms/maintenance/partialWoPagination.html', {
    #                   'wo': wos})
    data['form_is_valid'] = True
    # print('done')
    return JsonResponse(data)
def wo_change_status(request,id,status):
    data=dict()
    if(status=="7"):
        wo=WorkOrder.objects.get(id=id)
        result=TaskUtility.check_completion_date(wo)
        if(result):
            data['form_is_valid']=True
            data['wo_time']=result
        else:
            data['form_is_valid']=False
            data['wo_status']=wo.woStatus
    return JsonResponse(data)
def set_wo_status(request,woId,status_code):
    data=dict()
    if(request.method=="GET"):
        try:
            wo=WorkOrder.objects.get(id=woId)
            wo.woStatus=status_code
            wo.save()
            data["success"]=True
        except WorkOrder.DoesNotExist:
            data["error"]="couldnt find such wo"
    return JsonResponse(data)




def wo_copy(request,ids=None):
    if(request.method=='GET'):
        print("kire khar")
        data=dict()
        id=request.GET.get('id','')
        wo_asset1=WorkOrder.objects.get(id=id).woAsset
        assets=Asset.objects.all().order_by('-id')
        # assets=Asset.objects.all().order_by('-id')
        asset_loc=Asset.objects.filter(assetTypes=1)
        asset_cat=AssetCategory.objects.all()
        wos=AssetUtility.doPaging(request,assets)
        form=CopyAssetForm()
        q=request.GET.get('q','')

        data["modalcopyasset"]=render_to_string('cmms/sworkorder/assetcopy.html',{'asset':wos,'asset_cat':asset_cat,
        'asset_loc':asset_loc,'perms': PermWrapper(request.user),'form':form,'id':id})
        data['html_asset_paginator'] = render_to_string('cmms/asset/partialAssetPagination_swo.html', {
                          'asset': wos,'pageType':'swo_copy','ptr':0,'q':q})
        data['form_is_valid']=True
        return JsonResponse(data)
@csrf_exempt
def save_wo_copy(request):
        data=dict()
        data['form_is_valid']=True
        assetlist=request.GET.get("q", "")
        assetlist=[int(i) for i in assetlist.split(',') ]
        ids=request.GET.get('id',False)
        # print(assetlist,'assetlist')
        WOUtility.copy(int(ids),assetlist,request)
        books = WorkOrder.objects.filter(isScheduling=False,visibile=True)
        books=filterUser(request,books)
        wos=WOUtility.doPaging(request,books)
        data['html_swo_list'] = render_to_string('cmms/maintenance/partialWoList.html', {
            'wo': wos,
            'perms': PermWrapper(request.user)
        })
        data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination2.html', {'wo': wos           })
        return JsonResponse(data)
def woExport(request):
    data = WOUtility.download_csv(request, WorkOrder.objects.filter(isScheduling=0))

    return HttpResponse (data, content_type='text/csv')
