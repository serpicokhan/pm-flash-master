from cmms.models import WorkOrder,Asset
from django.db.models import Q

import jdatetime
import datetime
from django.core.paginator import *
class SWOUtility:

    @staticmethod
    def getListWorkorderLastWeek():
        lastweek=WorkOrder.objects.raw("select id,summaryofIssue,woPriority,woAsset_id,assignedToUser_id,woStatus,maintenanceType_id,completedByUser_id,estimatedLabor,actualLabor from workorder where isScheduling=True and pmonth(CURRENT_DATE)=pmonth(datecreated) and ceil(pday(datecreated)/7)=ceil(pday(CURRENT_DATE)/7) order by id desc")
        return lastweek
    @staticmethod
    def getListWorkorderLastMonth():
        lastmonth=WorkOrder.objects.raw("select id,summaryofIssue,woPriority,woAsset_id,assignedToUser_id,woStatus,maintenanceType_id,completedByUser_id,estimatedLabor,actualLabor from workorder where isScheduling=True and  pmonth(CURRENT_DATE)=pmonth(datecreated) order by id desc")
        return lastmonth
    @staticmethod
    def getlastWorkorder():
        company=WorkOrder.objects.filter(datecreated=datetime.date.today()).filter(isScheduling=True).order_by("-id")
        return company
    # Generate paging
    @staticmethod
    def doPaging(request,books):
        page=request.GET.get('page',1)
        paginator = Paginator(books, 10)
        wos=None
        try:
            wos=paginator.page(page)
        except PageNotAnInteger:
            wos = paginator.page(1)
        except EmptyPage:
            wos = paginator.page(paginator.num_pages)
        return wos
    @staticmethod
    def seachSWoByTags(searchStr):
        if(not searchStr):
            return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=True).order_by('-id')
        return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=True,woTags__contains=searchStr).order_by('-id')
    @staticmethod
    def getAssetSMSummaryReport(asset):
        wos=[]
        woList=[]
        if(len(asset)>0):
                assets=Asset.objects.filter(Q(assetIsLocatedAt__in=asset) | Q(id__in=asset))
                wos=WorkOrder.objects.filter(woAsset__id__in=assets,isScheduling=True).order_by('woAsset_id')
        else:
            print('else')
            wos=WorkOrder.objects.filter(isScheduling=True).order_by('woAsset_id')
        return wos
