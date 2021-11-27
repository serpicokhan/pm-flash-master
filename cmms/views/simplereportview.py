'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nesimpleReportbject.OrderId.id)
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
from django.db.models import Q,F
#from cmms.models.report import *
from cmms.models import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import SimpleReportForm
from django.urls import reverse_lazy
from django.db import transaction
from cmms.business.reportbuilder import *
from cmms.business.AssetUtility import *
from cmms.business.mttr import *
from cmms.business.WOUtility import *
from cmms.business.UserUtility import *
from cmms.business.schedule_utility import *
from cmms.business.SWOUtility import *
from django.contrib.admin.models import LogEntry
from django.db.models import Sum
# import weasyprint
# from django.conf import settings


def list_simpleReport(request,id=None):
    #
    books = Report.objects.all()
    return render(request, 'cmms/reports/main.html', {'simpleReports': books})
##########################################################
def save_simpleReport_form(request, form, template_name,repId):
    data = dict()
    if (request.method == 'POST'):
        # if form.is_valid():
            # form.save()
            data['form_is_valid'] = True
            # books = Report.objects.all()
            # data['html_simpleReport_list'] = render_to_string('cmms/simplereports/partialReportlist.html', {
            # 'simpleReports': books
            # })
            # data['form_is_valid'] = True
            # else:
            # data['form_is_valid'] = False
            pass
    #form2 form asli sazande
    #form form create
    context = {'form': form,'lId':repId}


    data['html_simpleReport_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def simpleReport_delete(request, id):
    comp1 = get_object_or_404(Report, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  Report.objects.all()
        #Tasks.objects.filter(simpleReportId=id).update(simpleReport=id)
        data['html_simpleReport_list'] = render_to_string('cmms/reports/simplereports/partialReportlist.html', {
            'simpleReport': companies
        })
    else:
        context = {'simpleReport': comp1}
        data['html_simpleReport_form'] = render_to_string('cmms/reports/simplereports/partialSimpleReportDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def simpleReport_create(request,repType=None):
    #if(repType==1):
        if (request.method == 'POST'):
            books = Report.objects.all()
            return render(request, 'cmms/reports/main.html', {'reports': books})
            # form = SimpleReportForm(request.POST)
            # return save_simpleReport_form(request, form, 'cmms/reports/simplereports/partialReportCreate.html')
        else:
            form,tmpAddr =ReportBuilder.build(repType)
            return save_simpleReport_form(request, form, 'cmms/reports/simplereports/partialSimpleReportCreate.html',repType)
##########################################################
def simpleReport_update(request, repType):
    company= get_object_or_404(Report, id=repType)

    if (request.method == 'POST'):
        form = ReportForm(request.POST, instance=company)
    else:
        form = ReportForm(instance=company)


    return save_simpleReport_form(request, form,"cmms/reports/simplereports/partialSimpleReportUpdate.html",repType)
##########################################################
def simpleReportBroker(request,lId):
    # print('PPPPPPPPPPPPPPP',lId)
    #
    rep=Report.objects.get(id=lId)

    m= globals()['reporttest']()
    # return m.MTTRAll(request)
    return getattr(m, rep.reportClassName)(request)
    # m=reporttest()
    # return m.MTBFAll(request)

    # return getMTBFAll(request)

##########################################################
class reporttest:

    def MTBFALL(self,request):
         date1=DateJob.getDate2(request.POST.get("startDate",""))
         date2=DateJob.getDate2(request.POST.get("endDate",""))
         startDate=request.POST.get("startDate","").replace('-','/')
         endDate=request.POST.get("endDate","").replace('-','/')
         # mtbf=MTTR.getMTBFALL2(date1,date2)
         mtbf=MTTR.getMtbfAll(date1,date2)
         return render(request, 'cmms/reports/simplereports/MTBFALL.html',{'mtbf': mtbf,'start':startDate,'end':endDate})
    def WorkOrderPartUsageHistory(self,request):

        # print(request.Post)
        # print(request.POST.getlist("part", ""))
        parts=request.POST.getlist("part", "")
        date1=DateJob.getDate2(request.POST.get("craeteAfter",""))
        # rawdate1=request.POST.get("craeteAfter","")
        # rawdate2=request.POST.get("craeteBefore","")
        rawdate1=request.POST.get("craeteAfter","").replace('-','/')
        rawdate2=request.POST.get("craeteBefore","").replace('-','/')

        partNames=Part.objects.filter(id__in=parts).values_list('partName',flat=True)
        date2=DateJob.getDate2(request.POST.get("craeteBefore",""))
        wo=WorkOrder.objects.filter(datecreated__range=(date1,date2),isScheduling=False).values_list('id', flat=True)
        woparts=WorkorderPart.objects.filter(woPartStock__stockItem__in=parts,woPartWorkorder__in=wo,woPartActulaQnty__gte=1)
        return render(request, 'cmms/reports/simplereports/WorkOrderPartUsageHistory.html', {'woparts': woparts,'date1':rawdate1,'date2':rawdate2,'parts':list(partNames)})


    def PartUsageHistory(self,request):


        parts=request.POST.get("part", None)
        print(parts,"######################")


        date1=DateJob.getDate2(request.POST.get("startDate",""))
        rawdate1=request.POST.get("startDate","").replace('-','/')
        rawdate2=request.POST.get("endDate","").replace('-','/')
        partNames=[]
        if(parts):
            partNames=Part.objects.filter(id__in=parts)
        else:
            partNames=Part.objects.all()

        date2=DateJob.getDate2(request.POST.get("endDate",""))
        wo=WorkOrder.objects.filter(datecreated__range=(date1,date2),isScheduling=False).values_list('id', flat=True)
        woparts=[]
        if(parts):
            woparts=WorkorderPart.objects.filter(woPartStock__stockItem_id=parts, woPartWorkorder__in=wo,woPartActulaQnty__gte=1).order_by('-woPartWorkorder__datecreated')
        else:
            woparts=WorkorderPart.objects.filter(woPartWorkorder__in=wo,woPartActulaQnty__gte=1).order_by('-woPartWorkorder__datecreated','-woPartStock__stockItem__partName')
        return render(request, 'cmms/reports/simplereports/PartUsageHistory.html', {'woparts': woparts,'date1':rawdate1,'date2':rawdate2,'parts':partNames})
    def OveralPartUsageHistory(self,request):



        date1=DateJob.getDate2(request.POST.get("startDate",""))
        rawdate1=request.POST.get("startDate","").replace('-','/')
        rawdate2=request.POST.get("endDate","").replace('-','/')


        date2=DateJob.getDate2(request.POST.get("endDate",""))
        wo=WorkOrder.objects.filter(datecreated__range=(date1,date2),isScheduling=False).values_list('id', flat=True)
        woparts=[]
        woparts=WorkorderPart.objects.filter(woPartWorkorder__in=wo,woPartActulaQnty__gte=1).order_by('-woPartWorkorder__datecreated')
        return render(request, 'cmms/reports/simplereports/OveralPartUsageHistory.html', {'woparts': woparts,'date1':rawdate1,'date2':rawdate2})


    def AssetList(self,request):
        categoryText=request.POST.getlist("categoryText", None)
        locationVal=request.POST.getlist("locationVal", "")
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        categoryText=[int(i) for i in categoryText]
        if(len(locationVal) >0 and not locationVal[0]):
            locationVal.pop(0)
        locationVal=[int(i) for i in locationVal]
        assetlist=AssetUtility.getAssetListByNameAndLocation(categoryText,locationVal)
        return render(request, 'cmms/reports/simplereports/AssetList.html',{'assetlist': assetlist})


    def DowntimeByRepairTypeByAssetCategory(self,request):
        categoryText=request.POST.getlist("categoryText", "")
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)

        categoryText=[int(i) for i in categoryText]

        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        assetList=AssetUtility.getAssetListByCategory(categoryText)
        # print("#######",assetList)
        ########### GERnetare output####################
        ##############count by event type ###################
        ##############sum ofline time by event type############
        s1,s2=[],[]
        z1,z2=[],[]
        offlineCountByEvent=AssetUtility.getOfflineCountByEvent(assetList,date1,date2)
        # print(offlineCountByEvent,'$$$$$$$$$$$$$$$$$$$$')
        offlineSumTimeByEvent=AssetUtility.getOfflineSumTimeByEvent(assetList,date1,date2)
        for i in offlineCountByEvent:
            s1.append(i.id)
            s2.append(i.eventname)
        for i in offlineSumTimeByEvent:
            z1.append(int(i.id))
            z2.append(i.eventname)

        #
        #convert assetlist to tuple for sql query compatibility means: Rawquery([1,2,3])==>(1,2,3)



        return render(request, 'cmms/reports/simplereports/DowntimeByRepairTypeByAssetCategory.html',{'s1': s1,'s2':s2,'z1': z1,'z2':z2,'start':startDate,'end':endDate})

    def MTTRALL(self,request):
         print("!!!!!!!!!!!!!!!!!!")
         date1=DateJob.getDate2(request.POST.get("startDate",""))
         date2=DateJob.getDate2(request.POST.get("endDate",""))
         startDate=request.POST.get("startDate","")
         endDate=request.POST.get("endDate","")
         mttrs=MTTR.getMTTRAll(date1,date2)
         return render(request, 'cmms/reports/simplereports/MTTRALL.html',{'mttrs': mttrs,'start':startDate,'end':endDate})

    def MTTRByCategory(self,request):
        categoryText=request.POST.get("categoryText", "")
        catText='-1'
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        mttrs=MTTR.getMTTRByCategory(categoryText,date1,date2)
        return render(request, 'cmms/reports/simplereports/MTTRByCategory.html',{'mttrs': mttrs,'start':startDate,'end':endDate})
    def MTBFByCategory(self,request):
         categoryText=request.POST.get("categoryText", "")
         catText='-1'
         date1=DateJob.getDate2(request.POST.get("startDate",""))
         date2=DateJob.getDate2(request.POST.get("endDate",""))
         startDate=request.POST.get("startDate","").replace('-','/')
         endDate=request.POST.get("endDate","").replace('-','/')
         mtbf=MTTR.getMTBFByCategory(categoryText,date1,date2)
         return render(request, 'cmms/reports/simplereports/MTBFByCategory.html',{'mtbf': mtbf,'start':startDate,'end':endDate})
    def OverdueWorkOrdersDetailReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")
        priorityType=request.POST.getlist("priorityType", "")
        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            print(assignUser,"##########################")
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        if(len(priorityType) >0 and not priorityType[0]):
            priorityType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]
        priorityType=[int(i) for i in priorityType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(priorityType)==1):
            priorityType.append(-1)

        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getOverdueWorkOrdersDetailReport(date1,date2,tuple(assignUser),tuple(asset),tuple(categoryText),tuple(maintenanceType),tuple(priorityType)))
        tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها
        for i in woList:
            tasks=Tasks.objects.filter(workOrder=i.id)
            tasklist.append(tasks)
        #ادغام دو queryset
        woListDic=zip(woList,tasklist)

        return render(request, 'cmms/reports/simplereports/OverdueWorkOrdersDetailReport.html',{'woList':woListDic,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})

    def OpenWorkOrdersDetailReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")
        priorityType=request.POST.getlist("priorityType", "")
        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        if(len(priorityType) >0 and not priorityType[0]):
            priorityType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]
        priorityType=[int(i) for i in priorityType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(priorityType)==1):
            priorityType.append(-1)

        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getOpenWorkOrdersDetailReport(date1,date2,assignUser,asset,categoryText,maintenanceType,priorityType))
        tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها
        for i in woList:
            tasks=Tasks.objects.filter(workOrder=i.id)
            tasklist.append(tasks)
        #ادغام دو queryset
        woListDic=zip(woList,tasklist)

        return render(request, 'cmms/reports/simplereports/OpenWorkOrdersDetailReport.html',{'woList':woListDic,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
    def CloseWorkOrdersDetailReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")
        priorityType=request.POST.getlist("priorityType", "")
        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        if(len(priorityType) >0 and not priorityType[0]):
            priorityType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]
        priorityType=[int(i) for i in priorityType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(priorityType)==1):
            priorityType.append(-1)

        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getCloseWorkOrdersDetailReport(date1,date2,assignUser,asset,categoryText,maintenanceType,priorityType))
        tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها
        for i in woList:
            tasks=Tasks.objects.filter(workOrder=i.id)
            tasklist.append(tasks)
        #ادغام دو queryset
        woListDic=zip(woList,tasklist)

        return render(request, 'cmms/reports/simplereports/CloseWorkOrdersDetailReport.html',{'woList':woListDic,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
    def AllWorkOrdersDetailReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")
        priorityType=request.POST.getlist("priorityType", "")
        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        if(len(priorityType) >0 and not priorityType[0]):
            priorityType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]
        priorityType=[int(i) for i in priorityType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(priorityType)==1):
            priorityType.append(-1)

        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getAllWorkOrdersDetailReport(date1,date2,assignUser,asset,categoryText,maintenanceType,priorityType))
        tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها
        for i in woList:
            tasks=Tasks.objects.filter(workOrder=i.id)
            tasklist.append(tasks)
        #ادغام دو queryset
        woListDic=zip(woList,tasklist)
        return render(request, 'cmms/reports/simplereports/AllWorkOrdersDetailReport.html',{'woList':woListDic,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
    def OpenWorkOrdersListReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")
        priorityType=request.POST.getlist("priorityType", "")
        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        if(len(priorityType) >0 and not priorityType[0]):
            priorityType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]
        priorityType=[int(i) for i in priorityType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(priorityType)==1):
            priorityType.append(-1)

        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getOpenWorkOrdersListReport(date1,date2,assignUser,asset,categoryText,maintenanceType,priorityType))
        tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها

        return render(request, 'cmms/reports/simplereports/OpenWorkOrdersListReport.html',{'woList':woList,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
        # html = render_to_string('cmms/reports/simplereports/OpenWorkOrdersListReport.html',
        # {'woList':woList,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = f'filename=order_11.pdf'
        # weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS('cmms/static/css/pdf.css')])
        # return response
    def CloseWorkOrdersListReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")
        priorityType=request.POST.getlist("priorityType", "")
        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        if(len(priorityType) >0 and not priorityType[0]):
            priorityType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]
        priorityType=[int(i) for i in priorityType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(priorityType)==1):
            priorityType.append(-1)

        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getCloseWorkOrdersListReport(date1,date2,assignUser,asset,categoryText,maintenanceType,priorityType))
        tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها

        return render(request, 'cmms/reports/simplereports/CloseWorkOrdersListReport.html',{'woList':woList,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
    def OpenPMWorkOrdersListReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")
        priorityType=request.POST.getlist("priorityType", "")
        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        if(len(priorityType) >0 and not priorityType[0]):
            priorityType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]
        priorityType=[int(i) for i in priorityType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(priorityType)==1):
            priorityType.append(-1)

        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getOpenPMWorkOrdersListReport(date1,date2,assignUser,asset,categoryText,maintenanceType,priorityType))
        tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها

        return render(request, 'cmms/reports/simplereports/OpenPMWorkOrdersListReport.html',{'woList':woList,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
    def OpenWorkOrderGraphReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")

        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]

        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(asset)==1):
            asset.append(-1)


        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getOpenWorkOrderGraphReport(date1,date2,tuple(assignUser),tuple(asset),tuple(categoryText),tuple(maintenanceType)))
        s1,s2=[],[]
        for i in woList:
            s1.append(i.id)
            s2.append(i.name)
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها

        return render(request, 'cmms/reports/simplereports/OpenWorkOrderGraphReport.html',{'wolist':woList,'s1':s1,'s2':s2,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
    def CloseWorkOrderGraphReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        assignUser=request.POST.getlist("assignUser", "")
        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")

        ##### حذف .... در combobox
        if(len(assignUser) >0 and not assignUser[0]):
            assignUser.pop(0)
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        #ساخت لیست
        assignUser=[int(i) for i in assignUser]
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]

        #از بین بردن کامای اضافی ایجاد شده در تاپل
        if(len(assignUser)==1):
            assignUser.append(-1)
        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)


        user1=User.objects.filter(id__in=assignUser).values_list('username', flat=True)
        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getCloseWorkOrderGraphReport(date1,date2,tuple(assignUser),tuple(asset),tuple(categoryText),tuple(maintenanceType)))
        s1,s2=[],[]
        for i in woList:
            s1.append(i.id)
            s2.append(i.name)
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها

        return render(request, 'cmms/reports/simplereports/CloseWorkOrderGraphReport.html',{'wolist':woList,'s1':s1,'s2':s2,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'users':list(user1),'assetcat':list(assetcat),'assets':list(asset1),'maintype':list(maintype),'stdate':startDate,'enddate':endDate})
    def RequestedWorkOrdersListReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")

        asset=request.POST.getlist("Asset", "")
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")
        priorityType=request.POST.getlist("priorityType", "")
        ##### حذف .... در combobox

        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        if(len(priorityType) >0 and not priorityType[0]):
            priorityType.pop(0)
        #ساخت لیست

        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]
        priorityType=[int(i) for i in priorityType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل

        if(len(maintenanceType)==1):
            maintenanceType.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(priorityType)==1):
            priorityType.append(-1)


        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)
        woListDic=[]
        woList=list(WOUtility.getRequestedWorkOrdersListReport(date1,date2,tuple(asset),tuple(categoryText),tuple(maintenanceType),tuple(priorityType)))
        tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها

        return render(request, 'cmms/reports/simplereports/RequestedWorkOrdersListReport.html',{'woList':woList,'tasks':tasklist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'assetcat':list(assetcat),'assets':list(asset1),'priority':priorityType,'maintype':list(maintype),'stdate':startDate,'enddate':endDate})

    def ProjectsReportWithWorkOrderDetails(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        woStatus=request.POST.getlist("woStatus", "")

        if(len(woStatus) >0 and not woStatus[0]):
            woStatus.pop(0)
        woStatus=[int(i) for i in woStatus]
        #از بین بردن کامای اضافی ایجاد شده در تاپل

        if(len(woStatus)==1):
            woStatus.append(-1)

        projList=list(WOUtility.getProjectsReportWithWorkOrderDetails(date1,date2,tuple(woStatus)))
        print("$$$$$$$$",len(projList))
        wolist=[]
         # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها
        for xx in projList:

             wos=WOUtility.getWorkOrderProjectDetails(xx.id)
             wolist.append(wos)
         #ادغام دو queryset
        woListDic=zip(projList,wolist)
        return render(request, 'cmms/reports/simplereports/ProjectsReportWithWorkOrderDetails.html',{'woList':woListDic,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'woStatus':list(woStatus),'stdate':startDate,'enddate':endDate})
    #######################################
    #######################################
    #######################################
    ####### Business Metrics###############
    def FailureCodeCauseCount(self,request):
        #this report include bar graph
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")

        ######asset category###########
        categoryText=request.POST.getlist("categoryText", "")
        if(len(categoryText) >0 and not categoryText[0]):
                categoryText.pop(0)
        categoryText=[int(i) for i in categoryText]
        if(len(categoryText)==1):
                categoryText.append(-1)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        woList=list(WOUtility.getCauseCount(date1,date2,tuple(categoryText)))
        s1,s2=[],[]
        for i in woList:
            s1.append(i.tedad)
            s2.append(i.causeDescription)

        return render(request, 'cmms/reports/simplereports/FailureCodeCauseCount.html',{'wolist':woList,'s1':s1,'s2':s2,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'assetcat':list(assetcat),'stdate':startDate,'enddate':endDate})
    def FailureCodeProblemCount(self,request):
        #this report include bar graph
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")

        ######asset category###########
        categoryText=request.POST.getlist("categoryText", "")
        if(len(categoryText) >0 and not categoryText[0]):
                categoryText.pop(0)
        categoryText=[int(i) for i in categoryText]
        if(len(categoryText)==1):
                categoryText.append(-1)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        woList=list(WOUtility.getProblemCount(date1,date2,tuple(categoryText)))
        s1,s2=[],[]
        for i in woList:
            s1.append(i.tedad)
            s2.append(i.causeDescription)

        return render(request, 'cmms/reports/simplereports/FailureCodeProblemCount.html',{'wolist':woList,'s1':s1,'s2':s2,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'assetcat':list(assetcat),'stdate':startDate,'enddate':endDate})
    def LabourHoursByAsset(self,request):
        #this report include bar graph
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")

        ######asset category###########
        categoryText=request.POST.getlist("categoryText", "")
        maintenanceType=request.POST.getlist("maintenanceType", "")

        if(len(categoryText) >0 and not categoryText[0]):
                categoryText.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        # print("maintenanceType:=>>>>>>>>>>",maintenanceType)

        categoryText=[int(i) for i in categoryText]
        maintenanceType=[int(i) for i in maintenanceType]

        if(len(categoryText)==1):
                categoryText.append(-1)
        if(len(maintenanceType)==0):
            maintenanceType=list(MaintenanceType.objects.all().values_list('id',flat=True))
            maintype=MaintenanceType.objects.all().values_list('name', flat=True)
            #maintenanceType.append(-1)
        else:
            #پیدا کردن اسم
            maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)

        #پیدا کردن اسم
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        woList=list(AssetUtility.getLabourHoursByAsset(date1,date2,tuple(categoryText),','.join([str(elem) for elem in maintenanceType]) ))

        return render(request, 'cmms/reports/simplereports/LabourHoursByAsset.html',{'wolist':woList,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'assetcat':list(assetcat),'maintype':list(maintype),'date1':startDate,'date2':endDate})
    def LabourHoursByAssetTop10(self,request):
       #this report include bar graph
       date1=DateJob.getDate2(request.POST.get("startDate",""))
       date2=DateJob.getDate2(request.POST.get("endDate",""))
       startDate=request.POST.get("startDate","").replace('-','/')
       endDate=request.POST.get("endDate","").replace('-','/')

       ######asset category###########
       categoryText=request.POST.getlist("categoryText", "")
       maintenanceType=request.POST.getlist("maintenanceType", "")

       if(len(categoryText) >0 and not categoryText[0]):
               categoryText.pop(0)
       if(len(maintenanceType) >0 and not maintenanceType[0]):
           maintenanceType.pop(0)
       # print("maintenanceType:=>>>>>>>>>>",maintenanceType)

       categoryText=[int(i) for i in categoryText]
       maintenanceType=[int(i) for i in maintenanceType]

       if(len(categoryText)==1):
               categoryText.append(-1)
       if(len(maintenanceType)==0):
           maintenanceType=list(MaintenanceType.objects.all().values_list('id',flat=True))
           maintype=MaintenanceType.objects.all().values_list('name', flat=True)
           #maintenanceType.append(-1)
       else:
           #پیدا کردن اسم
           maintype=MaintenanceType.objects.filter(id__in=maintenanceType).values_list('name', flat=True)

       #پیدا کردن اسم
       assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
       woList=list(AssetUtility.getLabourHoursByAssetTop10(date1,date2,tuple(categoryText),','.join([str(elem) for elem in maintenanceType]) ))
       s1,s2=[],[]
       for i in woList:
           if(i.timespent):
               s1.append(i.timespent)
           else:
               s1.append(0)
           s2.append(i.assetName)

       return render(request, 'cmms/reports/simplereports/LabourHoursByAssetTop10.html',{'wolist':woList,'s1':s1,'s2':s2,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'assetcat':list(assetcat),'maintype':list(maintype),'date1':startDate,'date2':endDate})
    ################################
    def WorkOrderCostListReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        asset=request.POST.getlist("parentAsset", "")
        categoryText=request.POST.getlist("categoryText", "")

        ##### حذف .... در combobox

        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)

        #ساخت لیست
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        #از بین بردن کامای اضافی ایجاد شده در تاپل

        if(len(asset)==1):
            asset.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)



        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        # woListDic=[]
        woList=list(WOUtility.getWorkOrderCostListReport(date1,date2,tuple(asset),tuple(categoryText)))
        # tasklist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها
        # for i in woList:
        #     tasks=Tasks.objects.filter(workOrder=i.id)
        #     tasklist.append(tasks)
        # #ادغام دو queryset
        # woListDic=zip(woList,tasklist)

        return render(request, 'cmms/reports/simplereports/WorkOrderCostListReport.html',{'woList':woList,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'assetcat':list(assetcat),'assets':list(asset1),'stdate':startDate,'enddate':endDate})
    ################################
    def  WorkOrderCostDetailReport(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        asset=request.POST.getlist("parentAsset", "")
        categoryText=request.POST.getlist("categoryText", "")

        ##### حذف .... در combobox

        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)

        #ساخت لیست
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        #از بین بردن کامای اضافی ایجاد شده در تاپل

        if(len(asset)==1):
            asset.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)

        asset1=Asset.objects.filter(id__in=asset).values_list('assetName', flat=True)
        assetcat=AssetCategory.objects.filter(id__in=categoryText).values_list('name', flat=True)
        assetList=[]
        if(len(asset)==0):
            if(len(categoryText)==0):
                assetList=Asset.objects.all()
            else:
                assetList=Asset.objects.filter(assetCategory__in=categoryText)

        else:
            if(len(categoryText)==0):
                assetList=Asset.objects.filter(id__in=asset)
            else:
                 assetList=Asset.objects.filter(id__in=asset).filter(assetCategory__in=categoryText)

        # woListDic=[]

        AssetList=list(assetList)
        wolist=[]
        # پیدا کردن لیستی از تسکهای مرتبز با دستورکارها
        for i in AssetList:
             wos=WOUtility.getWorkOrderCostDetailReport(date1,date2,i.id)
             wolist.append(wos)
        # #ادغام دو queryset
        woListDic=zip(AssetList,wolist)

        return render(request, 'cmms/reports/simplereports/WorkOrderCostDetailReport.html',{'woList':woListDic,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'assetcat':list(assetcat),'assets':list(asset1),'stdate':startDate,'enddate':endDate})
    def WorkOrderHoursLoggedbyTechnician(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        userLink=request.POST.get("userLink", "")
        user=SysUser.objects.get(id=userLink)
        n1=UserUtility.getOveralView(userLink,date1,date2)
        n2=UserUtility.getDetailWoView(userLink,date1,date2)
        return render(request, 'cmms/reports/simplereports/WorkOrderHoursLoggedbyTechnician.html',{'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'n1':list(n1),'n2':list(n2),'stdate':startDate,'enddate':endDate,'user':user.fullName})

    def UpcommingScheduledMaintenanceList(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","")
        endDate=request.POST.get("endDate","")
        asset=request.POST.getlist("parentAsset", "")
        categoryText=request.POST.getlist("categoryText", "")
        userLink=request.POST.get("assignUser", "")
        maintenanceType=request.POST.get("maintenanceType", "")

        ##### حذف .... در combobox

        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(categoryText) >0 and not categoryText[0]):
            categoryText.pop(0)
        if(len(userLink) >0 and not userLink[0]):
            userLink.pop(0)
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)

        #ساخت لیست
        asset=[int(i) for i in asset]
        categoryText=[int(i) for i in categoryText]
        userLink=[int(i) for i in userLink]
        maintenanceType=[int(i) for i in maintenanceType]
        #از بین بردن کامای اضافی ایجاد شده در تاپل

        if(len(asset)==1):
            asset.append(-1)
        if(len(categoryText)==1):
            categoryText.append(-1)
        if(len(userLink)==1):
            userLink.append(-1)
        up_wos=ScheduleUtility.GenerateUpcommingWo(date1,date2,asset,categoryText,userLink,maintenanceType)
        return render(request, 'cmms/reports/simplereports/UpcommingScheduledMaintenanceList.html',{'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate,'wos':up_wos})
    def SiteAssetSMSummaryReport(self,request):
        asset=request.POST.getlist("asset", "")
        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        asset=[int(i) for i in asset]


        assets=[]
        if(len(asset)>0):
            assets=Asset.objects.filter(id__in=asset)
        else:
            assets=Asset.objects.filter(assetTypes=1)
        print(assets)
        up_wos=SWOUtility.getAssetSMSummaryReport(asset)
        print(up_wos)
        return render(request, 'cmms/reports/simplereports/SiteAssetSMSummaryReport.html',{'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'asset':assets,'wos':up_wos})
    def UpcomingScheduledMaintenanceWithStockForecasting(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))

        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        maintenanceType=request.POST.getlist("maintenanceType", "")
        if(len(maintenanceType) >0 and not maintenanceType[0]):
            maintenanceType.pop(0)
        maintenanceType=[int(i) for i in maintenanceType]
        wos=ScheduleUtility.GenerateUpcommingWo2(date1,date2,maintenanceType)
        partlist=[]
        for c in wos:
            parts=WorkorderPart.objects.filter(woPartWorkorder=c).select_related('woPartStock')
            partlist.append(parts)
        wolist=zip(wos,partlist)
        return render(request, 'cmms/reports/simplereports/UpcomingScheduledMaintenanceWithStockForecasting.html',{'woList':wolist,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'maintype':list(maintenanceType),'stdate':startDate,'enddate':endDate})
    def ListOfOfflineAssets(self,request):
        asset=request.POST.getlist("location", "")
        category=request.POST.getlist("category", "")


        ##### حذف .... در combobox

        if(len(asset) >0 and not asset[0]):
            asset.pop(0)
        if(len(category) >0 and not category[0]):
            category.pop(0)


        #ساخت لیست
        asset=[int(i) for i in asset]
        category=[int(i) for i in category]

        #از بین بردن کامای اضافی ایجاد شده در تاپل

        if(len(asset)==1):
            asset.append(-1)
        if(len(category)==1):
            category.append(-1)

        wos=[]
        if(len(category)>0):
            darayees=Asset.objects.filter(assetStatus=False,assetCategory__in=category)
            for d in darayees:
                k=AssetLife.objects.filter(assetLifeAssetid__assetStatus=False,assetLifeAssetid=d).order_by('-assetOfflineFrom','-assetOfflineFromTime')
                if(len(k)>0):
                    wos.append(list(k)[0])

            # wos=AssetLife.objects.filter(assetLifeAssetid__assetStatus=False,assetLifeAssetid__assetCategory__in=category).order_by('-assetOfflineFrom','-assetOfflineFromTime')
        elif(len(asset)>0):
            for d in asset:
                k=AssetLife.objects.filter(assetLifeAssetid__assetStatus=False,assetLifeAssetid=d).order_by('-assetOfflineFrom','-assetOfflineFromTime')
                if(len(k)>0):
                    wos.append(list(k)[0])

            # wos=AssetLife.objects.filter(assetLifeAssetid__id__in=asset,assetLifeAssetid__assetStatus=False).order_by('-assetOfflineFrom','-assetOfflineFromTime')
        else:
            # # print(AssetLife.objects.filter(assetLifeAssetid__assetStatus=False).query)
            # wos=AssetLife.objects.filter(assetLifeAssetid__assetStatus=False).order_by('-assetOfflineFrom','-assetOfflineFromTime')
            darayees=Asset.objects.filter(assetStatus=False)
            for d in darayees:
                k=AssetLife.objects.filter(assetLifeAssetid__assetStatus=False,assetLifeAssetid=d).order_by('-assetOfflineFrom','-assetOfflineFromTime')
                if(len(k)>0):
                    wos.append(list(k)[0])
        return render(request, 'cmms/reports/simplereports/ListOfOfflineAssets.html',{'woList':wos,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S")})
    def AssetOnlineAndOfflineHistory(self,request):
                date1=DateJob.getDate2(request.POST.get("startDate",""))
                date2=DateJob.getDate2(request.POST.get("endDate",""))
                startDate=request.POST.get("startDate","").replace('-','/')
                endDate=request.POST.get("endDate","").replace('-','/')
                asset=request.POST.getlist("location", "")
                category=request.POST.getlist("category", "")
                offlinecode=request.POST.getlist("offlinecode", "")



                ##### حذف .... در combobox

                if(len(asset) >0 and not asset[0]):
                    asset.pop(0)
                if(len(category) >0 and not category[0]):
                    category.pop(0)
                if(len(offlinecode) >0 and not offlinecode[0]):
                    offlinecode.pop(0)


                #ساخت لیست
                asset=[int(i) for i in asset]
                category=[int(i) for i in category]
                offlinecode=[int(i) for i in offlinecode]

                #از بین بردن کامای اضافی ایجاد شده در تاپل

                if(len(asset)==1):
                    asset.append(-1)
                if(len(category)==1):
                    category.append(-1)

                if(len(offlinecode)==0):
                    offlinecode=StopCode.objects.all().values_list('id',flat=True)
                wos=[]
                assets=[]
                # wos=AssetUtility.getAssetOfflineHistory(category,asset,offlinecode,date1,date2)
                if(len(category)>0):
                    assets=Asset.objects.filter(id__in=AssetLife.objects.filter(assetLifeAssetid__assetCategory__in=category,assetOfflineFrom__range=(date1,date2)).values_list('assetLifeAssetid',flat=True).distinct())
                    # print(Asset.objects.filter(id__in=AssetLife.objects.filter(assetLifeAssetid__assetCategory__in=category).values_list('assetLifeAssetid',flat=True)).query)
                elif(len(asset)>0):
                    assets=Asset.objects.filter(id__in=AssetLife.objects.filter(assetLifeAssetid__id__in=asset,assetOfflineFrom__range=(date1,date2)).values_list('assetLifeAssetid',flat=True).distinct())
                else:
                    assets=Asset.objects.filter(id__in=AssetLife.objects.filter(assetOfflineFrom__range=(date1,date2)).values_list('assetLifeAssetid',flat=True).distinct())
                assetList=[]
                time_sum=0
                for i in assets:
                    al=AssetUtility.getAssetOfflineHistory(i,offlinecode,date1,date2)
                    assetList.append(al)
                    for k in al:
                        time_sum=time_sum+k.getAffectedHour_digits()
                #ادغام دو queryset
                woListDic=zip(assets,assetList)
                offlinecodelist=StopCode.objects.filter(id__in=offlinecode)
                assetcatnames=AssetCategory.objects.filter(id__in=category).values_list('name',flat=True)
                stopnames=StopCode.objects.filter(id__in=offlinecode).values_list('stopDescription',flat=True)
                return render(request, 'cmms/reports/simplereports/AssetOnlineAndOfflineHistory.html',{'woList':woListDic,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'asset':list(assets),'problemcode':list(stopnames),'assetcat':list(assetcatnames),'stdate':startDate,'enddate':endDate,'sum':time_sum})
    def PartsReceivedIntoInventory(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        wos=PartPurchase.objects.filter(purchaseDateRecieved__range=[date1,date2])
        return render(request, 'cmms/reports/simplereports/PartsReceivedIntoInventory.html',{'woList':wos,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate})
    def InventoryPurchaseTransactionsBetween2Dates(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        parts=Part.objects.filter(id__in=PartPurchase.objects.filter(purchaseDateRecieved__range=[date1,date2]).values('purchasePartId'))
        stocks=Stock.objects.filter(stockItem__in=parts)
        # wos=PartPurchase.objects.filter(purchaseDateRecieved__range=[date1,date2])
        wos=[]
        for c in stocks:
            ts=PartPurchase.objects.filter(purchasePartId=c.stockItem,purchaseStock=c.location,purchaseDateRecieved__range=[date1,date2])
            wos.append(ts)
        woListDic=zip(stocks,wos)
        return render(request, 'cmms/reports/simplereports/InventoryPurchaseTransactionsBetween2Dates.html',{'woList':woListDic,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate})
    def ListOfLowStockInventoryFilteredByLocation(self,request):
        location=request.POST.getlist("location", "")
        wos=[]
        if(len(location) >0 and not location[0]):
            location.pop(0)
        #ساخت لیست
        location=[int(i) for i in location]
        if(len(location)==1):
            location.append(-1)
        if(len(location)>0):
            wos=Stock.objects.filter(location__in=location,qtyOnHand__lt=F('minQty'))
        else:
            wos=Stock.objects.filter(qtyOnHand__lt=F('minQty'))
        return render(request, 'cmms/reports/simplereports/ListOfLowStockInventoryFilteredByLocation.html',{'woList':wos,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'location':location})
    def UserGroupPerformance(self,request):
            location=request.POST.getlist("location", "")
            date1=DateJob.getDate2(request.POST.get("startDate",""))
            date2=DateJob.getDate2(request.POST.get("endDate",""))
            startDate=request.POST.get("startDate","").replace('-','/')
            endDate=request.POST.get("endDate","").replace('-','/')
            mtype=request.POST.getlist("maintenanceType", "")
            ugroup=request.POST.getlist("usergroup", "")
            wos=[]
            print("######",len(ugroup))
            if(len(location) >0 and not location[0]):
                location.pop(0)
            if(len(mtype) >0 and not mtype[0]):
                mtype.pop(0)
            if(len(ugroup) >0 and not ugroup[0]):
                print("$$$$$$$$$$$$$$$$$$$$$$")
                ugroup.pop(0)
            #ساخت لیست
            location=[int(i) for i in location]
            if(len(location)==0):
                location.append(-1)
            mtype=[int(i) for i in mtype]
            if(len(mtype)==0):
                mtype.append(-1)
            ugroup=[int(i) for i in ugroup]
            if(len(ugroup)==0):
                ugroup.append(-1)
            unitmember={}


            if((ugroup[0]==-1)):
                ugroup=UserGroup.objects.values_list('id', flat=True)
            if((mtype[0]==-1)):
                mtype=MaintenanceType.objects.values_list('id', flat=True)
            if(location[0]==-1):
                location=Asset.objects.values_list('id',flat=True)
            print(ugroup,"$$$$$$$$$$$$$$$")
            maint=[]
            for x in ugroup:



                unitmember[x]=UserGroup.objects.raw("select get_get_unint_member_count({0}) as id".format(x))
                ma=[]
                ma.append(unitmember[x][0].id)
                unitname=UserGroup.objects.get(id=x)
                ma.append(unitname.userGroupName)
                data={}
                data["member"]=unitmember[x][0].id
                data["unitname"]=unitname.userGroupName


                data["hozur"]=UserGroup.objects.raw("select get_unint_member_attendance({0},'{1}','{2}') as id".format(x,date1,date2))[0].id
                maxhozur=Attendance.objects.raw("""select attendance.name_id as id,sum(attendance.attendanceTime) as t1 from attendance inner join usergroups on usergroups.userUserGroups_id=attendance.name_id inner join usergroup on usergroup.id=usergroups.groupUserGroups_id
                                                    where usergroup.id ={0} and datecreated between '{1}' and '{2}'
                                                    GROUP by attendance.name_id order by(t1) desc """.format(x,date1,date2))

                if(len(list(maxhozur))>0):
                    data["maxhozurH"]=maxhozur[0].t1
                    data["maxhozurP"]=SysUser.objects.get(id=maxhozur[0].id).fullName
                else:
                    data["maxhozurH"]=0
                    data["maxhozurP"]="-"

                zaribhozur=25*8
                data["nafarsaathozur"]=data["hozur"]/zaribhozur
                for m in mtype:
                    zarib=UserGroupMaintenanceZarib.objects.filter(groupUGMZ=x,maintenanceTypeUGMZ=m)
                    if(zarib):

                        # print("select get_maintenance_time_usergroup({0},{1},'{2}','{3}',{4})".format(x,m,date1,date2,location[0]))
                        # print("$$$$$$$$$$$$$$$$$$$$$$")
                        mres=WorkOrder.objects.raw("select get_maintenance_time_usergroup({0},{1},'{2}','{3}',{4}) as id".format(x,m,date1,date2,location[0]))
                        mname=MaintenanceType.objects.get(id=m).name
                        data["{}".format(mname)]=mres[0].id
                        # ma.append(mres[0].id)
                        # print("################")
                        # print(UserGroupMaintenanceZarib.objects.filter(groupUGMZ=x,maintenanceTypeUGMZ=m).query)


                        # ma.append(mres[0].id/zarib[0].zaribUGMZ)
                        data["{0}_{1}".format("نفر_ساعت",mname)]="{:.2f}".format(mres[0].id/zarib[0].zaribUGMZ)

                        print(zarib[0].zaribUGMZ)



                maint.append(data)



            return render(request, 'cmms/reports/simplereports/ListOfLowStockInventoryFilteredByLocation.html',{'woList':maint,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'location':location,'stdate':startDate,'enddate':endDate})
    def IstgahReport(self,request):
            location=request.POST.getlist("location", "")
            date1=DateJob.getDate2(request.POST.get("startDate",""))
            date2=DateJob.getDate2(request.POST.get("endDate",""))
            startDate=request.POST.get("startDate","").replace('-','/')
            endDate=request.POST.get("endDate","").replace('-','/')
            mtype=request.POST.get("maintenanceType", "")
            ugroup=request.POST.getlist("usergroup", "")
            assetCategory=request.POST.getlist("assetCategory", "")
            wos=[]

            if(len(location) >0 and not location[0]):
                location.pop(0)
            if(len(assetCategory) >0 and not assetCategory[0]):
                assetCategory.pop(0)
            # if(len(mtype) >0 and not mtype[0]):
            #     mtype.pop(0)
            if(len(ugroup) >0 and not ugroup[0]):
                print("$$$$$$$$$$$$$$$$$$$$$$")
                ugroup.pop(0)
            #ساخت لیست
            location=[int(i) for i in location]
            if(len(location)==0):
                location.append(-1)
            assetCategory=[int(i) for i in assetCategory]
            if(len(assetCategory)==0):
                assetCategory.append(-1)
            # mtype=[int(i) for i in mtype]
            # if(len(mtype)==0):
            #     mtype.append(-1)
            ugroup=[int(i) for i in ugroup]
            if(len(ugroup)==0):
                ugroup.append(-1)
            unitmember={}


            if((ugroup[0]==-1)):
                ugroup=UserGroup.objects.values_list('id', flat=True)
            if((assetCategory[0]==-1)):
                assetCategory=AssetCategory.objects.values_list('id', flat=True)
            if((mtype[0]==-1)):
                mtype=MaintenanceType.objects.values_list('id', flat=True)
            if(location[0]==-1):
                location=Asset.objects.values_list('id',flat=True)
            print(ugroup,"$$$$$$$$$$$$$$$")
            maint=[]
            mname=MaintenanceType.objects.get(id=mtype).name
            for x in ugroup:




                ma=[]
                mc=[]

                unitname=UserGroup.objects.get(id=x)
                ma.append(unitname.userGroupName)
                mc.append(unitname.userGroupName)
                data={}
                data["member"]=unitname.userGroupName
                data["unitname"]=unitname.userGroupName
                row1=[]

                # //ساخت سطرهای گزارش
                row1.append("نام واحد")
                for a1 in assetCategory:
                    assetCategoryName=AssetCategory.objects.get(id=a1).name

                    row1.append("{0}-{1}".format(mname,assetCategoryName))

                # سطرهای اضافی خواجه زاده
                row1.append("مجموع")
                row1.append("درصد بیشترین")
                row1.append("بدون توقف تولید")
                row1.append("گزارشات EM")

                totalCount=0
                totalTime=0.0
                maxtime=0.0
                maxCount=0
                noneStopCount=0
                noneStopTime=0.0
                for a1 in assetCategory:
                    assetCategoryName=AssetCategory.objects.get(id=a1).name
                    # print("select get_maintenance_time_usergroup({0},{1},'{2}','{3}',{4})".format(x,m,date1,date2,location[0]))
                    # print("$$$$$$$$$$$$$$$$$$$$$$")
                    mres=WorkOrder.objects.raw("select get_maintenance_time_station({0},{1},'{2}','{3}',{4},{5}) as id".format(x,mtype,date1,date2,location[0],a1))
                    mres[0].id= '{0:02.0f}:{1:02.0f}'.format(*divmod(mres[0].id * 60, 60))
                    if(maxtime<mres[0].id):
                        maxtime=mres[0].id

                    totalTime=totalTime+mres[0].id
                    ma.append(mres[0].id)
                    mcount=WorkOrder.objects.raw("select get_maintenance_time_station_count({0},{1},'{2}','{3}',{4},{5}) as id".format(x,mtype,date1,date2,location[0],a1))
                    # mcount[0].id= '{0:02.0f}:{1:02.0f}'.format(*divmod(mcount[0].id*60, 60))
                    ncount=WorkOrder.objects.raw("select get_maintenance_count_station_nonestop({0},{1},'{2}','{3}',{4},{5}) as id".format(x,mtype,date1,date2,location[0],a1))
                    # ncount[0].id= '{0:02.0f}:{1:02.0f}'.format(*divmod(ncount[0].id*60, 60))
                    noneStopCount=noneStopCount+ncount[0].id
                    nTime=WorkOrder.objects.raw("select get_maintenance_time_station_nonestop({0},{1},'{2}','{3}',{4},{5}) as id".format(x,mtype,date1,date2,location[0],a1))
                    nTime[0].id= '{0:02.0f}:{1:02.0f}'.format(*divmod(nTime[0].id*60, 60))
                    noneStopTime=noneStopTime+nTime[0].id
                        # ma.append(mres[0].id)
                        # print("################")
                        # print(UserGroupMaintenanceZarib.objects.filter(groupUGMZ=x,maintenanceTypeUGMZ=m).query)
                    if(maxCount<mcount[0].id):
                        maxCount=mcount[0].id

                    mc.append(mcount[0].id)
                    totalCount=totalCount+mcount[0].id

                        # ma.append(mres[0].id/zarib[0].zaribUGMZ)
                        # data["{0}_{1}".format("نفر_ساعت",mname)]="{:.2f}".format(mres[0].id/zarib[0].zaribUGMZ)

                        # print(zarib[0].zaribUGMZ)

                ma.append(float("{:.2f}".format(totalTime)))
                mc.append(float("{:.2f}".format(totalCount)))

                if(totalTime==0):
                    ma.append(0)
                else:
                    ma.append(float("{:.2f}".format(maxtime/totalTime)))
                if(totalCount==0):
                    mc.append(0)
                else:
                    mc.append(float("{:.2f}".format(maxCount/totalCount)))
                ma.append(float("{:.2f}".format(noneStopTime)))
                mc.append(noneStopCount)
                # گزارشات EM
                emres=WorkOrder.objects.raw("select get_maintenance_time_station_EM({0},{1},'{2}','{3}',{4}) as id".format(x,mtype,date1,date2,location[0]))
                emres[0].id= '{0:02.0f}:{1:02.0f}'.format(*divmod(emres[0].id*60, 60))
                emcountres=WorkOrder.objects.raw("select get_maintenance_time_station_count_EM({0},{1},'{2}','{3}',{4}) as id".format(x,mtype,date1,date2,location[0]))
                ma.append(emres[0].id)
                mc.append(emcountres[0].id)


                maint.append(zip(ma,mc))



            return render(request, 'cmms/reports/simplereports/ListofStationMaintenance.html',{'row1':row1,'woList':maint,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'location':location,'stdate':startDate,'enddate':endDate,'mtype':mname})
    def Amalkard3MaheReport(self,request):

            location=request.POST.get('location','')
            SType=request.POST.get('SType','')
            ugroup=request.POST.getlist("usergroup", "")



            if(len(ugroup) >0 and not ugroup[0]):
                ugroup.pop(0)

            ugroup=[int(i) for i in ugroup]
            if(len(ugroup)==0):
                ugroup.append(-1)
            if(ugroup[0]==-1):
                 ugroup=UserGroup.objects.values_list('id', flat=True).exclude(userGroupCode='other')
            ###get maintenanceType
            mtype=MaintenanceType.objects.all().exclude(id=1)
            dtset=DateJob.getQDate(int(SType))#return a range
            print(dtset)
            javabMain=dict()
            hoz=dict()

            # javabMain=dict()
            for g in ugroup:
                javab={}
                hozur=[]
                for m in mtype:
                        javab[m.name]=[]
                for d in dtset:

                    ff=[]
                    dt=DateJob.findQDate(d)
                    print(dt)
                    hozur.append(WorkOrder.objects.raw("select get_group_hozur({0},'{1}','{2}') as id".format(g,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1])))[0].id)



                    for m in mtype:
                            # print('select get_group_workorder_time_by_maintype({0},{1},"{2}","{3}",{4}) as id'.format(4,m.id,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1]),location))
                            # print("$$",WorkOrder.objects.raw('select get_group_workorder_time_by_maintype({0},{1},"{2}","{3}",{4}) as id'.format(4,m.id,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1]),location))[0].id)
                            javab[m.name].append(WorkOrder.objects.raw("select get_group_workorder_time_by_maintype({0},{1},'{2}','{3}',{4}) as id".format(g,m.id,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1]),location))[0].id)
                javab['hozur']=hozur
                javabMain[g]=javab
                # hoz[g]=hozur
            # kk=zip(javabMain,hoz)
            td={}
            usr=UserGroup.objects.all().exclude(userGroupCode='other')
            for i in usr:
                td[i.id]=i.userGroupName







            x=[1,2,3,4]
            return render(request, 'cmms/reports/simplereports/Amalkard3MaheReport.html',{'test':x,'javab':javabMain,'dtset':[(str(i[0])+i[1]) for i in dtset],'hozur':hoz,'usr':td,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S")})
    def TahlilOfflineStatus(self,request):
        location=request.POST.get('location','')
        SType=request.POST.get('SType','')
        causeCode=request.POST.getlist("causeCode", "")
        if(len(causeCode) >0 and not causeCode[0]):
            causeCode.pop(0)

        causeCode=[int(i) for i in causeCode]
        if(len(causeCode)==0):
            causeCode.append(-1)
        if(causeCode[0]==-1):
             causeCode=OfflineStatus.objects.values_list('id', flat=True)


        dtset=DateJob.getQDateM(int(SType))#return a range
        # print(causeCode,"$$$$")
        mainJavab={}
        label1=CauseCode.objects.filter(id__in=causeCode).values_list('causeDescription',flat=True)
        label=[]
        label2=[]
        loc=Asset.objects.get(id=location)
        for x in label1:
            label.append(x)
        for x in causeCode:
            label2.append(x)
        for d in dtset:
            javab={}
            dt=DateJob.findQDateM(d)

            for x in causeCode:

                javab[x]=AssetLife.objects.raw("""select count(assetlife.id) as id from assetlife
                inner join assets on assets.id= assetlife.assetLifeAssetid_id
                left join workorder on workorder.id=assetlife.assetWOAssoc_id
                where 	(assets.id={0} or assets.assetIsLocatedAt_id={0})
                and assetlife.assetOfflineFrom between '{1}' and '{2}' and
                 workorder.woCauseCode_id={3} """.format(location,DateJob.getDate2(dt[0]),
                 DateJob.getDate2(dt[1]),x))[0].id
            mainJavab["{0}-{1}".format(d[0],d[1])]=javab



        return render(request, 'cmms/reports/simplereports/TahlilOfflineStatus.html',{'javab':mainJavab,'location':loc,'label':label,'causeCode':label2,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S")})
    def ShakhesTamirat(self,request):
        usergroup=request.POST.get('usergroup','')
        SType=request.POST.get('SType','')
        dtset=DateJob.getQDateM(int(SType))#return a range
        mainJavab={}

        for d in dtset:
            javab={}
            dt=DateJob.findQDateM(d)
            # if(d[1] =="فروردین"):
            #     print(d[1] )
            # print(DateJob.getDate2(dt[0]),
            # DateJob.getDate2(dt[1]))



            javab['تعداد تعمیر']=int(WorkOrder.objects.raw("""select count(workorder.id) as id from workorder
            inner join usergroups on workorder.assignedToUser_id= usergroups.userUserGroups_id
            inner join usergroup on usergroups.groupusergroups_id=usergroup.id
            inner join maintenancetype on workorder.maintenancetype_id=maintenancetype.id
            where usergroup.id={0}
            and workorder.datecreated between '{1}' and '{2}' and
             MaintenanceType.name='تعمیر' and workorder.isScheduling=0 """.format(usergroup,DateJob.getDate2(dt[0]),
            DateJob.getDate2(dt[1])))[0].id)


            javab['EM']=int(Tasks.objects.raw(""" select COALESCE( sum(timestampdiff(minute,cast(concat(taskStartDate, ' ', taskStartTime) as datetime)
                                                ,cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0) as id from tasks

                                                                 inner join usergroups on tasks.taskAssignedToUser_id=usergroups.userUserGroups_id
                                                                 inner join usergroup on usergroups.groupUserGroups_id=usergroup.id
                                                                 inner JOIN workorder on tasks.workOrder_id=workorder.id
                                                                 inner join maintenancetype on workorder.maintenancetype_id=maintenancetype.id
                                                                 where maintenancetype.name='تعمیر' and usergroup.id={0}
                                                                 and tasks.taskDateCompleted between '{1}' and '{2}'
                                                                 and workorder.isScheduling=0 and isem=1
                                                                """.format(usergroup,DateJob.getDate2(dt[0]),
                                                                DateJob.getDate2(dt[1])))[0].id)/60

            javab['کل تعمیرات']=int(Tasks.objects.raw(""" select COALESCE( sum(timestampdiff(minute,cast(concat(taskStartDate, ' ', taskStartTime) as datetime)
                                                ,cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0) as id from tasks

                                                                 inner join usergroups on tasks.taskAssignedToUser_id=usergroups.userUserGroups_id
                                                                 inner join usergroup on usergroups.groupUserGroups_id=usergroup.id
                                                                 inner JOIN workorder on tasks.workOrder_id=workorder.id
                                                                 inner join maintenancetype on workorder.maintenancetype_id=maintenancetype.id
                                                                 where maintenancetype.name='تعمیر' and usergroup.id={0}
                                                                 and tasks.taskDateCompleted between '{1}' and '{2}'
                                                                 and workorder.isScheduling=0
                                                                """.format(usergroup,DateJob.getDate2(dt[0]),
                                                                DateJob.getDate2(dt[1])))[0].id)/60
            javab['بدون توقف تولید']=int(Tasks.objects.raw(""" select COALESCE( sum(timestampdiff(minute,cast(concat(taskStartDate, ' ', taskStartTime) as datetime)
                                                ,cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0) as id from tasks

                                                                 inner join usergroups on tasks.taskAssignedToUser_id=usergroups.userUserGroups_id
                                                                 inner join usergroup on usergroups.groupUserGroups_id=usergroup.id
                                                                 inner JOIN workorder on tasks.workOrder_id=workorder.id
                                                                 inner join maintenancetype on workorder.maintenancetype_id=maintenancetype.id
                                                                 left join stopcode on workorder.woStopCode_id=stopcode.id
                                                                 where maintenancetype.name='تعمیر' and usergroup.id={0}
                                                                 and tasks.taskDateCompleted between '{1}' and '{2}'
                                                                 and workorder.isScheduling=0 and (workorder.woStopCode_id is null or stopcode.stopcode='nostop')
                                                                """.format(usergroup,DateJob.getDate2(dt[0]),
                                                                DateJob.getDate2(dt[1])))[0].id)/60






            mainJavab["{0}-{1}".format(d[0],d[1])]=javab
            group=UserGroup.objects.get(id=usergroup).userGroupName
        return render(request, 'cmms/reports/simplereports/ShakhesTamirat.html',{'group':group,'javab':mainJavab,'dtset':[(str(i[0])+i[1]) for i in dtset],'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S")})
    def UserGroupPerformanceWithGraph(self,request):
            location=request.POST.getlist("location", "")
            lbls=[]

            mtype=request.POST.getlist("maintenanceType", "")
            ugroup=request.POST.getlist("usergroup", "")
            wos=[]

            SType=request.POST.get('SType','')
            dtset=DateJob.getQDateM(int(SType))#return a range
            mainJavab={}


            if(len(location) >0 and not location[0]):
                location.pop(0)
            if(len(mtype) >0 and not mtype[0]):
                mtype.pop(0)
            if(len(ugroup) >0 and not ugroup[0]):
                # print("$$$$$$$$$$$$$$$$$$$$$$")
                ugroup.pop(0)
            #ساخت لیست
            location=[int(i) for i in location]
            if(len(location)==0):
                location.append(-1)
            mtype=[int(i) for i in mtype]
            if(len(mtype)==0):
                mtype.append(-1)
            ugroup=[int(i) for i in ugroup]
            if(len(ugroup)==0):
                ugroup.append(-1)
            unitmember={}


            if((ugroup[0]==-1)):
                ugroup=UserGroup.objects.values_list('id', flat=True).exclude(userGroupCode='other')
            if((mtype[0]==-1)):
                mtype=MaintenanceType.objects.values_list('id', flat=True).exclude(id=1)
            if(location[0]==-1):
                location=Asset.objects.values_list('id',flat=True)
            # print(ugroup,"$$$$$$$$$$$$$$$")
            maint=[]
            mtype2=MaintenanceType.objects.filter(id__in=mtype).exclude(id=1)
            ug=UserGroup.objects.filter(id__in=ugroup)


            for x in ug:
                javab={}
                hozur=[]
                # for m in mtype2:
                #          javab[m.name]=[]
                for d in dtset:
                    dt=DateJob.findQDateM(d)




                    # cc=UserGroup.objects.raw("select get_get_unint_member_count({0}) as id".format(x.id))[0].id
                    cc=UserGroup.objects.raw("select get_unint_member_count({0},'{1}','{2}') as id".format(x.id,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1])))[0].id

                    # ma=[]
                    # ma.append(javab['memeber_count'])
                    unitname=UserGroup.objects.get(id=x.id)
                    # ma.append(unitname.userGroupName)
                    data={}
                    data["member"]=cc
                    data["unitname"]=unitname.userGroupName


                    dhozu=UserGroup.objects.raw("select get_unint_member_attendance({0},'{1}','{2}') as id".format(x.id,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1])))[0].id
                    maxhozur=Attendance.objects.raw("""select attendance.name_id as id,sum(attendance.attendanceTime) as t1 from attendance inner join usergroups on usergroups.userUserGroups_id=attendance.name_id inner join usergroup on usergroup.id=usergroups.groupUserGroups_id
                                                        where usergroup.id ={0} and datecreated between '{1}' and '{2}'
                                                        GROUP by attendance.name_id order by(t1) desc """.format(x.id,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1])))

                    if(len(list(maxhozur))>0):
                        data["maxhozurH"]=maxhozur[0].t1
                        data["maxhozurP"]=SysUser.objects.get(id=maxhozur[0].id).fullName
                    else:
                        data["maxhozurH"]=0
                        data["maxhozurP"]="-"

                    zaribhozur=25*8
                    data_hozur=0;
                    if(dhozu):
                        data_hozur=dhozu
                        data["حضور"]=dhozu
                    else:
                         data_hozur=0
                         data["حضور"]=0
                    if(not "نفرساعت حضور" in lbls):
                                lbls.append("نفرساعت حضور")
                    # if(not "member" in lbls):
                    #             lbls.append("memebr")


                    data["نفرساعت حضور"]=data_hozur/zaribhozur
                    for m in mtype:
                        zarib=UserGroupMaintenanceZarib.objects.filter(groupUGMZ=x.id,maintenanceTypeUGMZ=m)
                        if(zarib):
                            mres=WorkOrder.objects.raw("select get_maintenance_time_usergroup({0},{1},'{2}','{3}',{4}) as id".format(x.id,m,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1]),location[0]))
                            mname=MaintenanceType.objects.get(id=m).name
                            if(not "{0}_{1}".format("نفر_ساعت",mname) in lbls):
                                # lbls.append("{0}".format(mname))
                                lbls.append("{0}_{1}".format("نفر_ساعت",mname))
                            data["{0}".format(mname)]="{}".format(mres[0].id)
                            data["{0}_{1}".format("نفر_ساعت",mname)]="{:.2f}".format(mres[0].id/zarib[0].zaribUGMZ)

                    # maint.append(data)
                    javab["{0}-{1}".format(d[0],d[1])]=data
                mainJavab["{}".format(x.userGroupName)]=javab







            return render(request, 'cmms/reports/simplereports/UserGroupPerformanceWithGraph.html',{'javab':mainJavab,'lbl':lbls,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'location':location})
    def TotalTamirPerIstgah(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        location=request.POST.get("location","")
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        assetCategory=request.POST.getlist("assetCategory", "")
        if(len(assetCategory) >0 and not assetCategory[0]):
             assetCategory.pop(0)
        assetCategory=[int(i) for i in assetCategory]
        if(len(assetCategory)==0):
             assetCategory.append(-1)
        if((assetCategory[0]==-1)):
             assetCategory=AssetCategory.objects.values_list('id', flat=True)
        mainJavab={}
        tamircode=MaintenanceType.objects.filter(name__contains="تعمیر")[0].id
        tamirkol=0
        pertkol=0
        for x in assetCategory:
             name=AssetCategory.objects.get(id=x).name
             mainJavab[name]=Tasks.objects.raw("""select get_maintenance_time_by_assetcategory({0},{1},'{2}','{3}',{4}) as id   """.format(tamircode,x,date1,date2,location))[0].id
             pertkol+=Tasks.objects.raw("""select get_pert_time_assetcategory({0},'{1}','{2}',{3},{4}) as id   """.format(tamircode,date1,date2,location,x))[0].id
             tamirkol+=mainJavab[name]

        mainJavab["پرت کل"]=pertkol
        # mainJavab["کل تعمیرات"]=AssetCategory.objects.raw(""" select get_total_maintenance_time({0},'{1}','{2}') as id""".format(tamircode,date1,date2))[0].id
        mainJavab["کل تعمیرات"]=tamirkol
        return render(request, 'cmms/reports/simplereports/TotalTamirPerIstgah.html',{'javab':mainJavab,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate})
    def GroupTamirPerIstgah(self,request):
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        location=request.POST.get("location","")
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        assetCategory=request.POST.getlist("assetCategory", "")
        ugroup=request.POST.getlist("usergroup", "")
        if(len(ugroup) >0 and not ugroup[0]):
            # print("$$$$$$$$$$$$$$$$$$$$$$")
            ugroup.pop(0)
        ugroup=[int(i) for i in ugroup]
        if(len(ugroup)==0):
            ugroup.append(-1)
        if((ugroup[0]==-1)):
            ugroup=UserGroup.objects.values_list('id', flat=True).exclude(userGroupCode='other')
        ug=UserGroup.objects.filter(id__in=ugroup)

        if(len(assetCategory) >0 and not assetCategory[0]):
             assetCategory.pop(0)
        assetCategory=[int(i) for i in assetCategory]
        if(len(assetCategory)==0):
             assetCategory.append(-1)
        if((assetCategory[0]==-1)):
             assetCategory=AssetCategory.objects.values_list('id', flat=True)
        mainJavab={}
        tamircode=MaintenanceType.objects.filter(name__contains="تعمیر")[0].id
        tamirkol=0
        for u in ug:
            tamirkolcount=0
            tamirkoltime=0
            pertkoltime=0
            pertkolcount=0
            nonestopcount=0
            nonestoptime=0
            emcount=0
            emtime=0

            gjavab={}
            for x in assetCategory:
                 javab={}
                 name=AssetCategory.objects.get(id=x).name
                 javab["ساعت"]=Tasks.objects.raw("""select get_group_workorder_time_by_maintype_by_assetcategory({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id
                 tamirkoltime+=javab["ساعت"]
                 javab["تعداد"]=Tasks.objects.raw("""select get_group_workorder_count_by_maintype_by_assetcategory({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,x,location))[0].id
                 tamirkolcount+=javab["تعداد"]
                 if(javab["تعداد"]>0):
                    javab["mttr"]=javab["ساعت"]/javab["تعداد"]
                 else:
                    javab["mttr"]=0

                 pertkoltime+=WorkOrder.objects.raw("""select get_group_pert_time({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id
                 pertkolcount+=WorkOrder.objects.raw("""select get_group_pert_count({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id
                 nonestopcount+=WorkOrder.objects.raw("""select get_maintenance_count_station_nonestop({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id
                 nonestoptime+=WorkOrder.objects.raw("""select get_maintenance_time_station_nonestop({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id
                 emtime+=WorkOrder.objects.raw("""select get_maintenance_time_station_EM_assetcategory({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id
                 emcount+=WorkOrder.objects.raw("""select get_maintenance_time_station_count_EM_assetcategory({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id


                 # pertkol+=javab["پرت"]
                 # print("""select get_group_pert_time({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))

                 gjavab[name]=javab

            gjavab["پرت کل"]={}
            gjavab["کل تعمیرات"]={}
            gjavab["بدون توقف تولید"]={}
            gjavab["EM"]={}
            gjavab["EM"]["ساعت"]=emtime
            gjavab["EM"]["تعداد"]=emcount
            gjavab["EM"]["mttr"]=(emtime/emcount) if emcount >0 else 0
            gjavab["بدون توقف تولید"]["تعداد"]=nonestopcount
            gjavab["بدون توقف تولید"]["ساعت"]=nonestoptime
            gjavab["بدون توقف تولید"]["mttr"]=(nonestoptime/nonestopcount) if emcount >0 else 0
            gjavab["پرت کل"]["ساعت"]=pertkoltime
            gjavab["پرت کل"]["تعداد"]=pertkolcount
            gjavab["پرت کل"]["mttr"]=0
            gjavab["کل تعمیرات"]["ساعت"]=tamirkoltime
            gjavab["کل تعمیرات"]["تعداد"]=tamirkolcount
            if(tamirkolcount>0):
                 gjavab["کل تعمیرات"]["mttr"]=tamirkoltime/tamirkolcount
            else:
                  gjavab["کل تعمیرات"]["mttr"]=0









            mainJavab[u.userGroupName]=gjavab
            # mainJavab[u.userGroupName]["پرت کل"]=pertkol
            # mainJavab[u.userGroupName]["تعداد کل تعمیرات"]=tamirkolcount
            # mainJavab[u.userGroupName]["ساعت کل تعمیرات"]=tamirkoltime
        gname=[]
        for u in ug:
            gname.append(u.userGroupName)
        locname=Asset.objects.get(id=location).assetName



        return render(request, 'cmms/reports/simplereports/GroupTamirPerIstgah.html',{'javab':mainJavab,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate,'location':locname,'groups':gname})
    def GroupTamirPerIstgahPerMonth(self,request):
        SType=request.POST.get('SType','')
        dtset=DateJob.getQDateM(int(SType))#return a range
        location=request.POST.get("location","")
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        assetCategory=request.POST.getlist("assetCategory", "")
        ugroup=request.POST.getlist("usergroup", "")
        if(len(ugroup) >0 and not ugroup[0]):
            # print("$$$$$$$$$$$$$$$$$$$$$$")
            ugroup.pop(0)
        ugroup=[int(i) for i in ugroup]
        if(len(ugroup)==0):
            ugroup.append(-1)
        if((ugroup[0]==-1)):
            ugroup=UserGroup.objects.values_list('id', flat=True).exclude(userGroupCode='other')
        ug=UserGroup.objects.filter(id__in=ugroup)
        if(len(assetCategory) >0 and not assetCategory[0]):
             assetCategory.pop(0)
        assetCategory=[int(i) for i in assetCategory]
        if(len(assetCategory)==0):
             assetCategory.append(-1)
        if((assetCategory[0]==-1)):
             assetCategory=AssetCategory.objects.values_list('id', flat=True)

        tamircode=MaintenanceType.objects.filter(name__contains="تعمیر")[0].id
        tamirkol=0
        totalJavab={}
        tJavab={}
        for u in ug:
            mainJavab={}
            subJavab={}
            for d in dtset:
                dt=DateJob.findQDateM(d)
                tamirkolcount=0
                tamirkoltime=0
                pertkoltime=0
                pertkolcount=0
                nonestopcount=0
                nonestoptime=0
                emcount=0
                emtime=0

                gjavab={}
                ugavab={}

                for x in assetCategory:
                     javab=0
                     name=AssetCategory.objects.get(id=x).name
                     javab=Tasks.objects.raw("""select get_group_workorder_time_by_maintype_by_assetcategory({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1]),location,x))[0].id
                     tamirkoltime+=javab


                     pertkoltime+=WorkOrder.objects.raw("""select get_group_pert_time({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1]),location,x))[0].id
                     # pertkolcount+=WorkOrder.objects.raw("""select get_group_pert_count({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id
                     # nonestopcount+=WorkOrder.objects.raw("""select get_maintenance_count_station_nonestop({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id
                     nonestoptime+=WorkOrder.objects.raw("""select get_maintenance_time_station_nonestop({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1]),location,x))[0].id
                     emtime+=WorkOrder.objects.raw("""select get_maintenance_time_station_EM_assetcategory({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,DateJob.getDate2(dt[0]),DateJob.getDate2(dt[1]),location,x))[0].id
                     # emcount+=WorkOrder.objects.raw("""select get_maintenance_time_station_count_EM_assetcategory({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))[0].id


                     # pertkol+=javab["پرت"]
                     # print("""select get_group_pert_time({0},{1},'{2}','{3}',{4},{5}) as id   """.format(u.id,tamircode,date1,date2,location,x))

                     gjavab[name]=javab

                ugavab["پرت کل"]=0
                ugavab["کل تعمیرات"]=0
                ugavab["بدون توقف تولید"]=0
                ugavab["EM"]=0
                ugavab["EM"]=emtime
                # ugavab["EM"]["تعداد"]=emcount
                # ugavab["EM"]["mttr"]=(emtime/emcount) if emcount >0 else 0
                # ugavab["بدون توقف تولید"]["تعداد"]=nonestopcount
                ugavab["بدون توقف تولید"]=nonestoptime
                # ugavab["بدون توقف تولید"]["mttr"]=(nonestoptime/nonestopcount) if emcount >0 else 0
                ugavab["پرت کل"]=pertkoltime
                # ugavab["پرت کل"]["تعداد"]=pertkolcount
                # ugavab["پرت کل"]["mttr"]=0
                ugavab["کل تعمیرات"]=tamirkoltime
                # ugavab["کل تعمیرات"]["تعداد"]=tamirkolcount
                # if(tamirkolcount>0):
                #      ugavab["کل تعمیرات"]["mttr"]=tamirkoltime/tamirkolcount
                # else:
                #       ugavab["کل تعمیرات"]["mttr"]=0









                mainJavab["{0}-{1}".format(d[0],d[1])]=gjavab
                subJavab["{0}-{1}".format(d[0],d[1])]=ugavab
                # mainJavab[u.userGroupName]["پرت کل"]=pertkol
                # mainJavab[u.userGroupName]["تعداد کل تعمیرات"]=tamirkolcount
                # mainJavab[u.userGroupName]["ساعت کل تعمیرات"]=tamirkoltime
            totalJavab["{0}".format(u.userGroupName)]=mainJavab
            tJavab["{0}".format(u.userGroupName)]=subJavab

        gname=[]
        for u in ug:
            gname.append(u.userGroupName)
        locname=Asset.objects.get(id=location).assetName



        return render(request, 'cmms/reports/simplereports/GroupTamirPerIstgahPerMonth.html',{'javab':totalJavab,'sub':tJavab,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate,'location':locname,'groups':gname})
    def HozurTimePerGroup(self,request):
          date1=DateJob.getDate2(request.POST.get("startDate",""))
          date2=DateJob.getDate2(request.POST.get("endDate",""))
          location=request.POST.get("location","")
          startDate=request.POST.get("startDate","").replace('-','/')
          endDate=request.POST.get("endDate","").replace('-','/')
          ugroup=request.POST.getlist("usergroup", "")
          if(len(ugroup) >0 and not ugroup[0]):
               # print("$$$$$$$$$$$$$$$$$$$$$$")
               ugroup.pop(0)
          ugroup=[int(i) for i in ugroup]
          if(len(ugroup)==0):
               ugroup.append(-1)
          if((ugroup[0]==-1)):
               ugroup=UserGroup.objects.values_list('id', flat=True).exclude(userGroupCode='other')
          ug=UserGroup.objects.filter(id__in=ugroup)
          gname=[]
          for u in ug:
              gname.append(u.userGroupName)
          m=MaintenanceType.objects.all()
          javab={}
          for u in ug:
              tt={}
              for k in m:
                  tt['{}'.format(k.name)]=WorkOrder.objects.raw(""" select get_maintenance_time_usergroup({0},{1},'{2}','{3}',{4}) as id """.format(u.id,k.id,date1,date2,location))[0].id
              # print("""select get_unint_member_attendance({0},'{1}','{2}') as id""".format(u.id,date1,date2))
              kol=WorkOrder.objects.raw("""select get_unint_member_attendance({0},'{1}','{2}') as id""".format(u.id,date1,date2))[0].id
              tt["بدون برنامه"]=kol-sum(tt.values())
              javab['{}'.format(u.userGroupName)]=tt
          loc=Asset.objects.get(id=location).assetName
          return render(request, 'cmms/reports/simplereports/HozurTimePerGroup.html',{'javab':javab,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate,'groups':gname,'location':loc})
    def LogReport(Self,request):
         books=LogEntry.objects.none()
         reportType=request.POST.getlist("reportType","")
         date1=DateJob.getDate2(request.POST.get("startDate",""))
         date2=DateJob.getDate2(request.POST.get("endDate",""))
         startDate=request.POST.get("startDate","").replace('-','/')
         endDate=request.POST.get("endDate","").replace('-','/')
         if(len(reportType) >0 and not reportType[0]):
              reportType.pop(0)
         reportType=[str(i) for i in reportType]
         if(len(reportType)==0):
              reportType.append(-1)
         if((reportType[0]==-1)):
             print(LogEntry.objects.filter(action_time__range=(date1,date2)).query)

             books=LogEntry.objects.filter(action_time__range=(date1,date2))
         else:
             books=LogEntry.objects.filter(object_repr=reportType,action_time__range=(date1,date2))
         return render(request, 'cmms/reports/simplereports/logReport.html',{'wolog':books,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate})
    def SummaryReportByUser(Self,request):
         reportType=request.POST.getlist("reportType","")
         user=request.POST.get("usernames","")
         maintype=request.POST.get("maintenanceType","")
         date1=DateJob.getDate2(request.POST.get("startDate",""))
         date2=DateJob.getDate2(request.POST.get("endDate",""))
         startDate=request.POST.get("startDate","").replace('-','/')
         endDate=request.POST.get("endDate","").replace('-','/')
         n1=WOUtility.GetOnTimeCompletedWONumByUser(date1,date2,user,maintype)
         n2=WOUtility.GetTotalCompletedWONumByUser(date1,date2,user,maintype)
         n3=0
         try:
             n3=(n1[0].id/n2[0].id)*100
         except ZeroDivisionError:
             n3=0
         m1=WOUtility.GetOnTimeCompletedWONumByUser2(date1,date2,user)
         m2=WOUtility.GetTotalCompletedWONumByUser2(date1,date2,user)
         m3=0
         try:
             m3=(m1[0].id/m2[0].id)*100
         except ZeroDivisionError:
             m3=0
         s=WOUtility.GetDowntimeByUser(date1,date2,user)
         d={}
         for i in s:
             d[i.d2]=float("{:.2f}".format((float(i.id)/60)))
             # d[i.d2]=float(i.id)
         s2=WOUtility.GetDowntimeHitsReasonByUser(date1,date2,user)
         d2={}
         for i in s2:
             d2[i.d2]=i.id
         s3=WOUtility.GetUserWoByMType(date1,date2,user)
         d3={}

         for i in s3:
             d3[i.name]=i.id
         user_wo_by_mtype=UserUtility.getuser_work_hour_mtype(date1,date2,user)
         user_hozur=UserUtility.getHozurTimeUser(date1,date2,user)[0].id
         if(user_hozur is None):
             user_hozur=0
         d4={}
         total=0
         for i in user_wo_by_mtype:
             d4[i.name]=float("{:.2f}".format((float(i.id)/60)))
             total=total+float(i.id)
         d4["بدون برنامه"]=float("{:.2f}".format((((float(user_hozur)))-total)/60))


         username=SysUser.objects.get(id=user)
         mtype_name=MaintenanceType.objects.get(id=maintype)
         return render(request, 'cmms/reports/simplereports/SummaryReportByUser.html',{'result1':n3,'result2':m3,'result3':d,'result4':d2,'result5':d3,'result6':d4,'username':username.title,'mtype':mtype_name.name,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate})
    def SummaryReportByAsset(Self,request):
         reportType=request.POST.getlist("reportType","")
         asset=request.POST.get("assetname","")
         maintype=request.POST.get("maintenanceType","")
         date1=DateJob.getDate2(request.POST.get("startDate",""))
         date2=DateJob.getDate2(request.POST.get("endDate",""))
         startDate=request.POST.get("startDate","").replace('-','/')
         endDate=request.POST.get("endDate","").replace('-','/')
         n1=AssetUtility.GetOnTimeCompletedWONumByAsset(date1,date2,asset,maintype)
         n2=AssetUtility.GetTotalCompletedWONumByAsset(date1,date2,asset,maintype)
         n3=0
         try:
             n3=(n1[0].id/n2[0].id)*100
         except ZeroDivisionError:
             n3=0
         m1=AssetUtility.GetOnTimeCompletedWONumByAsset2(date1,date2,asset)
         m2=AssetUtility.GetTotalCompletedWONumByAsset2(date1,date2,asset)
         m3=0
         try:
             m3=(m1[0].id/m2[0].id)*100
         except ZeroDivisionError:
             m3=0
         s=AssetUtility.GetDowntimeByAsset(date1,date2,asset)
         d={}
         for i in s:
             d[i.d2]=float("{:.2f}".format((float(i.id)/60)))
             # d[i.d2]=float(i.id)
         s2=AssetUtility.GetDowntimeHitsReasonByAsset(date1,date2,asset)
         d2={}
         for i in s2:
             d2[i.d2]=i.id
         s3=AssetUtility.GetAssetWoByMType(date1,date2,asset)
         d3={}

         for i in s3:
             d3[i.name]=i.id


         assetname=Asset.objects.get(id=asset)
         mtype_name=MaintenanceType.objects.get(id=maintype)
         return render(request, 'cmms/reports/simplereports/SummaryReportByAsset.html',{'result1':n3,'result2':m3,'result3':d,'result4':d2,'result5':d3,'username':assetname.assetName,'mtype':mtype_name.name,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate})
    ################################
    def PartUsageByLocation(Self,request):
        reportType=request.POST.getlist("reportType","")
        makan=request.POST.get("makan","")
        assetType=request.POST.getlist("assetType","")
        assetname=request.POST.getlist("assetname","")
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        if(len(assetType) >0 and not assetType[0]):
            # print("$$$$$$$$$$$$$$$$$$$$$$")
            assetType.pop(0)
        assetType=[int(i) for i in assetType]
        if(len(assetType)==0):
            assetType.append(-1)
        if((assetType[0]==-1)):
             assetType=AssetCategory.objects.values_list('id', flat=True)

        if(len(assetname) >0 and not assetname[0]):
             assetname.pop(0)
        assetname=[int(i) for i in assetname]
        if(len(assetname)==0):
             assetname.append(-1)
        if((assetname[0]==-1)):
             assetname=Asset.objects.values_list('id', flat=True)
        n1=WorkorderPart.objects.values('woPartWorkorder__woAsset__assetName','woPartStock__stockItem__partName','woPartWorkorder__woAsset__assetCategory__name').filter(woPartWorkorder__woAsset__assetIsLocatedAt=makan,timeStamp__range=(date1,date2)).annotate(part_total=Sum('woPartActulaQnty')).order_by('woPartWorkorder__woAsset__assetName','-part_total')

        if(assetType[0]!=-1):
            n1=WorkorderPart.objects.values('woPartWorkorder__woAsset__assetName','woPartStock__stockItem__partName','woPartWorkorder__woAsset__assetCategory__name').filter(woPartWorkorder__woAsset__assetIsLocatedAt=makan,woPartWorkorder__woAsset__assetCategory__in=assetType,timeStamp__range=(date1,date2)).annotate(part_total=Sum('woPartActulaQnty')).order_by('woPartWorkorder__woAsset__assetName','-part_total')
        elif(assetname[0]!=-1):
            n1=WorkorderPart.objects.values('woPartWorkorder__woAsset__assetName','woPartStock__stockItem__partName','woPartWorkorder__woAsset__assetCategory__name').filter(woPartWorkorder__woAsset__assetIsLocatedAt=makan,woPartWorkorder__woAsset__in=assetname,timeStamp__range=(date1,date2)).annotate(part_total=Sum('woPartActulaQnty')).order_by('woPartWorkorder__woAsset__assetName','-part_total')
        return render(request, 'cmms/reports/simplereports/PartUsageByLocation.html',{'result1':n1,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate})
    def PartUsageByLocationandPart(Self,request):
        reportType=request.POST.getlist("reportType","")
        makan=request.POST.get("makan","")
        # print(makan)
        assetType=request.POST.getlist("assetType","")
        assetname=request.POST.getlist("assetname","")
        partName=request.POST.get("part","")
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        endDate=request.POST.get("endDate","").replace('-','/')
        if(len(assetType) >0 and not assetType[0]):
            # print("$$$$$$$$$$$$$$$$$$$$$$")
            assetType.pop(0)
        assetType=[int(i) for i in assetType]
        if(len(assetType)==0):
            assetType.append(-1)
        # if((assetType[0]==-1)):
        #      assetType=AssetCategory.objects.values_list('id', flat=True)

        if(len(assetname) >0 and not assetname[0]):
             assetname.pop(0)
        assetname=[int(i) for i in assetname]
        if(len(assetname)==0):
             assetname.append(-1)
        # if((assetname[0]==-1)):
        #      assetname=Asset.objects.values_list('id', flat=True)

        n1=WorkorderPart.objects.values('woPartWorkorder__woAsset__assetName','woPartStock__stockItem__partName',
        'woPartWorkorder__woAsset__assetCategory__name').filter(woPartWorkorder__woAsset__assetIsLocatedAt=makan,
        timeStamp__range=(date1,date2),woPartStock__stockItem_id=partName).annotate(part_total=Sum('woPartActulaQnty')).order_by('woPartWorkorder__woAsset__assetName','-part_total')
        # n2=WorkorderPart.objects.values('woPartWorkorder__woAsset__assetName','woPartStock__stockItem__partName',
        # 'woPartWorkorder__woAsset__assetCategory__name','timeStamp').filter(woPartWorkorder__woAsset__assetIsLocatedAt=makan,
        # woPartStock__stockItem_id=partName,timeStamp__range=(date1,date2)).annotate(part_total=Sum('woPartActulaQnty')).order_by('timeStamp')
        # # print(WorkorderPart.objects.filter(woPartWorkorder__woAsset__assetIsLocatedAt=makan,timeStamp__range=(date1,date2),woPartStock__stockItem_id=partName).query)
        n2=WorkorderPart.objects.raw(''' SELECT
              sum(workorderpart.woPartActulaQnty) as id ,
              pdate(date(workorderpart.timeStamp)) as t,
              parts.id as pid,
              parts.partName as p

            FROM
              workorderpart
              INNER JOIN workorder ON workorderpart.woPartWorkorder_id = workorder.id
              INNER JOIN assets ON workorder.woAsset_id = assets.id
              INNER JOIN stocks ON workorderpart.woPartStock_id = stocks.id
              INNER JOIN parts ON stocks.stockItem_id = parts.id
              INNER JOIN assetcategory ON assets.assetCategory_id = assetcategory.id
              where assets.assetIsLocatedAt_id={0} and (workorderpart.timeStamp between '{1}' and '{2}') and parts.id={3}
              group by t,pid,p
              '''.format(makan,date1,date2,partName))

        if(assetType[0]!=-1):
            n1=WorkorderPart.objects.values('woPartWorkorder__woAsset__assetName','woPartStock__stockItem__partName',
            'woPartWorkorder__woAsset__assetCategory__name').filter(woPartWorkorder__woAsset__assetIsLocatedAt=makan,woPartWorkorder__woAsset__assetCategory__in=assetType,timeStamp__range=(date1,date2),woPartStock__stockItem_id=partName).annotate(part_total=Sum('woPartActulaQnty')).order_by('woPartWorkorder__woAsset__assetName','-part_total')
            assetType.append(-1)

            n2=WorkorderPart.objects.raw(''' SELECT
                  sum(workorderpart.woPartActulaQnty) as id ,
                  pdate(date(workorderpart.timeStamp)) as t,
                  parts.id as pid,
                  parts.partName as p

                FROM
                  workorderpart
                  INNER JOIN workorder ON workorderpart.woPartWorkorder_id = workorder.id
                  INNER JOIN assets ON workorder.woAsset_id = assets.id
                  INNER JOIN stocks ON workorderpart.woPartStock_id = stocks.id
                  INNER JOIN parts ON stocks.stockItem_id = parts.id
                  INNER JOIN assetcategory ON assets.assetCategory_id = assetcategory.id
                  where assets.assetIsLocatedAt_id={0} and (workorderpart.timeStamp between '{1}' and '{2}') and parts.id={3} and assetcategory.id in {4}
                  group by t,pid,p
                  '''.format(makan,date1,date2,partName,tuple(assetType)))
        elif(assetname[0]!=-1):
            assetname.append(-1)
            n1=WorkorderPart.objects.values('woPartWorkorder__woAsset__assetName','woPartStock__stockItem__partName','woPartWorkorder__woAsset__assetCategory__name').filter(woPartWorkorder__woAsset__assetIsLocatedAt=makan,woPartWorkorder__woAsset__in=assetname,timeStamp__range=(date1,date2),woPartStock__stockItem_id=partName).annotate(part_total=Sum('woPartActulaQnty')).order_by('woPartWorkorder__woAsset__assetName','-part_total')
            n2=WorkorderPart.objects.raw(''' SELECT
                  sum(workorderpart.woPartActulaQnty) as id ,
                  pdate(date(workorderpart.timeStamp)) as t,
                  parts.id as pid,
                  parts.partName as p

                FROM
                  workorderpart
                  INNER JOIN workorder ON workorderpart.woPartWorkorder_id = workorder.id
                  INNER JOIN assets ON workorder.woAsset_id = assets.id
                  INNER JOIN stocks ON workorderpart.woPartStock_id = stocks.id
                  INNER JOIN parts ON stocks.stockItem_id = parts.id
                  INNER JOIN assetcategory ON assets.assetCategory_id = assetcategory.id
                  where assets.assetIsLocatedAt_id={0} and (workorderpart.timeStamp between '{1}' and '{2}') and parts.id={3} and assets.id in {4}
                  group by t,pid,p
                  '''.format(makan,date1,date2,partName,tuple(assetname)))
        # z1={}

        k=[]
            # print(n2)
        # print(n2.query)
        for i in n2:
            print(i)
            z1={}
            # z1['tedad']=i.woPartActulaQnty
            # print(jdatetime.date.fromgregorian(day=i.timeStamp.day,month=i.timeStamp.month,year=i.timeStamp.year))
            z1['zaman']=i.t
            z1['part']=i.p
            z1['total']=i.id
            k.append(z1)

        return render(request, 'cmms/reports/simplereports/PartUsageByLocationandPart.html',{'result1':n1,'result2':k   ,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'enddate':endDate})
    def MTBFByAnalythis(Self,request):
        reportType=request.POST.get("reportType","")
        reportType2=request.POST.get("reportType2","")
        makan=request.POST.get("makan","")
        behbood=request.POST.get("behbood","")
        alarm=request.POST.get("alarm","")

        assetname=request.POST.get("assetname","")
        date1=DateJob.getDate2(request.POST.get("startDate",""))
        date2=DateJob.getDate2(request.POST.get("endDate",""))
        startDate=request.POST.get("startDate","").replace('-','/')
        # endDate=request.POST.get("endDate","").replace('-','/')
        #محاسبه سال
        mtbf_vector=MTTR.get_mtbf_asset_mahane(assetname,startDate)
        z1=[]
        z2=[]
        print(reportType2)
        behbood_vec=[behbood]*12 if reportType2 == '0' else [behbood]*4
        alarm_vec=[alarm]*12 if reportType2 == '0' else [alarm]*4
        for i in mtbf_vector:
            z1.append(i)
            z2.append(mtbf_vector[i])
        # print(mtbf_vector)
        asset=Asset.objects.get(id=assetname).assetName
        return render(request, 'cmms/reports/simplereports/mtbfanalysis.html',{'result1':zip(z1,z2),'z1':z1,'z2':z2,'z3':behbood_vec,'z4':alarm_vec,'currentdate':jdatetime.datetime.now().strftime("%Y/%m/%d ساعت %H:%M:%S"),'stdate':startDate,'asset':asset})
