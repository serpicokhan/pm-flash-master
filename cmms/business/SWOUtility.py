from cmms.models import *
from django.db.models import Q
from django.db import transaction

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
            return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=True).order_by('-running','-id')
        if(searchStr.isdigit()):
            return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=True).filter(Q(summaryofIssue__contains=searchStr)|Q(id=int(searchStr))).order_by('-running','-id')
        return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=True,woTags__contains=searchStr).order_by('-running','-id')
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
    @staticmethod
    def copy(ids,assetlist):
        with transaction.atomic():
            kl=[ids]
             ##### Create Wo #########
            for assets in assetlist:
                if(assets.isdigit()):

                    Ast=Asset.objects.get(id=assets)
                    for i in kl:
                        stableWo=WorkOrder.objects.get(id=i)
                        print(assets)
                        oldWo=WorkOrder.objects.get(id=i)
                        stableWo.pk=None
                        stableWo.visibile=False
                        stableWo.woAsset=Ast

                        stableWo.isScheduling=True
                        stableWo.isPm=False
                        # stableWo.datecreated=datetime.now().date()
                        # stableWo.timecreated=datetime.now().time()
                        # stableWo.isPartOf=unit.workOrder
                        # Newsch.schNextWo=WorkOrder.objects.create(datecreated=Newsch.schnextTime.date(),timecreated=Newsch.schnextTime.time(),visibile=False,isScheduling=False,isPartOf=Newsch.workOrder)
                        stableWo.save()

                        #################
                        # wt=WorkorderTask.objects.filter(workorder=oldWo)
                        wt=Tasks.objects.filter(workOrder=oldWo)
                        if(wt!=None):
                            for f in wt:
                                f.pk=None
                                f.workOrder=stableWo
                                f.save()
                        ##############
                        sch=Schedule.objects.filter(workOrder=oldWo)
                        if(sch!=None):
                            for f in sch:
                                f.pk=None
                                f.workOrder=stableWo
                                f.save()

                        ##############
                        wp=WorkorderPart.objects.filter(woPartWorkorder=oldWo)
                        if(wp!=None):
                            for f in wp:
                                f.pk=None
                                f.woPartWorkorder=stableWo
                                # woPartMsg=StockUtility.remove(f)
                                f.save()
                        ###############
                        wf=WorkorderFile.objects.filter(woFileworkorder=oldWo)
                        if(wf!=None):

                            for f in wf:
                                f.pk=None
                                f.woFileworkorder=stableWo
                                f.save()

                        ################
                        try:
                            wn=get_object_or_404(WorkorderUserNotification,woNotifWorkorder=oldWo)
                            if(wn!=None):
                                wn.pk=None
                                wn.woNotifWorkorder=stableWo
                                wn.save()
                        except Exception as es:
                            print(es)