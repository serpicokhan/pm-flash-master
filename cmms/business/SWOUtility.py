from cmms.models import *
from django.db.models import Q
from django.db import transaction

import jdatetime
import datetime
from django.core.paginator import *
from cmms.business.schedule_utility import *

from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
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
        else:
            return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=True).filter(Q(summaryofIssue__icontains=searchStr)|Q(woAsset__assetCode__icontains=searchStr)|Q(woAsset__assetName__icontains=searchStr)).order_by('-running','-id')

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
    def copy(ids,assetlist,request):
        with transaction.atomic():
            kl=ids
            print(kl,'k1')
            print(assetlist)
             ##### Create Wo #########
            for assets in assetlist:


                    Ast=Asset.objects.get(id=assets)

                    stableWo=WorkOrder.objects.get(id=kl)
                    print(assets)
                    oldWo=WorkOrder.objects.get(id=kl)
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
                    print(sch,"sch")
                    if(sch!=None):
                        for f in sch:
                            f.pk=None
                            f.workOrder=stableWo
                            f.workOrder.save()
                            f.schNextWo=None
                            f.save()
                            ScheduleUtility.CreateNewWO(f.id)

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
                    LogEntry.objects.log_action(
                        user_id         = request.user.pk,
                        content_type_id = ContentType.objects.get_for_model(oldWo).pk,
                        object_id       = oldWo.id,
                        object_repr     = 'sworkorder',
                        action_flag     = CHANGE,
                        change_message= request.META.get('REMOTE_ADDR')
                    )
                    LogEntry.objects.log_action(
                        user_id         = request.user.pk,
                        content_type_id = ContentType.objects.get_for_model(stableWo).pk,
                        object_id       = stableWo.id,
                        object_repr     = 'workorder',
                        action_flag     = CHANGE,
                        change_message= request.META.get('REMOTE_ADDR')
                    )
