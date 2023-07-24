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
from cmms.models import *
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
from django.core import serializers
import logging
from django.conf import settings
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.business.mttr import *
from cmms.business.misccost import *
from cmms.business.DateJob import *
from cmms.business.WOUtility import *
from cmms.business.AssetUtility import *
from cmms.business.amarutility import *
from cmms.business.UserUtility import *
from cmms.business.PartUtility import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
import json
from django.http import JsonResponse
from django.db.models import F
from django.urls import reverse
import collections
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
# Create your views here.
import datetime
def index(request):
    today=1
    return render(request,"cmms/mainTheme.html",{"today" : today})
    ###################################################################
@login_required
def list_dashboard_ceo(request):
    user1=SysUser.objects.get(userId=request.user)
    # print("here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    request.session['userpic'] = str(user1.profileImage)
    request.session['username'] = str(user1.fullName)
    request.session['usertitle'] = str(user1.title)
    darayee=Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1).order_by('assetName')
    return render(request,"cmms/dashboards/ceo.html",{"darayee" : darayee,'section':'list_dashboard_ceo'})
@login_required
def list_dashboard(request):
    today=1


    user1=SysUser.objects.get(userId=request.user)
    # print("here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    request.session['userpic'] = str(user1.profileImage)
    request.session['username'] = str(user1.fullName)
    request.session['usertitle'] = str(user1.title)


    if(user1.userId.groups.filter(name= 'director').exists()):
        return render(request,"cmms/dashboards/director.html",{"today" : today,'user2':user1})
    elif((user1.userId.groups.filter(name= 'director').exists())):
        return render(request,"cmms/dashboards/director.html",{"today" : today,'user2':user1})
    elif((user1.userId.groups.filter(name= 'manager').exists())):
        dashugroups=UserGroup.objects.all().exclude(userGroupName="سایر")
        gid=UserGroup.objects.all().exclude(userGroupName="سایر").values_list('id',flat=True)
        darayee=Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1).order_by('assetName')
        return render(request,"cmms/dashboards/manager.html",{"dashugroups" : dashugroups,'ggid':list(gid),'user2':user1,'naghsh':'کاربر PM','darayee':darayee,'section':'dashboard','dash_name':'داشبورد اپراتور'})
    elif((user1.userId.groups.filter(name= 'suboperator').exists())):

        dashugroups=UserGroup.objects.all().exclude(userGroupName="سایر")
        request.session['operator'] = True
        gid=UserGroup.objects.all().exclude(userGroupName="سایر").values_list('id',flat=True)
        darayee=Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1).order_by('assetName')
        return render(request,"cmms/dashboards/operator3.html",{"dashugroups" : dashugroups,'ggid':list(gid),'user2':user1,'naghsh':'اپراتور','darayee':darayee,'section':'dashboard','dash_name':'داشبورد اپراتور'})
    else:
        # request.session['operator'] = True

        # return HttpResponseRedirect(reverse('list_wo'))
        return render(request,"cmms/dashboards/main.html",{"today" : today,'user2':user1,'section':'dashboard','menu':'opmenu.html'})
    # return render(request,"cmms/dashboards/main.html",{"today" : today,'user2':user1})




    ###################################################################
