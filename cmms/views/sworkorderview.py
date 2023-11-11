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
from cmms.forms import WorkOrderForm,CopyAssetForm
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
from cmms.business.AssetUtility import AssetUtility
from cmms.business.DateJob import *

def filterUser(request,books):
    if(request.user.username!="admin" and  not request.user.groups.filter(name='operator').exists()):
        books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-timestamp','-running')
    else:
        books=books.order_by('-timeStamp','-running')
    return books
##########################################################
@permission_required('cmms.view_workorder')
def list_swo(request,id=None):
    books = WorkOrder.objects.filter(isScheduling=True)
     #paging
    books=filterUser(request,books)
    wos,page=SWOUtility.doPagingWithPage(request,books)
    return render(request, 'cmms/sworkorder/woList.html', {'wo': wos,'section':'list_swo','page':page})

##########################################################
##########################################################
##########################################################
# نمای کاربر عادی و کاربر معمولی تفاوت داشته باشد
###############



#################################################################

def save_swo_form(request, form, template_name,id=None,page=None):


    data = dict()

    if (request.method == 'POST'):
        if form.is_valid():
            q=request.GET.get('q',False)
            form.save()
            #print("id:"+str(id))
            data['form_is_valid'] = True
            books=None
            if(q):
                books=(SWOUtility.seachSWoByTags(q))
                books=filterUser(request,books)
            else:
                books = WorkOrder.objects.filter(isScheduling=True)
                books=filterUser(request,books)
            wos,page=SWOUtility.doPagingWithPage(request,books)
            SWOUtility.log(request,form,id)
            data['html_wo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {
                'wo': wos,
                'perms': PermWrapper(request.user),
                'page':page,
                'q':q
            })
            # data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination.html', {'wo': wos,'pageType':'swo_searchworkOrderByTags','pageArgs':searchStr            })
        else:
            data['form_is_valid'] = False
            print(form.errors)

    context = {'form': form,'lId':id if id != None else 0,'ispm':True,'page':page}
    if(form.instance):
        data['id']=form.instance.id
    data['html_wo_form'] = render_to_string(template_name, context, request=request)
    print(JsonResponse(data))
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
        wos=SWOUtility.doPaging(request,companies)
        #Tasks.objects.filter(woId=id).update(workorder=id)
        data['html_wo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {
            'wo': wos,
            'perms': PermWrapper(request.user)
        })
        data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination.html', {'wo': wos,'pageType':'list_swo','pageArgs':'1'            })
    else:
        context = {'wo': comp1}
        data['html_wo_form'] = render_to_string('cmms/sworkorder/partialWoDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################
def swo_create(request):



        form = WorkOrderForm(DateJob.clean_workorderdate(request))
        if (request.method == 'POST'):
            if(int(form.data['lastWorkOrderid'])>0):
                return swo_update(request, int(form.data['lastWorkOrderid']))
            else:
                LogEntry.objects.log_action(
                 user_id         = request.user.pk,
                 content_type_id = ContentType.objects.get_for_model(form.instance).pk,
                 object_id       = form.instance.id,
                 object_repr     = 'workorder',
                 action_flag     = ADDITION
             )
                return save_swo_form(request, form, 'cmms/sworkorder/partialWoCreate.html')

        else:
            reqUser=SysUser.objects.get(userId=request.user)
            # woInstance=WorkOrder.objects.create(isScheduling=True,creatNewWO=False,woStatus=1,woPriority=2,isPm=False,RequestedUser=reqUser)

            form = WorkOrderForm(initial={'isScheduling':True,'creatNewWO':False,'woStatus':1,'woPriority':2,'isPm':False,'requestedUser':reqUser})
            return save_swo_form(request, form, 'cmms/sworkorder/partialWoCreate.html')


##########################################################
def swo_update(request, id):
    company= get_object_or_404(WorkOrder, id=id)
    page=request.GET.get('page',1)


    # print(company)
    if (request.method == 'POST'):


        # form = WorkOrderForm(updated_request)
        form = WorkOrderForm(DateJob.clean_workorderdate(request), instance=company)
        LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(form.instance).pk,
        object_id       = form.instance.id,
        object_repr     = 'workorder',
        action_flag     = CHANGE
    )
    else:
        form = WorkOrderForm(instance=company,initial={'woasset_':company.woAsset})

    return save_swo_form(request, form,'cmms/sworkorder/partialWoUpdate.html',id,page=page)
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
@permission_required('cmms.add_workorder',login_url='/not_found')
def SWOupdateRunning(request,id):
    obj=WorkOrder.objects.get(id=id)
    obj.running=not obj.running
    obj.save()
    data=dict()
    data['result']=obj.running
    return JsonResponse(data)

@permission_required('cmms.add_workorder',login_url='/not_found')
def swo_setAsset(request,wid,aid):
    data=dict()
    try:
        wo=WorkOrder.objects.get(id=wid)
        wo.woAsset_id=aid
        wo.save()

        data['result']=wo.woAsset_id
        books=AssetMeterReading.objects.filter(assetWorkorderMeterReading=wo)
        for book in books:
            book.assetMeterLocation=Asset.objects.get(id=aid)
            book.save()
        sches=Schedule.objects.filter(workOrder=wo)
        for sch in sches:
            sch.schAsset=Asset.objects.get(id=aid)
            sch.save()
        data['form_is_valid']=True
    except Exception as error:
        print(error)
        data['form_is_valid']=False

    return JsonResponse(data)