def dash_getDashPMPALL(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    loc=request.GET.get('loc',False)
    n1=[]
    print('loc',loc)
    if(loc=='-1'):
        n1=WorkOrder.objects.raw("select get_numberof_planned_maintenance_hours_all('{0}','{1}') as id ,get_numberof_unplanned_maintenance_hours_all('{0}','{1}') as unpm".format(start,end))
    else:
        n1=WorkOrder.objects.raw("select get_numberof_planned_maintenance_hours_loc('{0}','{1}',{2}) as id ,get_numberof_unplanned_maintenance_hours_loc('{0}','{1}',{2}) as unpm".format(start,end,loc))
    data['pm']=n1[0].id
    data['unpm']=n1[0].unpm
    return JsonResponse(data)




def GetWoPartNum(request,startHijri,endHijri):
    data=dict()

    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=PartUtility.getUsedPartNum(start,end)
    #n2=WorkorderPart.objects.raw("SELECT  count(woPartActulaQnty) as id  from workorderpart where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH)")
    data['html_monthlywopartnumrep_list'] = render_to_string('cmms/summery/partialwopart.html', {
                'x1': n1,
                #'x2':n2

            })
    data['html_is_valid']=True

    return JsonResponse(data)
def GetWoPartNum2(request,startHijri,endHijri,loc):
    data=dict()

    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=PartUtility.getUsedPartNum2(start,end,loc)
    #n2=WorkorderPart.objects.raw("SELECT  count(woPartActulaQnty) as id  from workorderpart where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH)")
    data['html_monthlywopartnumrep_list'] = render_to_string('cmms/summery/partialwopart.html', {
                'x1': n1,
                #'x2':n2

            })
    data['html_is_valid']=True

    return JsonResponse(data)
##############################################
def GeStopNum(request,startHijri,endHijri):
    data=dict()

    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=AssetUtility.getAssetOfflineTime(start,end)
    #n2=WorkorderPart.objects.raw("SELECT  count(woPartActulaQnty) as id  from workorderpart where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH)")
    data['html_stopnumrep_list'] = render_to_string('cmms/summery/stopNum.html', {
                'x1': n1/60,
                #'x2':n2

            })
    data['html_is_valid']=True

    return JsonResponse(data)
def GeStopNum2(request,startHijri,endHijri,loc):
    data=dict()

    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=AssetUtility.getAssetOfflineTime2(start,end,loc)
    #n2=WorkorderPart.objects.raw("SELECT  count(woPartActulaQnty) as id  from workorderpart where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH)")
    data['html_stopnumrep_list'] = render_to_string('cmms/summery/stopNum.html', {
                'x1': n1,
                #'x2':n2

            })
    data['html_is_valid']=True

    return JsonResponse(data)
    ###################################################################
def GetWoReqNum(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.getWoReqNum(start,end)
    #n2=WorkOrder.objects.raw("SELECT  count(id) as id  from workorder where pmonth(datecreated) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH) and isScheduling=0" )
    data['html_monthlyworeqnumrep_list'] = render_to_string('cmms/summery/partialworequest.html', {
                'x1': n1,
                #'x2':n2

            })
    data['html_is_valid']=True

    return JsonResponse(data)
def GetWoReqNum2(request,startHijri,endHijri,loc):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)

    n1=WOUtility.getWoReqNum2(start,end,loc)

    #n2=WorkOrder.objects.raw("SELECT  count(id) as id  from workorder where pmonth(datecreated) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH) and isScheduling=0" )
    data['html_monthlyworeqnumrep_list'] = render_to_string('cmms/summery/partialworequest.html', {
                'x1': n1,
                #'x2':n2

            })
    data['html_is_valid']=True

    return JsonResponse(data)
    ###################################################################


def GetOpenWoReqNum(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WorkOrder.objects.raw("SELECT  count(id) as id  from workorder where datecreated between '{0}' and '{1}' and isscheduling=0".format(start,end))

    #n2=WorkOrder.objects.raw("SELECT  count(id) as id  from workorder where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH) and woStatus=5")
    data['html_openworeqnumrep_list'] = render_to_string('cmms/summery/partialopenworequest.html', {
                'x1': n1,


            })
    data['html_is_valid']=True

    return JsonResponse(data)
###################################################################

def GetCloseWoReqNum(request,startHijri,endHijri):
     data=dict()
     start,end=DateJob.convert2Date(startHijri,endHijri)
     n1=WorkOrder.objects.raw("SELECT  count(id) as id  from workorder where (datecreated between '{0}' and '{1}') and woStatus=7 and isScheduling=0".format(start,end))
     #n2=WorkOrder.objects.raw("SELECT  count(id) as id  from workorder where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH) and woStatus=5")
     data['html_closeworeqnumrep_list'] = render_to_string('cmms/summery/partialcloseworequest.html', {
                 'x1': n1,


             })
     data['html_is_valid']=True

     return JsonResponse(data)
###################################################################
def GetOverdueWoReqNum(request,startHijri,endHijri):
     data=dict()
     start,end=DateJob.convert2Date(startHijri,endHijri)
     # print("SELECT  count(id) as id  from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and current_date>requiredCompletionDate and isScheduling=0 and visibile=1 and datecreated between '{0}' and '{1}'".format(start,end))
     n1=WorkOrder.objects.raw("SELECT   count(id) as id  from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and current_date>requiredCompletionDate and isScheduling=0 and datecreated between '{0}' and '{1}'".format(start,end))
     #n2=WorkOrder.objects.raw("SELECT  count(id) as id  fr om workorder where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH) and woStatus=5")
     data['html_overdueworeqnumrep_list'] = render_to_string('cmms/summery/partialoverdueworequest.html', {
                 'x1': n1,


             })
     data['html_is_valid']=True

     return JsonResponse(data)
def GetOverdueWoReqNum2(request,startHijri,endHijri,loc):
     data=dict()
     start,end=DateJob.convert2Date(startHijri,endHijri)
     n1=WorkOrder.objects.raw("""SELECT  count(id) as id  fr om workorder
     inner join assets on workorder.woAsset_id=assets.id
      where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and
      current_date>requiredCompletionDate and isScheduling=0 and (datecreated between '{0}' and '{1}')
      and assets.assetIsLocatedAt_id={2}
      """.format(start,end,loc))
     #n2=WorkOrder.objects.raw("SELECT  count(id) as id  fr om workorder where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH) and woStatus=5")
     data['html_overdueworeqnumrep_list'] = render_to_string('cmms/summery/partialoverdueworequest.html', {
                 'x1': n1,


             })
     data['html_is_valid']=True

     return JsonResponse(data)
def GetdueWoNum(request,startHijri,endHijri):
     data=dict()
     start,end=DateJob.convert2Date(startHijri,endHijri)
     # n1=WorkOrder.objects.raw("SELECT  count(id) as id  fr om workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and current_date>requiredCompletionDate and isScheduling=0 and datecreated between '{0}' and '{1}'".format(start,end))
     #n2=WorkOrder.objects.raw("SELECT  count(id) as id  fr om workorder where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH) and woStatus=5")
     # data['html_dueservice_list'] = render_to_string('cmms/summery/partialoverdueworequest.html', {
             #     'x1': n1,
             #
             #
             # })
     no=datetime.datetime.now().date()
     # print(WorkOrder.objects.filter(woStatus__in=(1,2,4,5,6,9),woStatus__isnull=False,isPm=True,isScheduling=False,visibile=True,datecreated__range=(start,F('requiredCompletionDate'))).query)
     n1=WorkOrder.objects.filter(woStatus__in=(1,2,4,5,6,9),woStatus__isnull=False,isPm=True,isScheduling=False,visibile=True)
     # n1=n1.filter(datecreated__range=(start,F('requiredCompletionDate')))
     n1=n1.filter(datecreated__gte=start,requiredCompletionDate__gte=datetime.datetime.today()).count()
     # print(n1)
     # n1=10

     data['html_dueservice_list']=data['html_highprioritywo_list'] = render_to_string('cmms/summery/partialduedatewo.html', {
                  'x1': n1,
              })
     data['html_is_valid']=True

     return JsonResponse(data)
def GetdueWoNum2(request,startHijri,endHijri,loc):
     data=dict()
     start,end=DateJob.convert2Date(startHijri,endHijri)
     # n1=WorkOrder.objects.raw("SELECT  count(id) as id  fr om workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and current_date>requiredCompletionDate and isScheduling=0 and datecreated between '{0}' and '{1}'".format(start,end))
     #n2=WorkOrder.objects.raw("SELECT  count(id) as id  fr om workorder where pmonth(timeStamp) =pmonth(CURRENT_DATE - INTERVAL 1 MONTH) and woStatus=5")
     # data['html_dueservice_list'] = render_to_string('cmms/summery/partialoverdueworequest.html', {
             #     'x1': n1,
             #
             #
             # })
     no=datetime.datetime.now().date()
     n1=WorkOrder.objects.filter(woStatus__in=(1,2,4,5,6,9),woStatus__isnull=False,isPm=True,isScheduling=False,datecreated__range=(no,F('requiredCompletionDate')),woAsset__assetIsLocatedAt__id=loc).count()
     data['html_dueservice_list']=n1
     data['html_is_valid']=True

     return JsonResponse(data)
###################################################################
def GetMTTR(request,startHijri,endHijri):

     data=dict()
     start,end=DateJob.convert2Date(startHijri,endHijri)
     n1=MTTR.getMTTR(start,end)

     data['html_monthlymttrrep_list'] = render_to_string('cmms/summery/partialmttr.html', {
                 'x1': n1,
                # 'x2':n2

             })
     data['html_is_valid']=True

     return JsonResponse(data)
     ###################################################################
def GetMiscCost(request,startHijri,endHijri):

     data=dict()
     start,end=DateJob.convert2Date(startHijri,endHijri)
     ###From ExtraCoast Class
     n1=ExtraCost.getMiscCost(start,end)


     data['html_monthlymiscrep_list'] = render_to_string('cmms/summery/partialmisc.html', {
                 'x1': n1,
                 #'x2':n2

             })
     data['html_is_valid']=True

     return JsonResponse(data)
def GetMiscCost2(request,startHijri,endHijri,loc):

     data=dict()
     start,end=DateJob.convert2Date(startHijri,endHijri)
     ###From ExtraCoast Class
     n1=ExtraCost.getMiscCost2(start,end,loc)
     # print(n1[0].id)

     data['html_monthlymiscrep_list'] = render_to_string('cmms/summery/partialmisc.html', {
                 'x1': n1,
                 #'x2':n2

             })
     data['html_is_valid']=True

     return JsonResponse(data)
     ###################################################################
def GetHighPriorityWO(request,startHijri,endHijri):
    data=dict()

    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.GetHighPriorityWO(start,end)
    data['html_highprioritywo_list'] = render_to_string('cmms/summery/partialhighprioritywo.html', {
                 'x1': n1,
             })
    return JsonResponse(data)
def GetHighPriorityWO2(request,startHijri,endHijri,loc):
    data=dict()

    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.GetHighPriorityWO2(start,end,loc)
    data['html_highprioritywo_list'] = render_to_string('cmms/summery/partialhighprioritywo.html', {
                 'x1': n1,
             })
    return JsonResponse(data)
     ###################################################################
def GetRequestedWo(request,startHijri,endHijri):
    data=dict()

    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.getRequestedWo(start,end)
    data['html_requestedwo_list'] = render_to_string('cmms/summery/partialrequestedwo.html', {
                 'x1': n1,
             })
    return JsonResponse(data)
    ###################################################################


def GetLowItemStock(request):
     data=dict()
     n1=Stock.objects.raw("select count(id) as id ,sum(qtyOnHand) as q1 ,sum(minQty) as q2, stockItem_id from stocks group by stockItem_id,location_id having q1<q2 ")
     data['html_lowitemstock_list'] = render_to_string('cmms/summery/partiallowitemstock.html', {
                  'x1': len(list(n1)),
              })
     return JsonResponse(data)

#############################################################نمودارهای دایره ای##################
def dash_GetCompletedWo(request,startHijri,endHijri,isScheduling):
    data=dict()
    searchPtr="is not null" if isScheduling=='1' else "is NULL"
    makan=request.GET.get("makan",False)

    start,end=DateJob.convert2Date(startHijri,endHijri)
    if(makan=='-1'):
        n1=WOUtility.GetCompletedWorkOrderNum(start,end,searchPtr)

        n2=WOUtility.GetOnTimeCompletedWorkOrderNum(start,end,searchPtr)
    else:
        n1=WOUtility.GetCompletedWorkOrderNum(start,end,searchPtr,makan)
        n2=WOUtility.GetOnTimeCompletedWorkOrderNum(start,end,searchPtr,makan)
    data['html_dashwoCompleted_list'] ={
                 'woCompletedNum': n1,
                 'woCompletedOnTimeNum':n2
                              }
    return JsonResponse(data)
################################################################################################
def dash_GetTotalCompletedWo(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.GetTotalCompletedWorkOrderNum(start,end)
    n2=WOUtility.GetTotalOnTimeCompletedWorkOrderNum(start,end)
    data['html_dashwoCompleted_list'] ={
                 'woCompletedNum': n1[0].id,
                 'woCompletedOnTimeNum':n2[0].id
                              }
    return JsonResponse(data)

###############################################################################
def dash_GetAllWorkOrders(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.GetTotalCompletedWorkOrderNum(start,end)

    n2=WOUtility.GetTotalOnTimeCompletedWorkOrderNum(start,end)
    N3=WOUtility.GetAvgDaysToCompletedNum(start,end)

    n3=0
    if(N3[0].id):
        n3=N3[0].id



    n4=WOUtility.GetAvgTotalCostPerWO(start,end)
    print("{0}/{1}/{2}/{3}".format(n1[0].id,n2[0].id,n3,n4))
    data['html_dashAllWorkOrders_list'] ={
                 'TotalwoCompletedNum': n1[0].id,
                 'TotalOnTimeCompletedWorkOrderNum': n2[0].id,
                 'GetAvgDaysToCompletedNum':"{:2.0f}".format(n3),
                 'GetAvgTotalCostPerWO':'{:20,.0f}'.format(n4)
                              }
    return JsonResponse(data)

#####################################
def dash_getResource(request,startHijri,endHijri):
    data=dict()
    location=request.GET.get("loc",False)
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.getResources(start,end,location)

    data['html_dashAllResource_list'] =render_to_string('cmms/summery/partialResource.html', {
                'res': n1,
                #'x2':n2

            })
    return JsonResponse(data)
############################################
def dash_getDashMTTR(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    loc=request.GET.get('loc',False)
    mttrs=MTTR.getMTTRAll2(start,end,location=loc)
    s1=[]
    s2=[]
    for i in mttrs:
         s1.append(float(i.id))
         s2.append(str(jdatetime.date.fromgregorian(date=i.dt1)))
    data['html_dashMTTR_list'] ={
                's1': s1,
                's2':s2

            }
    return JsonResponse(data)
############################################
def dash_getDashTolid(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    loc=request.GET.get('loc',False)
    amar1,amar2=AmarUtility.getTolid(start,end,location=loc)
    s1=[]
    s2=[]
    dt={}
    dt['total']=[]
    for i in amar1:
         s1.append(float(i.id))
         s2.append(str(jdatetime.date.fromgregorian(date=i.assetAmarDate)))
         dt['total'].append({str(jdatetime.date.fromgregorian(date=i.assetAmarDate)):i.id})
    for i in amar2:
        dt[str(i.shifttypes)]=[]#={str(i.assetAmarDate):i.id}
    # dt['total']=[]#={str(i.assetAmarDate):i.id}
    for i in amar2:
        dt[str(i.shifttypes)].append({str(jdatetime.date.fromgregorian(date=i.assetAmarDate)):i.id})

    data['html_dashMTTR_list'] ={
                's1': s1,
                's2':s2,
                's3':dt

            }
    return JsonResponse(data)
def dash_getDashTolidBar(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    loc=request.GET.get('loc',False)
    amar1=AmarUtility.getTolidBar(start,end,location=loc)

    s1=[]
    s2=[]
    dt={}
    # dt['total']=[]
    if(amar1):
        for i in amar1:
            if(i):
            # print(i.id)
                dt[i.jalali_month]=[]

        for i in amar1:
            dt[i.jalali_month].append({'val':i.sum_value,'loc':i.id,'mah':i.jalali_month,'sal':i.jalali_year})
        # sum_a = sum(float(item['value']) for item in data['A'] if item['value'])
        # # print(data['A'][0]['value'].isdigit())
        # sum_b = sum(float(item['value']) for item in data['B'] if item['value'])
        # sum_c = sum(float(item['value']) for item in data['C'] if item['value'])
        data['html_dashMTTR_list'] ={

                    's3':dt

                }
    else:
        data['html_dashMTTR_list'] ={

                    's3':[]

                }
    return JsonResponse(data)
@api_view(['GET'])
def dash_getDashTolidBarAPI(request,loc):
    data=dict()
    # start,end=DateJob.convert2Date(startHijri,endHijri)
    # loc=request.GET.get('loc',False)
    amar1=AmarUtility.getTolidBarAPI(location=loc)
    s1=[]
    s2=[]
    dt=dict()
    dt['total']=[]
    for i in amar1:
         # s1.append(float(i.id))
         # s2.append(str(jdatetime.date.fromgregorian(date=i.assetAmarDate)))
         # dt['total'][str(jdatetime.date.fromgregorian(date=i.assetAmarDate))]=i.id
         dt['total'].append({'date':str(jdatetime.date.fromgregorian(date=i.assetAmarDate)),'value':i.id})
    # for i in amar2:
        # dt[str(i.shifttypes)]=[]#={str(i.assetAmarDate):i.id}
    # dt['total']=[]#={str(i.assetAmarDate):i.id}
    # for i in amar2:
    #     dt[str(i.shifttypes)].append({str(jdatetime.date.fromgregorian(date=i.assetAmarDate)):i.id})

    # serialized_data = TotalDataSerializer(dt, many=True)
    # return Response(serialized_data.data)
    return JsonResponse(dt['total'],safe=False)
############################################
def dash_getDashTolidTime(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    loc=request.GET.get('loc',False)
    # if(loc=='6961'):
    #     amar1,amar2=AmarUtility.getTolid(start,end,location=loc)
    # else:
    amar1,amar2=AmarUtility.getTolidTime(start,end,location=loc)
    s1=[]
    s2=[]
    dt={}
    dt['total']=[]
    for i in amar1:
         s1.append(float(i.id))
         s2.append(str(jdatetime.date.fromgregorian(date=i.assetAmarDate)))
         dt['total'].append({str(jdatetime.date.fromgregorian(date=i.assetAmarDate)):i.id})
    for i in amar2:
        dt[str(i.shifttypes)]=[]#={str(i.assetAmarDate):i.id}
    # dt['total']=[]#={str(i.assetAmarDate):i.id}
    for i in amar2:
        dt[str(i.shifttypes)].append({str(jdatetime.date.fromgregorian(date=i.assetAmarDate)):i.id})

    # print(amar)
    data['html_dashMTTR_list'] ={
                's1': s1,
                's2':s2,
                's3':dt

            }
    return JsonResponse(data)


#############################################
def dash_getWoByStatus(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    w1=WOUtility.getWoStatusCount(start,end,1)
    w2=WOUtility.getWoStatusCount(start,end,2)
    w3=WOUtility.getWoStatusCount(start,end,3)
    w4=WOUtility.getWoStatusCount(start,end,4)
    w5=WOUtility.getWoStatusCount(start,end,5)
    w6=WOUtility.getWoStatusCount(start,end,6)
    w7=WOUtility.getWoStatusCount(start,end,7)
    w8=WOUtility.getWoStatusCount(start,end,8)
    w9=WOUtility.getWoStatusCount(start,end,9)
    w10=WOUtility.getOverDueWo(start,end)
    print("w10:{0},w9:{1},w2:{2}".format(w10[0].id,w9[0].id,w2[0].id))

    ##############
    p1=WOUtility.getPmStatusCount(start,end,1)
    p2=WOUtility.getPmStatusCount(start,end,2)
    p3=WOUtility.getPmStatusCount(start,end,3)
    p4=WOUtility.getPmStatusCount(start,end,4)
    p5=WOUtility.getPmStatusCount(start,end,5)
    p6=WOUtility.getPmStatusCount(start,end,6)
    p7=WOUtility.getPmStatusCount(start,end,7)
    p8=WOUtility.getPmStatusCount(start,end,8)
    p9=WOUtility.getPmStatusCount(start,end,9)
    p10=WOUtility.getOverDuePm(start,end)
    data['html_dashWoStatus_list']={'dash_WoStatus_w1':w1[0].id,'dash_WoStatus_w2':w2[0].id,'dash_WoStatus_w3':w3[0].id,'dash_WoStatus_w4':w4[0].id,'dash_WoStatus_w5':w5[0].id,
                                    'dash_WoStatus_w6':w6[0].id,'dash_WoStatus_w7':w7[0].id,'dash_WoStatus_w8':w8[0].id,'dash_WoStatus_w9':w9[0].id,'dash_WoStatus_w10':w10[0].id,
                                    'dash_PmStatus_p1':p1[0].id,'dash_PmStatus_p2':p2[0].id,'dash_PmStatus_p3':p3[0].id,'dash_PmStatus_p4':p4[0].id,'dash_PmStatus_p5':p5[0].id,
                                    'dash_PmStatus_p6':p6[0].id,'dash_PmStatus_p7':p7[0].id,'dash_PmStatus_p8':p8[0].id,'dash_PmStatus_p9':p9[0].id,'dash_PmStatus_p10':p10[0].id,}
    return JsonResponse(data)
#############################
def dash_GetCompletedWoDonat(request,startHijri,endHijri):
    data=dict()
    print("*******dsadsa***************")
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1,n2=WOUtility.getCompletedWoByAsset(start,end)
    s1,s2=[],[]
    z1,z2=[],[]
    for i in n1:
        s1.append(i.id)
        s2.append(i.assetname)
    for i  in n2:
        s1.append(i.id)
        s2.append('سایر')

    data['html_dashWoStatusDonat_list'] ={'woCompletedNum': s1,
                                    'woCompletedAssetId':s2,
                                    'woCompletedNotInList':z1
                                    }
    #data2 = serializers.serialize('json', data)
    return JsonResponse(data)

    #####################################
def dash_getEquipDownTime(request,startHijri,endHijri):
        data=dict()
        start,end=DateJob.convert2Date(startHijri,endHijri)
        # print("here")
        n1=AssetUtility.getEquipmentDownTime(start,end)
        s1,s2=[],[]
        for i in n1:
            s1.append(i.id)
            s2.append(i.assetname)
        data['html_dashEqDownTime_list'] = {
                    'dt1': s1,
                    'dt2':s2
                    #'x2':n2

                }
        return JsonResponse(data)
#####################################
def dash_getEquipCost(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=AssetUtility.getEquipmentCost(start,end)
    s1,s2=[],[]
    for assetName, assetCost in n1.items():
        s1.append(assetName)
        s2.append(format(assetCost/1000000,'.2f'))
    data['html_dashEqCost_list'] = {
                'dt1': s1,
                'dt2':s2
                #'x2':n2
                }
    return JsonResponse(data)
##########################################################
##########################################################
def dash_getDashIstgahStatus(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1,n2,n3=AssetUtility.getDashIstgahStatus(start,end)

    data['html_DashIstgahStatus_list'] = {
                'dt1': n1,
                'dt2':n2,
                'dt3':n3 #assetname

                #'x2':n2
                }
    return JsonResponse(data)
def dash_getDashIstgahStatus2(request,startHijri,endHijri,loc):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1,n2,n3=AssetUtility.getDashIstgahStatusWithLocation(start,end,loc)

    data['html_DashIstgahStatus_list'] = {
                'dt1': n1,
                'dt2':n2,
                'dt3':n3 #assetname

                #'x2':n2
                }
    return JsonResponse(data)
############################################
def dash_getDashCauseCount(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.getDashCauseCount(start,end)

    data['html_DashCAuseCount_list'] = {
                'dt1': n1,

                }
    return JsonResponse(data)
def dash_getDashCauseCount2(request,startHijri,endHijri,loc):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.getDashCauseCount2(start,end,loc)

    data['html_DashCAuseCount_list'] = {
                'dt1': n1,

                }
    return JsonResponse(data)
############################################
def dash_getDashResourceStatus(request,startHijri,endHijri,gid):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=TaskUtility.getWorkHourByGid(start,end,gid)
    n2=UserUtility.getHozurTimeGid(start,end,gid)
    mid=MaintenanceType.objects.all()
    d={}
    for k in mid:
        d[k.name]=TaskUtility.getGroupMaintenance(start,end,gid,k.id)
        d['c_'+k.name]=k.color

    data['html_DashResourceStatus_list'] = {
                'dt1': int(n1),
                'dt2':n2,
                'dt3':d


                #'x2':n2
                }
    return JsonResponse(data)
def dash_getDashResourceStatus2(request,startHijri,endHijri,gid,loc):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=TaskUtility.getWorkHourByGid2(start,end,gid,loc)
    n2=UserUtility.getHozurTimeGid2(start,end,gid,loc)
    mid=MaintenanceType.objects.all()
    d={}
    for k in mid:
        d[k.name]=TaskUtility.getGroupMaintenance(start,end,gid,k.id)
        d['c_'+k.name]=k.color

    data['html_DashResourceStatus_list'] = {
                'dt1': int(n1),
                'dt2':n2,
                'dt3':d


                #'x2':n2
                }
    return JsonResponse(data)
# EM
def GetEmCount(request,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.getEmCount(start,end)

    data['html_emwo_list'] = {
                'dt1': n1,

                }
    return JsonResponse(data)
def GetEmCount2(request,startHijri,endHijri,loc):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    n1=WOUtility.getEmCount2(start,end,loc)

    data['html_emwo_list'] = {
                'dt1': n1,

                }
    return JsonResponse(data)
def dash_GetReactivevsRepatable(request,startHijri,endHijri):
    data=dict()
    loc=request.GET.get('loc',False)
    where=""
    if(loc!='-1' ):
        where="and t3.woAsset_id in (select id from assets where id ={0} or assetIsLocatedAt_id={0})".format(loc)
    start,end=DateJob.convert2Date(startHijri,endHijri)
    fixtime=WorkOrder.objects.raw("""
     select COALESCE(sum(timestampdiff(MINute,cast(concat(t1.taskStartDate, ' ', t1.taskStartTime)
     as datetime),cast(concat(t1.taskDateCompleted, ' ',t1.taskTimeCompleted) as datetime))),0) as id
     ,t1.taskstartdate dt1 from tasks as t1 join workorder as t3 on t1.workorder_id=t3.id
     where t3.datecreated between '{0}' and '{1}'  and t3.visibile=1 and
      t3.isScheduling=0   and t3.maintenanceType_id=18 {2}
      group by dt1
      having id>0
            """.format(start,end,where))
    print("""
     select COALESCE(sum(timestampdiff(MINute,cast(concat(t1.taskStartDate, ' ', t1.taskStartTime)
     as datetime),cast(concat(t1.taskDateCompleted, ' ',t1.taskTimeCompleted) as datetime))),0) as id
     ,t1.taskstartdate dt1 from tasks as t1 join workorder as t3 on t1.workorder_id=t3.id
     where t3.datecreated between  '{0}' and '{1}'  and t3.visibile=1 and
      t3.isScheduling=0   and t3.maintenanceType_id=10 {2}
      group by dt1
      having id>0
            """.format(start,end,where))
    servicetime=WorkOrder.objects.raw("""
     select COALESCE(sum(timestampdiff(MINute,cast(concat(t1.taskStartDate, ' ', t1.taskStartTime)
     as datetime),cast(concat(t1.taskDateCompleted, ' ',t1.taskTimeCompleted) as datetime))),0) as id
     ,t1.taskstartdate dt1 from tasks as t1 join workorder as t3 on t1.workorder_id=t3.id
     where t3.datecreated between  '{0}' and '{1}'  and t3.visibile=1 and
      t3.isScheduling=0   and t3.maintenanceType_id=10 {2}
      group by dt1
      having id>0
            """.format(start,end,where))
    n1=[]
    n2=[]
    n22={}
    n3=[]
    n4=[]
    nt2={}
    nt3={}
    for i in fixtime:
        n1.append(float(i.id/60))
        n2.append(str(jdatetime.date.fromgregorian(date=i.dt1)))
        nt2[str(jdatetime.date.fromgregorian(date=i.dt1))]=float(i.id/60)
        # n22["str(jdatetime.date.fromgregorian(date=i.dt1))"]
    for i in servicetime:
        n3.append(float(i.id/60))
        n4.append(str(jdatetime.date.fromgregorian(date=i.dt1)))
        nt3[str(jdatetime.date.fromgregorian(date=i.dt1))]=float(i.id/60)
    nset=set(tuple(n2)+tuple(n4))
    # print(nset,"nset")
    for i in nset:
        if(not i in nt2):
            nt2[i]=0
        if(not i in nt3):
            nt3[i]=0
    order_fix=collections.OrderedDict(sorted(nt2.items()))
    order_service=collections.OrderedDict(sorted(nt3.items()))
    # print()
    # print(collections.OrderedDict(sorted(nt3.items())))
    lbl=[]
    v1=[]
    v2=[]
    for i in order_fix:
        lbl.append(i)
        v1.append(order_fix[i])
    for i in order_service:
        # lbl.append(i)
        v2.append(order_service[i])





    data['data'] = {
                'tamir': v1,
                'ttime':lbl,'service':v2,'ftime':lbl

                }
    return JsonResponse(data)