#######################Search By tags#####################
def swo_searchworkOrderByTags(request):
    data=dict()

    # searchStr=searchStr.replace('empty_','')

    # searchStr=searchStr.replace('_',' ')

    searchStr=request.GET.get('q','')
    page=request.GET.get('page',False)
    books=(SWOUtility.seachSWoByTags(searchStr))
    books=filterUser(request,books)

    wos=SWOUtility.doPaging(request,books)
    if(not searchStr):
        searchStr='empty_'
    data['html_swo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {'wo': wos, 'perms': PermWrapper(request.user)   })
    data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination.html', {'wo': wos,'pageType':'swo_searchworkOrderByTags','pageArgs':searchStr            })
    data['form_is_valid'] = True
    data['page']=page
    return JsonResponse(data)

@csrf_exempt
def swo_cancel(request,id):
    data=dict()
    if(request.method=='POST'):



        # print(wo)
        try:
            wo=WorkOrder.objects.get(pk=id)
            wo.delete()
        except:
            pass


        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkOrder.objects.filter(isScheduling=True).order_by('-id')
        companies=filterUser(request,companies)
        page=request.GET.get('page',1)
        wos=SWOUtility.doPaging(request,companies)
        # #Tasks.objects.filter(woId=id).update(workorder=id)
        data['html_wo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {
            'wo': wos,
            'perms': PermWrapper(request.user),
        })

    return JsonResponse(data)
##########################
#########show runnign swo in woList
def swo_show_swo_by_type(request):
    data=dict()
    books=WorkOrder.objects.none()
    status=request.GET.get("q","1")
    if(status=='1'):
        books=WorkOrder.objects.filter(running=True,isScheduling=True).order_by('-id')
    elif(status=='2'):
        books=WorkOrder.objects.filter(running=False,isScheduling=True).order_by('-id')
    else:
        books=WorkOrder.objects.filter(isScheduling=True).order_by('-id')
    books=filterUser(request,books).order_by('-running')
    wos=SWOUtility.doPaging(request,books)
    data['html_swo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {'wo': wos, 'perms': PermWrapper(request.user)   })
    data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination.html', {'wo': wos,'pageType':'swo_show_swo_by_type','q':status            })
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
@permission_required('cmms.view_workorder',login_url='/not_found')
def swo_detail(request,id=None):
    try:
        books=[]
        groups=[]

        if(request.user.username!="admin"):
            books = WorkOrder.objects.filter(isScheduling=True,visibile=True).filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
            usid=SysUser.objects.get(userId=request.user.id)

            groups=UserGroup.objects.filter(id__in=UserGroups.objects.filter(userUserGroups__id=usid.id).values_list('groupUserGroups',flat=True))

        else:
            books = WorkOrder.objects.filter(isScheduling=True).filter(visibile=True).order_by('-datecreated','-timecreated')
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
        return render(request, 'cmms/sworkorder/woList.html', {'wo': wos,'groups':groups,'user2':user1})
    except Exception as ex:
        print(ex)
        return render(request, 'cmms/404.html', {'to':123})

def swo_copy(request,ids=None):
    if(request.method=='GET'):
        print("1")
        data=dict()
        id=request.GET.get('id','')

        # wo_asset1=WorkOrder.objects.get(id__in=id).woAsset
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
def save_swo_copy(request):
        data=dict()
        data['form_is_valid']=True
        assetlist=request.GET.get("q", "")
        assetlist=[int(i) for i in assetlist.split(',') ]
        ids=request.GET.get('id',False)
        SWOUtility.copy2(ids,assetlist,request)
        books = WorkOrder.objects.filter(isScheduling=True)
        books=filterUser(request,books)
        wos=SWOUtility.doPaging(request,books)

        data['html_swo_list'] = render_to_string('cmms/sworkorder/partialWoList.html', {
            'wo': wos,
            'perms': PermWrapper(request.user)
        })
        data['html_swo_paginator'] = render_to_string('cmms/sworkorder/partialWoPagination2.html', {'wo': wos           })
        return JsonResponse(data)
def swo_asset_Search(request):
    data=dict()
    q=request.GET.get("q","")
    asset_loc=request.GET.get("asset_loc","0")
    asset_cat=request.GET.get("asset_cat","0")
    assets=AssetUtility.seachAsset2(q)
    wos=AssetUtility.doPaging(request,assets)
    form=CopyAssetForm()
    q=request.GET.get('q','')
    data["modalcopyasset"]=render_to_string('cmms/asset/partialAssetList_swo.html',{'asset':wos,'asset_cat':asset_cat,
    'asset_loc':asset_loc,'perms': PermWrapper(request.user),'form':form})
    data['html_asset_paginator'] = render_to_string('cmms/asset/partialAssetPagination_swo_search.html', {
                      'asset': wos,'pageType':'swo_asset_Search','ptr':0,'q':q})
    data['form_is_valid']=True
    return JsonResponse(data)
def swo_Update_Task_User(request,woid,uid):
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
        'ispm':True
        })
    data['form_is_valid']=True
    return JsonResponse(data)
