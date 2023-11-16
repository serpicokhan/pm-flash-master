from cmms.models import *
import jdatetime
import datetime

from datetime import datetime
from django.core.paginator import *
from cmms.business.misccost import *
from cmms.business.taskUtility import *
from cmms.business.PartUtility import  *
from cmms.business.EquipCostSettingUtility import *
from decimal import Decimal
from cmms.utils import *
from django.db.models import Q
from django.db import transaction
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv
import locale
import codecs
from django.db.models import Count, F, Value
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
import difflib
from django.utils import timezone
from datetime import timedelta

class WOUtility:

    @staticmethod
    def find_similarity(str1,str2,ratio):
        string1=str1#.toLower()
        string2=str2#.toLower()
        similarity = difflib.SequenceMatcher(None, string1, string2).ratio()
        print("similarity",similarity)
        if(similarity>=ratio):
            return True
        return False
    @staticmethod
    def find_wos_created_within_5_days(wo):
        current_date = timezone.now().date()
        five_days_ago = current_date - timedelta(days=5)
        # Query rows created within the last 5 days
        rows = WorkOrder.objects.filter(datecreated__gte=five_days_ago,woAsset=wo.woAsset,maintenanceType=wo.maintenanceType).exclude(woStatus__in=[7,8])

        # Access the required data or perform further operations with the rows
        for row in rows:
            print("date:",row.datecreated)
            # Do something with each row
            if(WOUtility.find_similarity(wo.woTags,row.woTags,0.5)):
                return True

        return False


    @staticmethod
    def getListWorkorderLastWeek(request):
        u1=SysUser.objects.get(userId=request.user)
        wherestr=''
        if(request.user.username!="admin"):
            wherestr='and (t1.assignedToUser_id={0} or t2.woNotifUser_id={0})'.format(u1.id)
        # print("select t1.id as id from workorder t1 left join  workorderusernotification t2 on t1.id=t2.woNotifWorkorder_id where isScheduling=0 and pmonth(CURRENT_DATE)=pmonth(datecreated) and ceil(pday(datecreated)/7)=ceil(pday(CURRENT_DATE)/7) and visibile=1 {0} order by datecreated desc".format(wherestr))
        lastweek=WorkOrder.objects.raw("select t1.id as id from workorder t1 left join sysusers t3 on t1.assignedToUser_id=t3.id left join workorderusernotification t2 on t1.id=t2.woNotifWorkorder_id where isScheduling=0 and pmonth(CURRENT_DATE)=pmonth(datecreated) and ceil(pday(datecreated)/7)=ceil(pday(CURRENT_DATE)/7) and visibile=1 {0} order by datecreated desc".format(wherestr))
        return lastweek
    @staticmethod
    def getListWorkorderLastMonth(request):
        u1=SysUser.objects.get(userId=request.user)
        wherestr=''
        if(request.user.username!="admin"):
            wherestr='and (t1.assignedToUser_id={0} or t2.woNotifUser_id={0})'.format(u1.id)
        lastmonth=WorkOrder.objects.raw("select t1.id as id from workorder t1 left join workorderusernotification t2 on t1.id=t2.woNotifWorkorder_id where isScheduling=0 and  pmonth(CURRENT_DATE)=pmonth(datecreated) and visibile=1 {0} order by datecreated desc".format(wherestr))
        return lastmonth
    @staticmethod
    def getlastWorkorder():

        company=WorkOrder.objects.filter(datecreated=datetime.date.today()).filter(isScheduling=False,visibile=True).order_by("-datecreated")
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
    def doPagingWithPage(request,books):
        page=request.GET.get('page',1)
        paginator = Paginator(books, 10)
        wos=None
        try:
            wos=paginator.page(page)
        except PageNotAnInteger:
            wos = paginator.page(1)
        except EmptyPage:
            wos = paginator.page(paginator.num_pages)
        return wos,page
    #GET Wo on demand completed between 2 dates
    @staticmethod
    def GetCompletedWorkOrderNum(start,end,isScheduling,makan=None):
        #print("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and isPartOf_id {2} and isScheduling=0".format(start,end,isScheduling))
        # return WorkOrder.objects.raw("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and isPartOf_id  {2} and isScheduling=0 and visibile=1".format(start,end,isScheduling))
        wo=WorkOrder.objects.none()
        if(isScheduling=='is not null'):
             wo=WorkOrder.objects.filter(dateCompleted__range=(start,end),isPartOf__isnull=False,visibile=True,woStatus=7)
        else:
            wo=WorkOrder.objects.filter(dateCompleted__range=(start,end),isPartOf__isnull=True,visibile=True,woStatus=7)
        if(makan):
            wo=wo.filter(Q(woAsset__id=makan)|Q(woAsset__assetIsLocatedAt__id=makan))
        return wo.count()
    #########################################################################################
    @staticmethod
    def GetOnTimeCompletedWorkOrderNum(start,end,isScheduling,makan=None):
        wo=WorkOrder.objects.none()
        if(isScheduling=='is not null'):
            wo= WorkOrder.objects.filter(dateCompleted__lte=F('requiredCompletionDate'),dateCompleted__range=(start,end),woStatus=7,visibile=1,isPartOf__isnull=False)
        else:
            WorkOrder.objects.filter(dateCompleted__lte=F('requiredCompletionDate'),dateCompleted__range=(start,end),woStatus=7,visibile=1,isPartOf__isnull=True)
        if(makan):
                wo=wo.filter(Q(woAsset__id=makan)|Q(woAsset__assetIsLocatedAt__id=makan))
        return wo.count()


        # return WorkOrder.objects.raw("select count(id) as id from workorder where datecompleted <= requiredCompletionDate and (datecompleted between '{0}' and '{1}') and  wostatus=7 and isPartOf_id={2} and visibile=1".format(start,end,isScheduling))

    #########################################################################################
    @staticmethod
    def GetTotalCompletedWorkOrderNum(start,end):
        return WorkOrder.objects.raw("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and isScheduling=0".format(start,end))


    ########################################completion rate#################################################
    @staticmethod
    def GetOnTimeCompletedWONumByUser(start,end,user,maintype):

        return WorkOrder.objects.raw("select count(id) as id from workorder where datecompleted <= requiredCompletionDate and (datecompleted between '{0}' and '{1}') and  wostatus=7 and assignedToUser_id={2} and maintenanceType_id={3}".format(start,end,user,maintype))

    #########################################################################################
    @staticmethod
    def GetOnTimeCompletedWONumByUser2(start,end,user):

        return WorkOrder.objects.raw("select count(id) as id from workorder where datecompleted <= requiredCompletionDate and (datecompleted between '{0}' and '{1}') and  wostatus=7 and assignedToUser_id={2}".format(start,end,user))

    #########################################################################################
    @staticmethod
    def GetTotalCompletedWONumByUser(start,end,user,maintype):
        return WorkOrder.objects.raw("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and assignedToUser_id={2} and maintenanceType_id={3}".format(start,end,user,maintype))
    #########################################################################################
    @staticmethod
    def GetTotalCompletedWONumByUser2(start,end,user):
        return WorkOrder.objects.raw("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and assignedToUser_id={2} ".format(start,end,user))


    #########################################################################################
    @staticmethod
    def GetTotalOnTimeCompletedWorkOrderNum(start,end):
        return WorkOrder.objects.raw("select count(id) as id from workorder where datecompleted <requiredCompletionDate and (datecompleted between '{0}' and '{1}') and  wostatus=7 and isScheduling=0".format(start,end))
    #########################################################################################
    @staticmethod
    def GetDowntimeByUser(start,end,userid):
        # print("select count(assetlife.id) as id,s.stopDescription as d2,assetStopCode_id from assetlife left join StopCode as s on assetlife.assetStopCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetSetOfflineByUser_id={2} group by assetStopCode_id".format(start,end,userid))
        # print("select sum(timestampdiff(MINute,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ',assetOnlineFromTime) as datetime))) as id,s.stopDescription as d2,assetStopCode_id from assetlife left join StopCode as s on assetlife.assetStopCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetSetOfflineByUser_id={2} group by assetStopCode_id".format(start,end,userid))
        return AssetLife.objects.raw("select sum(timestampdiff(MINute,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ',assetOnlineFromTime) as datetime))) as id,s.stopDescription as d2,assetStopCode_id from assetlife left join stopcode as s on assetlife.assetStopCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetSetOfflineByUser_id={2} group by assetStopCode_id".format(start,end,userid))
    #########################################################################################
    @staticmethod
    def GetDowntimeHitsReasonByUser(start,end,userid):
        # print("select count(assetlife.id) as id,s.stopDescription as d2,assetStopCode_id from assetlife left join StopCode as s on assetlife.assetStopCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetSetOfflineByUser_id={2} group by assetStopCode_id".format(start,end,userid))
        return AssetLife.objects.raw("""select count(assetlife.id) as id,s.causeDescription as d2,s.id from assetlife
         join workorder as wo on wo.id=assetlife.assetWOAssoc_id
         left join causecode as s on wo.woCauseCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetSetOfflineByUser_id={2} group by s.id""".format(start,end,userid))
    #########################################################################################
    @staticmethod
    def GetUserWoByMType(start,end,userid):

        return WorkOrder.objects.raw(""" select count(wo.id) as id,maintenanceType_id,m.name as name from workorder as wo
        inner join maintenancetype as m on wo.maintenanceType_id=m.id
        where (wo.datecreated between '{0}' and '{1}') and wo.assignedToUser_id={2} and isScheduling=0 and visibile=1
        group by maintenanceType_id

         """.format(start,end,userid))
    #########################################################################################
    @staticmethod
    def getWoReqNum(start,end):
        # print("!1@#!@#@!",WorkOrder.objects.filter(datecreated__range=[start,end],isScheduling=False).count())

        return WorkOrder.objects.filter(datecreated__range=[start,end],isScheduling=False,visibile=True).count()
        # raw("SELECT  count(id) as id  from workorder where datecreated between '{0}' and '{1}' and isScheduling=0".format(start,end))
    #########################################################################################
    @staticmethod
    def getWoReqNum2(start,end,loc):


        return WorkOrder.objects.filter(datecreated__range=[start,end],isScheduling=False,woAsset__assetIsLocatedAt__id=loc).count()
        # raw("SELECT  count(id) as id  from workorder where datecreated between '{0}' and '{1}' and isScheduling=0".format(start,end))
    #########################################################################################

    @staticmethod
    def GetAvgDaysToCompletedNum(start,end):
        return WorkOrder.objects.raw("SELECT  AVG(DATEDIFF( datecompleted,datecreated)) as id  from workorder where datecreated between '{0}' and '{1}' and isScheduling=0 and wostatus=7".format(start,end))
    ############################
    @staticmethod
    def getAvgWOHourCost(start,end,price):
        #return total time amount of task for specific workorder
        return None

    #########################################################################################
    @staticmethod
    def GetAvgTotalCostPerWO(start,end):
        #calculate misc cost getMiscCoast(start,end)
        n1=ExtraCost.getMiscCost(start,end)
        #calculate workorder hour ==> select last price from general setting ???
        n2=TaskUtility.getTotalWorkHour(start,end)
        #calculate part cost
        n3=PartUtility.getPartCost(start,end)
        t1=0
        t2=0
        t3=0
        if(n1[0].id):
            t1=n1[0].id
        if(n2[0].id):
            t2=n2[0].id
        if(n3[0].id):
            t3=n3[0].id

        t4=t1+t2+t3

        return t4
    #########################################################################################
    @staticmethod
    def getWoCompletedPage(isScheduling):
        if(isScheduling==0):
            return "cmms/summery/onDemandStatus.html"
        elif(isScheduling==1):
            return "cmms/summery/pmStatus.html"
        else:
            return "cmms/summery/woStatus.html"
    @staticmethod
    def getResources(start,end,loc=None):
        where="and 1=1"
        print(loc,"loc")
        if(loc!='-1'):
            # pass
            where="and  workorder.woAsset_id in (select id from assets where id={0} or assetIsLocatedAt_id={0})".format(loc)
        # print("""SELECT fullname as id,format((ontime*100.0/totalCompleted),0) as p1,format(hour,1) as hour,total,format(totalcompleted*100/total,2) as t2,format(totalcompleted,0) as totalcompleted
        #                                 FROM ( SELECT count(id) as ontime, workorder.assignedToUser_id as u1
        #                                        FROM workorder
        #
        #                                        where workorder.visibile=1 and workorder.isScheduling=0 and workorder.datecreated between '{0}' and '{1}' and
        #                                         workorder.wostatus=7 and workorder.datecompleted <=workorder.requiredCompletionDate
        #                                      group by (u1)) AS A
        #                                 left JOIN ( SELECT count(id) as totalCompleted, workorder.assignedToUser_id as u2
        #                                        FROM workorder
        #
        #                                        where workorder.visibile=1 and workorder.isScheduling=0 and workorder.datecreated
        #                                        between '{0}' and '{1}' and workorder.wostatus=7 group by (u2)) AS B
        #
        #                                 ON A.u1=B.u2
        #
        #                                 left join (SELECT sum(TIMESTAMPDIFF(HOUR, cast(concat(taskStartDate, ' ', taskStartTime)
        #                                  as datetime),cast(concat(taskDateCompleted, ' ',
        #                                   taskTimeCompleted) as datetime))) as hour,taskAssignedToUser_id
        #                                   as u3 FROM `tasks`
        #                                    group by taskAssignedToUser_id) as C
        #                                 on A.u1=C.u3
        #                                 left join(select count(id) as total ,workorder.assignedToUser_id as u3 from workorder
        #                                  where workorder.datecreated between '{0}' and '{1}' and workorder.isScheduling=0 and workorder.visibile=1
        #                                 group by u3) as D
        #                                 on A.u1=D.u3
        #                                 left join sysusers on C.u1=sysusers.id
        #
        #                                 """.format(start,end))
        return WorkOrder.objects.raw("""
										SELECT fullname as id,sum(TIMESTAMPDIFF(HOUR, cast(concat(taskStartDate, ' ', taskStartTime)
                                         as datetime),cast(concat(taskDateCompleted, ' ',
                                          taskTimeCompleted) as datetime))) as hour,taskAssignedToUser_id
                                          FROM `tasks`


                                          right join workorder
                                          on workorder.id=tasks.workOrder_id
                                           join sysusers on tasks.taskAssignedToUser_id=sysusers.id
                                          where workorder.datecreated between '{0}' and '{1}' and workorder.visibile=1 and workorder.isScheduling=0
                                          {2}
                                          group by tasks.taskAssignedToUser_id
                                          order by hour desc
                                        """.format(start,end,where))
        #                                 """.format(start,end))
        # return WorkOrder.objects.raw("""SELECT fullname as id,format((ontime*100.0/totalCompleted),0) as p1,format(hour,1) as hour
        #                                 ,total,format(totalcompleted*100/total,2) as t2,
        #                                 format(totalcompleted,0) as totalcompleted
        #                                 FROM ( SELECT count(id) as ontime, workorder.assignedToUser_id as u1
        #                                        FROM workorder
        #
        #                                        where workorder.visibile=1 and workorder.isScheduling=0 and workorder.datecreated
        #                                         between '{0}' and '{1}' and
        #                                         workorder.wostatus=7 and workorder.datecompleted <=workorder.requiredCompletionDate
        #                                      group by (u1)) AS A
        #                                 left JOIN ( SELECT count(id) as totalCompleted, workorder.assignedToUser_id as u2
        #                                        FROM workorder
        #
        #                                        where workorder.visibile=1 and workorder.isScheduling=0 and workorder.datecreated
        #                                        between '{0}' and '{1}' and workorder.wostatus=7 group by (u2)) AS B
        #
        #                                 ON A.u1=B.u2
        #
        #                                 left join (SELECT sum(TIMESTAMPDIFF(HOUR, cast(concat(taskStartDate, ' ', taskStartTime)
        #                                  as datetime),cast(concat(taskDateCompleted, ' ',
        #                                   taskTimeCompleted) as datetime))) as hour,taskAssignedToUser_id as u3 FROM `tasks`
        #
        #
        #                                    group by taskAssignedToUser_id) as C
        #                                 on A.u1=C.u3
        #                                 left join(select count(id) as total ,workorder.assignedToUser_id as u3 from workorder
        #                                  where workorder.datecreated between '{0}' and '{1}' and workorder.visibile=1
        #                                 group by u3) as D
        #                                 on A.u1=D.u3
        #                                 left join sysusers on C.u3=sysusers.id
        #
        #                                 """.format(start,end))
    ##############################Status#######################
    @staticmethod
    def getWoStatusCount(start,end,woStatus):
        # print(""" select count(id) as id from workorder where datecreated between '{0}' and '{1}' and isPartOf_id is null and isScheduling=0 and wostatus={2}""".format(start,end))
        return WorkOrder.objects.raw(""" select count(id) as id from workorder where datecreated between '{0}' and '{1}' and isPartOf_id is null and isScheduling=0 and wostatus={2}""".format(start,end,woStatus))

    ##############################Status#######################
    @staticmethod
    def getPmStatusCount(start,end,woStatus):
        return WorkOrder.objects.raw(""" select count(id) as id from workorder where datecreated between '{0}' and '{1}' and isPartOf_id is not null and isScheduling=0 and wostatus={2}""".format(start,end,woStatus))
    ######################################OverDue###################
    @staticmethod
    def getOverDuePm(start,end):
        return WorkOrder.objects.raw(""" select count(id) as id from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and datecreated between '{0}' and '{1}' and isPartOf_id is not null and isScheduling=0 and ((curdate()>requiredCompletionDate and dateCompleted is null) or (datecompleted> requiredCompletionDate))""".format(start,end))
    #####################################Overdue
    @staticmethod
    def getOverDueWo(start,end):
        return WorkOrder.objects.raw(""" select count(id) as id from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and datecreated between '{0}' and '{1}' and isPartOf_id is  null and isScheduling=0 and ((curdate()>requiredCompletionDate and dateCompleted is null) or (datecompleted> requiredCompletionDate))""".format(start,end))
   #############################fetch overdued workorders ######################################
    @staticmethod
    def getOverDueWoList(start,end):
        return WorkOrder.objects.raw(""" select count(id) as id from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and datecreated between '{0}' and '{1}'  and isScheduling=0 and ((curdate()>requiredCompletionDate and dateCompleted is null) or (datecompleted> requiredCompletionDate))""".format(start,end))
    @staticmethod
    def getOverDueWoDetail(start,end):
        return WorkOrder.objects.raw(""" select * from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and visibile=1  and datecreated between '{0}' and '{1}'  and isScheduling=0  and ((curdate()>requiredCompletionDate ) or (datecompleted> requiredCompletionDate))""".format(start,end))

    ##########################Pue chart for completed wo by assets
    @staticmethod
    def getCompletedWoByAsset(start,end):
        assetList=list(EquipCostSettingUtility.getList())
        print(""" select count(workorder.id)  as id , assetname,woasset_id from workorder inner join assets on workorder.woasset_id=assets.id  where ( datecreated between '{0}' and '{1}') and wostatus=7  and woasset_id in ({2}) group by woasset_id """.format(start,end,",".join(str(x) for x in assetList)))
        #print(""" select count(id)  as id , woasset_id from workorder where ( datecreated between '{0}' and '{1}') and wostatus=7  and woasset_id in ({2}) group by woasset_id """.format(start,end,",".join(str(x) for x in assetList)))
        n1=WorkOrder.objects.raw(""" select count(workorder.id)  as id , assetname,woasset_id from workorder inner join assets on workorder.woasset_id=assets.id  where ( datecreated between '{0}' and '{1}') and wostatus=7  and woasset_id in ({2}) group by woasset_id """.format(start,end,",".join(str(x) for x in assetList)))
        n2=WorkOrder.objects.raw(""" select count(id)  as id  from workorder where ( datecreated between '{0}' and '{1}') and wostatus=7  and woasset_id not in ({2})  """.format(start,end,",".join(str(x) for x in assetList)))
        return (n1,n2)
    #######################################
    @staticmethod
    def GetHighPriorityWO(start,end):
        # print("!!!!","select count(id) as id from workorder where wopriority IN (1,2) and wostatus IN (1,4,5,6,9) and isScheduling=0 and datecreated between '{0}' and '{1}'".format(start,end))

        n1 = WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False,visibile=True, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9)).count()
        return n1
    @staticmethod
    def GetHighPriorityWO2(start,end,loc):
        # print("!!!!","select count(id) as id from workorder where wopriority IN (1,2) and wostatus IN (1,4,5,6,9) and isScheduling=0 and datecreated between '{0}' and '{1}'".format(start,end))

        n1 = WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False,visibile=True, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9),woAsset__assetIsLocatedAt__id=loc).count()
        return n1
    ##############################
    # @staticmethod
    # def getListedCompletedWoByAsset(start,end):
    #     assetList=list(AdminSettingUtility.getList())
    #     return Workorder.objects.raw(""" seelct count(id)  as id , asset_id from workorder where ( datecreated netween '{0}' and '{1}') and wostatus=7  and asset_id in {2} group by asset_id """.format(start,end,",".join(str(x) for x in assetList)))
    @staticmethod
    def getProblems(searchStr):
        # return WorkOrder.objects.raw("select distict(summaryofIssue) as id from workorder where summaryofIssue like '%سرویس%' and summaryofIssue is not null ")
        return WorkOrder.objects.filter(summaryofIssue__isnull=False,summaryofIssue__contains=searchStr).values_list('summaryofIssue',flat=True).order_by('summaryofIssue').distinct()
    @staticmethod
    def seachWoByTags(searchStr):

        if(not searchStr):
            return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=False,visibile=True).order_by('-id')
        if(searchStr.isdigit()):
            return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=False).filter(Q(summaryofIssue__contains=searchStr,visibile=True)|Q(id=int(searchStr))).order_by('-id')
        return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=False,visibile=True).filter(Q(summaryofIssue__contains=searchStr)|Q(woAsset__assetName__contains=searchStr)|Q(woAsset__assetCode__icontains=searchStr)).order_by('-id')

    @staticmethod
    def changeWoStatus2Waiting4Part(wo):
        woObj=WorkOrder.objects.get(id=wo.id)
        woObj.woStatus=9
        woObj.save()
#######################Simple Report######################
    @staticmethod
    def getOverdueWorkOrdersDetailReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        whereConition="where datecreated between '{0}' and '{1}'  and wostatus in (1,2,4,5,6,9) and isScheduling=0".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(asset)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  assetCategory_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)

        if(len(priority)>0):
            whereConition+=" and  woPriority in {0}".format(priority)




        return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate,
        cast(concat(dateCompleted, ' ', timeCompleted) as datetime) as t5,
        cast(concat(requiredCompletionDate, ' ', requiredCompletionTime) as datetime) as t6


        from workorder
        left join maintenancetype b on workorder.maintenancetype_id=b.id
        left join assets a on workorder.woasset_id=a.id
        left join assetcategory ac on a.assetCategory_id=ac.id
        {0}

        having t6<now()

         order by workorder.datecreated
         """.format(whereConition))
    @staticmethod
    def getOpenWorkOrdersDetailReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        # whereConition="where datecreated between '{0}' and '{1}' and wostatus in (1,2,4,5,6,9) and isScheduling=0".format(start ,end)
        # if(len(assignedUser)>0):
        #     whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        # if(len(asset)>0):
        #     whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        # if(len(assetCategory)>0):
        #     whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))
        #
        # if(len(maintenanceType)>0):
        #     whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)
        #
        # if(len(priority)>0):
        #     whereConition+=" and  woPriority in {0}".format(priority)
        #
        # return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        # timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        # timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate
        #
        # from workorder
        # inner join maintenancetype b on workorder.maintenancetype_id=b.id
        # inner join assets a on workorder.woasset_id=a.id
        # {0} order by workorder.id
        #  """.format(whereConition))
        wo=WorkOrder.objects.none()
        if(len(assignedUser)>0):
            wo=WorkOrder.objects.filter(assignedToUser__id__in=assignedUser,visibile=True,datecreated__range=[start,end],isScheduling=False).exclude(woStatus__in=(1,7,8))
        else:
            wo=WorkOrder.objects.filter(isScheduling=False,visibile=True,datecreated__range=[start,end]).exclude(woStatus__in=(1,7,8))
        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(len(assetCategory)>0):
            wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        else:
            if(len(asset)>0):
                wo=wo.filter(woAsset__id__in=asset)
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)
        return wo;
    @staticmethod
    def getWorkOrdersDetailReportByStatus(start,end,assignedUser,asset,assetCategory,maintenanceType,priority,status,makan):


        wo=WorkOrder.objects.filter(visibile=True,datecreated__range=[start,end],isScheduling=False)
        if(len(makan)>0):
            wo=wo.filter(Q(woAsset__id__in=makan)|Q(woAsset__assetIsLocatedAt__id__in=makan))
        if(len(assignedUser)>0):

            wo=wo.filter(assignedToUser__id__in=assignedUser)

        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(len(assetCategory)>0):
            wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        else:
            if(len(asset)>0):
                wo=wo.filter(woAsset__id__in=asset)
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)

        return wo.filter(woStatus=status,isScheduling=False,visibile=True);

    @staticmethod
    def getCloseWorkOrdersDetailReport(start,end,assignedUser,makan,assetName,maintenanceType,priority):


        # print("asset:",asset)
        # print("priority",priority)
        # print("maintenance:",assetCategory)
        wo=WorkOrder.objects.none()
        if(len(assignedUser)>0):
            wo=WorkOrder.objects.filter(isScheduling=False,assignedToUser__id__in=assignedUser,woStatus__in=(7,8),visibile=True,datecreated__range=[start,end])
        else:
            wo=WorkOrder.objects.filter(isScheduling=False,woStatus__in=(7,8),visibile=True,datecreated__range=[start,end])
        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(assetName):
                wo=wo.filter(woAsset__id__in=assetName)
        elif(len(makan)>0):
            wo=wo.filter(Q(woAsset__id__in=makan)|Q(woAsset__assetIsLocatedAt__id__in=makan)|Q(woAsset__assetIsPartOf__in=makan))
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)
        return wo.filter(isScheduling=False,visibile=True);
    @staticmethod
    def getCloseWorkOrdersListReport(start,end,assignedUser,makan,assetName,maintenanceType,priority):


        # print("asset:",asset)
        # print("priority",priority)
        # print("maintenance:",assetCategory)
        # wo=WorkOrder.objects.none()
        # if(len(assignedUser)>0):
        #     wo=WorkOrder.objects.filter(isScheduling=False,assignedToUser__id__in=assignedUser,woStatus__in=(7,8),visibile=True,datecreated__range=[start,end])
        # else:
        #     wo=WorkOrder.objects.filter(isScheduling=False,woStatus__in=(7,8),visibile=True,datecreated__range=[start,end])
        # if(len(maintenanceType)>0):
        #     wo=wo.filter(maintenanceType__id__in=maintenanceType)
        # if(len(assetCategory)>0):
        #     wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        # else:
        #     if(len(asset)>0):
        #         wo=wo.filter(woAsset__id__in=asset)
        # if(len(priority)>0):
        #     wo=wo.filter(woPriority__in=priority)
        # return wo.filter(isScheduling=False,visibile=True);

        #################
        wo=WorkOrder.objects.none()
        if(len(assignedUser)>0):
            wo=WorkOrder.objects.filter(isScheduling=False,assignedToUser__id__in=assignedUser,woStatus__in=(7,8),visibile=True,datecreated__range=[start,end])
        else:
            wo=WorkOrder.objects.filter(isScheduling=False,woStatus__in=(7,8),visibile=True,datecreated__range=[start,end])
        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(assetName):
                wo=wo.filter(woAsset__id__in=assetName)
        elif(len(makan)>0):
            wo=wo.filter(Q(woAsset__id__in=makan)|Q(woAsset__assetIsLocatedAt__id__in=makan)|Q(woAsset__assetIsPartOf__in=makan))
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)
        return wo.filter(isScheduling=False,visibile=True);


    @staticmethod
    def getAllWorkOrdersDetailReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        # whereConition="where datecreated between '{0}' and '{1}'  and isScheduling=0".format(start ,end)
        # if(len(assignedUser)>0):
        #     whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        # if(len(asset)>0):
        #     whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        # if(len(assetCategory)>0):
        #     whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))
        #
        # if(len(maintenanceType)>0):
        #     whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)
        #
        # if(len(priority)>0):
        #     whereConition+=" and  woPriority in {0}".format(priority)
        #
        # return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        # timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        # timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate
        #
        # from workorder
        # inner join maintenancetype b on workorder.maintenancetype_id=b.id
        # inner join assets a on workorder.woasset_id=a.id
        # {0} order by workorder.id
        #  """.format(whereConition))
        wo=WorkOrder.objects.none()
        if(len(assignedUser)>0):
            wo=WorkOrder.objects.filter(assignedToUser__id__in=assignedUser,isScheduling=False,visibile=True,datecreated__range=[start,end])
        else:
            wo=WorkOrder.objects.filter(isScheduling=False,visibile=True,datecreated__range=[start,end])
        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(len(assetCategory)>0):
            wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        else:
            if(len(asset)>0):
                wo=wo.filter(woAsset__id__in=asset)
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)
        return wo.filter(isScheduling=False,visibile=True);
    @staticmethod
    def getRequestedWorkOrdersListReport(start,end,asset,assetCategory,maintenanceType,priority,makan=None,starttime=None,endtime=None):

        start_datetime=None
        end_datetime=None
        wo=WorkOrder.objects.none()
        # if(len(assignedUser)>0):
        #     wo=WorkOrder.objects.filter(isScheduling=False,assignedToUser__id__in=assignedUser,woStatus__in=(1),visibile=True,datecreated__range=[start,end])
        # else:
        wo=WorkOrder.objects.filter(isScheduling=False,woStatus=1,visibile=True)
        if(makan):
            wo=wo.filter(Q(woAsset__assetIsLocatedAt__id__in=makan)|Q(woAsset__id__in=makan))

        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(len(assetCategory)>0):
            wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        else:
            if(len(asset)>0):
                wo=wo.filter(woAsset__id__in=asset)
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)
        if(starttime):
            time_object = datetime.datetime.strptime(starttime, "%H:%M:%S").time()
            start_datetime = datetime.datetime.combine(start, time_object)
        else:
            start_datetime=datetime.datetime.combine(start, datetime.time(0,0,0))
        if(endtime):
            time_object = datetime.datetime.strptime(endtime, "%H:%M:%S").time()

            end_datetime = datetime.datetime.combine(end, time_object)
        else:
            end_datetime=datetime.datetime.combine(end, datetime.time(11,59,59))
        #     wo=wo.filter(timecreated__gte=starttime)
        # if(endtime):
        #     wo=wo.filter(timecreated__lte=endtime)
        filter_condition = Q(
                            Q(datecreated__gt=start_datetime.date()) |  # Row's datecreated is after start_date
                            Q(datecreated=start_datetime.date(), timecreated__gte=start_datetime.time())
                        ) & Q(
                            Q(datecreated__lt=end_datetime.date()) |  # Row's datecreated is before end_date
                            Q(datecreated=end_datetime.date(), timecreated__lte=end_datetime.time())
                        )
        return wo.filter(filter_condition).order_by('datecreated','timecreated');
    @staticmethod
    def getOpenWorkOrdersListReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority,makan=None):


        wo=WorkOrder.objects.none()
        wo=WorkOrder.objects.filter(isScheduling=False,woStatus__in=(2,4,5,6,9),visibile=True,datecreated__range=[start,end])
        print(wo.query)
        if(makan):
            print(makan,'!!!')
            wo=wo.filter(Q(woAsset__assetIsLocatedAt__id__in=makan)|Q(woAsset__id__in=makan))
            # print(wo.query)
        if(len(assignedUser)>0):
            # wo=WorkOrder.objects.filter(isScheduling=False,assignedToUser__id__in=assignedUser,woStatus__in=(1,2,4,5,6,9),visibile=True,datecreated__range=[start,end])
            # wo=WorkOrder.objects.filter(isScheduling=False,assignedToUser__id__in=assignedUser,woStatus__in=(1,2,4,5,6,9),visibile=True,datecreated__range=[start,end])
            wo=wo.filter(assignedToUser__id__in=assignedUser)
        # else:
        #     wo=WorkOrder.objects.filter(isScheduling=False,woStatus__in=(1,2,4,5,6,9),visibile=True,datecreated__range=[start,end])
        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(len(assetCategory)>0):
            wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        else:
            if(len(asset)>0):
                wo=wo.filter(woAsset__id__in=asset)
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)
        return wo.filter(isScheduling=False,visibile=True);
    @staticmethod
    def getWorkOrdersListReportByStatus(start,end,assignedUser,asset,assetCategory,maintenanceType,priority,status,makan):


        wo=WorkOrder.objects.filter(datecreated__range=[start,end])
        if(len(makan)>0):
            wo=wo.filter(Q(woAsset__id__in=makan)|Q(woAsset__assetIsLocatedAt__id__in=makan))
        if(len(assignedUser)>0):
            wo=wo.filter(assignedToUser__id__in=assignedUser)
        else:
            wo=WorkOrder.objects.filter(datecreated__range=[start,end])
        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(len(assetCategory)>0):
            wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        else:
            if(len(asset)>0):
                wo=wo.filter(woAsset__id__in=asset)
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)
        return wo.filter(woStatus=status,isScheduling=False,visibile=True);

    @staticmethod
    def getOpenPMWorkOrdersListReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        # whereConition="where datecreated between '{0}' and '{1}' and wostatus in (1,2,4,5,6,9) and isScheduling=0 and isPartOf_id is not null".format(start ,end)
        # if(len(assignedUser)>0):
        #     whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        # if(len(asset)>0):
        #     whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        # if(len(assetCategory)>0):
        #     whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))
        #
        # if(len(maintenanceType)>0):
        #     whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)
        #
        # if(len(priority)>0):
        #     whereConition+=" and  woPriority in {0}".format(priority)
        #
        # return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        # pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        # timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate,
        # woPriority,estimatedLabor
        #
        # from workorder
        # inner join maintenancetype b on workorder.maintenancetype_id=b.id
        # inner join assets a on workorder.woasset_id=a.id
        # {0} order by workorder.id
        #  """.format(whereConition))
        wo=WorkOrder.objects.none()
        if(len(assignedUser)>0):
            wo=WorkOrder.objects.filter(isScheduling=False,assignedToUser__id__in=assignedUser,woStatus__in=(1,2,4,5,6,9),visibile=True,datecreated__range=[start,end],isPm=True)
        else:
            wo=WorkOrder.objects.filter(isScheduling=False,woStatus__in=(1,2,4,5,6,9),visibile=True,datecreated__range=[start,end],isPm=True)
        if(len(maintenanceType)>0):
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        if(len(assetCategory)>0):
            wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        else:
            if(len(asset)>0):
                wo=wo.filter(woAsset__id__in=asset)
        if(len(priority)>0):
            wo=wo.filter(woPriority__in=priority)
        return wo.filter(isScheduling=False,visibile=True);
    @staticmethod
    def getOpenWorkOrderGraphReport(start,end,assignedUser,asset,assetCategory,maintenanceType,makan):

        wo=WorkOrder.objects.filter(datecreated__range=[start,end],isScheduling=False,visibile=True,woStatus__in=(2,4,5,6,9))
        # whereConition="where datecreated between '{0}' and '{1}' and wostatus in (1,2,4,5,6,9) and isScheduling=0  and visibile=1".format(start ,end)
        if(len(makan)>0):
            wo=wo.filter(Q(woAsset__id__in=makan)|Q(woAsset__assetIsLocatedAt__id__in=makan))

        if(len(assignedUser)>0):
            # whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
            wo=wo.filter(assignedToUser__in=assignedUser)
        if(len(assetCategory)>0):
            # whereConition+=" and  a.id in {0}".format(str(assetCategory))
            wo=wo.filter(woAsset__assetCategory__id__in=assetCategory)
        if(len(asset)>0):
                # whereConition+=" and  woasset_id in {0}".format(str(asset))
                wo=wo.filter(woAsset__id__in=asset)


        if(len(maintenanceType)>0):
            # whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)
            wo=wo.filter(maintenanceType__id__in=maintenanceType)
        return wo.values('maintenanceType__name').annotate(count=Count('id'))


        # return WorkOrder.objects.raw("""  select count(workorder.id) as id, b.name as name ,b.id as k
        #
        # from workorder
        # inner join maintenancetype b on workorder.maintenancetype_id=b.id
        # left join assets on workorder.woasset_id=assets.id
        # left join assetcategory as a on assets.assetCategory_id= a.id
        #
        #
        # {0}
        # group by b.name,b.id
        #
        # order by workorder.id
        #  """.format(whereConition))

    @staticmethod
    def getCloseWorkOrderGraphReport(start,end,assignedUser,asset,assetCategory,maintenanceType):

        whereConition="where datecreated between '{0}' and '{1}' and wostatus in (7,8) and isScheduling=0 ".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(assetCategory)>0):
            whereConition+=" and  a.id in {0}".format(str(assetCategory))
        else:
            if(len(asset)>0):
                whereConition+=" and  woasset_id in {0}".format(str(asset))


        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)



        return WorkOrder.objects.raw("""  select count(workorder.id) as id, b.name as name ,b.id as k

            from workorder
            inner join maintenancetype b on workorder.maintenancetype_id=b.id
            left join assets on workorder.woasset_id=assets.id
            left join assetcategory as a on assets.assetCategory_id= a.id


            {0}
            group by b.name,b.id

            order by workorder.id
             """.format(whereConition))
    @staticmethod
    def getProjectsReportWithWorkOrderDetails(start,end,woStatus):

        whereConition="where ProjectActualStartDate >= '{0}' and ProjectActualEndDate <='{1}'  ".format(start ,end)
        if(len(woStatus)>0):
            whereConition+=" and  b.woStatus in {0}".format(str(woStatus))


        return Project.objects.raw("""  select project.id
        from project
        left join workorder b on b.project_id=project.id
        {0}
        group by project.id

        order by project.id
         """.format(whereConition))
    @staticmethod
    def getWorkOrderProjectDetails(projectId):



        return WorkOrder.objects.raw("""
        select id,summaryofIssue,wostatus,isPartOf_id,
        get_workorder_part_price(id) as partcost,
        get_workorder_labor_price(id) as laborcost,
        get_workorder_misccost(id) as misccost

        from workorder
        where project_id={0}

        """.format(projectId))
    @staticmethod
    def getCauseCount(start,end,assetCategory):
        whereConition=""
        if(len(assetCategory)>0):
            whereConition=" and  woAsset_id in {0}".format(str(assetCategory))
        # print(""" select count(id) as tedad,causecode as id,causeDescription
        # from workOrder a
        # inner join causecode b
        # on a.woCauseCode=b.id
        # where (a.datecreated between '{0}' and '{1}') and isScheduling=0 {2}
        # group by(causecode)
        # """.format(start,end,whereConition))
        return WorkOrder.objects.raw(""" select count(wocausecode_id) as tedad,causecode as id,causeDescription
        from workorder a
        inner join causecode b
        on a.wocausecode_id=b.id
        where (a.datecreated between '{0}' and '{1}') and isScheduling=0 {2}
        group by(causecode)
        """.format(start,end,whereConition))
    @staticmethod
    def getCauseCountv2(start,end,assetCategory=None,makan=None,assetname=None):
        # whereConition=""
        # if(len(assetCategory)>0):
        #     whereConition=" and  assetLifeAssetid_id in {0}".format(str(assetCategory))
        #
        # # print(""" select count(id) as tedad,causecode as id,causeDescription
        # # from workOrder a
        # # inner join causecode b
        # # on a.woCauseCode=b.id
        # # where (a.datecreated between '{0}' and '{1}') and isScheduling=0 {2}
        # # group by(causecode)
        # # """.format(start,end,whereConition))
        # return WorkOrder.objects.raw(""" select count(assetCauseCode_id) as tedad,assetCauseCode_id as id,causeDescription
        # from assetlife a
        # inner join causecode b
        # inner
        # on a.assetCauseCode_id=b.id
        # where (a.assetOfflineFrom between '{0}' and '{1}')  {2}
        # group by(causecode)
        # """.format(start,end,whereConition))
        result = AssetLife.objects.values('assetCauseCode', 'assetCauseCode__causeDescription') \
        .annotate(tedad=Count('assetCauseCode')) \
        .filter(
            Q(assetOfflineFrom__range=[start, end])
        ) \
        .order_by('assetCauseCode')
        # if(assetCategory):
        #
        #     result=result.filter(assetLifeAssetid__assetCategory__in=assetCategory)
        if(makan):
            result =result.filter(assetLifeAssetid__assetIsLocatedAt__id=makan)
        if(assetname):
            result =result.filter(assetLifeAssetid__in=assetname)

        # result=result.order_by('assetCauseCode')
        return result.order_by('-tedad')




    @staticmethod
    def getProblemCount(start,end,assetCategory):
        whereConition=""
        if(len(assetCategory)>0):
            whereConition=" and  woAsset_id in {0}".format(str(assetCategory))
        return WorkOrder.objects.raw(""" select count(wocausecode_id) as tedad,problemcode as id,problemDescription
        from workOrder a
        inner join problemcode b
        on a.woproblemcode_id=b.id
        where (a.datecreated between '{0}' and '{1}') and isScheduling=0 {2}
        group by(problemcode)
        """.format(start,end,whereConition))
    @staticmethod
    def getWorkOrderCostListReport(start,end,asset,assetCategory):
        a1="(0=1)"
        b1="(0=1)"
        if(len(assetCategory)==0 and len(asset)==0):
            b1="(1=1)"
        if(len(assetCategory)>0):
            a1="   b.assetcategory_id in {0}".format(str(assetCategory))
        if(len(asset)>0):
            b1="   woAsset_id in {0}".format(str(asset))


        return WorkOrder.objects.raw(""" select workorder.id as id,b.id ,  get_workorder_part_price(workorder.id) as partcost,
           get_workorder_labor_price(workorder.id) as laborcost,
           get_workorder_misccost(workorder.id) as misccost,
           (IFNULL(get_workorder_part_price(workorder.id),0)+IFNULL(get_workorder_labor_price(workorder.id),0)+IFNULL(get_workorder_misccost(workorder.id),0)) as total
           from workOrder
           left join assets b on workorder.woasset_id=b.id
           where (dateCompleted between '{0}' and '{1}') and ({2} or {3})
           order by total desc

           """.format(start,end,a1,b1))
    @staticmethod
    def getWorkOrderCostDetailReport(start,end,asset):
        #same as above but asset parameter must take between ()
        b1="   woAsset_id in ({0})".format(str(asset))
        return WorkOrder.objects.raw(""" select workorder.id as id,b.id ,  get_workorder_part_price(workorder.id) as partcost,
           get_workorder_labor_price(workorder.id) as laborcost,
           get_workorder_misccost(workorder.id) as misccost,
           (IFNULL(get_workorder_part_price(workorder.id),0)+IFNULL(get_workorder_labor_price(workorder.id),0)+IFNULL(get_workorder_misccost(workorder.id),0)) as total
           from workOrder
           left join assets b on workorder.woasset_id=b.id
           where (dateCompleted between '{0}' and '{1}') and ({2}) order by total desc

           """.format(start,end,b1))
##################################
#this report is userd in userlist.html user detail part
    @staticmethod
    def getNumCompletedWoCurrentMonth(uid):
        #use in user page
        jdt1=jdatetime.datetime.now()
        jdt2=jdatetime.date(jdt1.year, jdt1.month, 1)
        endDate=datetime.datetime.now().date()
        stDate= jdt2.togregorian()




        return WorkOrder.objects.raw(""" SELECT workorder.id as id,
                  count(distinct(workorder.id)) as k
                FROM
                  workorder
                  INNER JOIN tasks ON tasks.workOrder_id = workorder.id
                    where tasks.taskAssignedToUser_id = {0}
                    and workorder.woStatus=7 and (workorder.datecreated between '{1}' and '{2}') and isScheduling=0

                    """.format(uid,stDate,endDate))
##################################
#this report is userd in userlist.html user detail part
    @staticmethod
    def getNumCompletedWoCurrentYear(uid):
        jdt1=jdatetime.datetime.now()
        jdt2=jdatetime.date(jdt1.year, 1, 1)
        endDate=datetime.datetime.now().date()
        stDate= jdt2.togregorian()


        #use in user page
        return WorkOrder.objects.raw(""" SELECT workorder.id as id,
                 count(distinct(workorder.id)) as k
                FROM
                  workorder
                  INNER JOIN tasks ON tasks.workOrder_id = workorder.id
                  where tasks.taskAssignedToUser_id = {0}
                    and workorder.woStatus=7 and (workorder.datecreated between '{1}' and '{2}') and isScheduling=0""".format(uid,stDate,endDate))
##########################################
#this report is userd in userlist.html user detail part
    @staticmethod
    def getnOnTimeCompletedWOCurrentMonth(uid):
        jdt1=jdatetime.datetime.now()
        jdt2=jdatetime.date(jdt1.year, jdt1.month, 1)
        endDate=datetime.datetime.now().date()
        stDate= jdt2.togregorian()

        return WorkOrder.objects.raw(''' select workorder.id as id , count(distinct(workorder.id)) as k from workorder
        INNER JOIN tasks ON tasks.workOrder_id = workorder.id
         where tasks.taskAssignedToUser_id={0} and ( datecreated between '{1}' and '{2}') and woStatus=7 and isScheduling=0 and datecreated <= requiredCompletionDate '''.format(uid,stDate,endDate))
    @staticmethod
    def getnOnTimeCompletedWOCurrentYear(uid):
        jdt1=jdatetime.datetime.now()
        jdt2=jdatetime.date(jdt1.year, 1, 1)
        endDate=datetime.datetime.now().date()
        stDate= jdt2.togregorian()
        return WorkOrder.objects.raw(''' select workorder.id as id , count(distinct(workorder.id)) as k from workorder
        INNER JOIN tasks ON tasks.workOrder_id = workorder.id
         where tasks.taskAssignedToUser_id={0} and ( datecreated between '{1}' and '{2}') and woStatus=7 and isScheduling=0 and datecreated <= requiredCompletionDate '''.format(uid,stDate,endDate))
    ##############################################
    #this report is userd in userlist.html user detail part

    @staticmethod
    def getAllWorkCountCurrentMonth(uid):
        #use in user page
        jdt1=jdatetime.datetime.now()
        jdt2=jdatetime.date(jdt1.year, jdt1.month, 1)
        endDate=datetime.datetime.now().date()
        stDate= jdt2.togregorian()
        return WorkOrder.objects.raw(""" SELECT workorder.id as id,
                  count(distinct(workorder.id)) as k
                FROM
                  workorder
                  INNER JOIN tasks ON tasks.workOrder_id = workorder.id
                    where tasks.taskAssignedToUser_id = {0}
                    and (workorder.datecreated between '{1}' and '{2}') and isScheduling=0""".format(uid,stDate,endDate))
    ##############################################
    #this report is userd in userlist.html user detail part

    @staticmethod
    def getAllWorkCountCurrentYear(uid):
        #use in user page
        jdt1=jdatetime.datetime.now()
        jdt2=jdatetime.date(jdt1.year, 1, 1)
        endDate=datetime.datetime.now().date()
        stDate= jdt2.togregorian()
        return WorkOrder.objects.raw(""" SELECT workorder.id as id,
                  count(distinct(workorder.id)) as k
                FROM
                  workorder
                  INNER JOIN tasks ON tasks.workOrder_id = workorder.id
                    where tasks.taskAssignedToUser_id = {0}
                    and (workorder.datecreated between '{1}' and '{2}') and isScheduling=0""".format(uid,stDate,endDate))


    @staticmethod
    def checkTaskDateRange(woInstance):
        return WorkOrder.objects.raw("SELECT hasGreaterDate ({0},'{1}') AS id".format(woInstance.id,datetime.datetime.combine(woInstance.dateCompleted,woInstance.timeCompleted)))[0].id

    @staticmethod
    def wst_vs_tst(woInstance):
        return WorkOrder.objects.raw("SELECT stDate_Vs_stTask ({0},'{1}') AS id".format(woInstance.id,datetime.datetime.combine(woInstance.datecreated,woInstance.timecreated)))[0].id

    @staticmethod
    def checkWODateRange(woInstance):
        dt1=datetime.datetime.combine(woInstance.dateCompleted,woInstance.timeCompleted)
        dt2=datetime.datetime.combine(woInstance.datecreated,woInstance.timecreated)
        if(dt1>=dt2):
            return 1
        else:
            return -1
    @staticmethod
    def checkErr(*kerr):
        print(kerr)
        err_msg=''
        err_code=0
        if(kerr[0]==-1):
            err_msg='تاریخ پایان دستور کار از تاریخ یک از کارها کوچکتر است'
            err_code=1
        if(kerr[1]==-1):
            err_msg='تاریخ شروع دستورکار از تاریخ پایان بزرگتر است'
            err_code=1
        if(kerr[2]==-1):
            err_msg='تاریخ شروع بایستی از تاریخ شروع کارها کمتر باشد'
            err_code=1
        return err_code,err_msg
    @staticmethod
    def getOverdueWoAsset(AID):
        # print(""" select count(workorder.id) as id from workorder inner join assets on assets.id=workorder.woasset_id where ( woasset_id={0} or assets.assetIsLocatedAt_id={0}) and (woStatus IN (1,2,4,5,6,9) or woStatus is NULL )  and isScheduling=0 and ((curdate()>requiredCompletionDate and dateCompleted is null) or (datecompleted> requiredCompletionDate))""".format(AID))
        return WorkOrder.objects.raw(""" select count(workorder.id) as id from workorder inner join assets on assets.id=workorder.woasset_id where ( woasset_id={0} or assets.assetIsLocatedAt_id={0} or assets.assetIsPartOf_id={0}) and (woStatus IN (1,2,4,5,6,9) or woStatus is NULL )  and isScheduling=0 and ((curdate()>requiredCompletionDate and dateCompleted is null) or (datecompleted> requiredCompletionDate))""".format(AID))
    @staticmethod
    def getOpenWoAsset(AID):
        # print(""" select count(workorder.id) as id from workorder inner join assets on assets.id=workorder.woasset_id where ( woasset_id={0} or assets.assetIsLocatedAt_id={0}) and (woStatus IN (1,2,4,5,6,9) or woStatus is NULL )  and isScheduling=0 """.format(AID))
        return WorkOrder.objects.raw(""" select count(workorder.id) as id from workorder inner join assets on assets.id=workorder.woasset_id where ( woasset_id={0} or assets.assetIsLocatedAt_id={0} or assets.assetIsPartOf_id={0}) and (woStatus IN (1,2,4,5,6,9) or woStatus is NULL )  and isScheduling=0 """.format(AID))
    @staticmethod
    def getWait4PartWoAsset(AID):
        # print(""" select count(workorder.id) as id from workorder inner join assets on assets.id=workorder.woasset_id where ( woasset_id={0} or assets.assetIsLocatedAt_id={0}) and (woStatus IN (9 ) or woStatus is NULL )  and isScheduling=0 """.format(AID))
        return WorkOrder.objects.raw(""" select count(workorder.id) as id from workorder inner join assets on assets.id=workorder.woasset_id where ( woasset_id={0} or assets.assetIsLocatedAt_id={0} or assets.assetIsPartOf_id={0}) and (woStatus IN (9 ) or woStatus is NULL )  and isScheduling=0 """.format(AID))
    @staticmethod
    def getRequestedWo(start,end):
        n1=WorkOrder.objects.filter(woStatus=1,datecreated__range=[start,end],isScheduling=False,visibile=True).count();
        return n1
    @staticmethod
    def getDashCauseCount(start,end):
        d={}
        causes=CauseCode.objects.all()
        for c in causes:
            d[c.causeDescription]=WorkOrder.objects.raw(""" select count(id) as id from workorder where woCauseCode_id={0} and datecreated between '{1}' and '{2}'""".format(c.id,start,end))[0].id
        return d
    #EM
    @staticmethod
    def getDashCauseCount2(start,end,loc):
        d={}
        causes=CauseCode.objects.all()
        for c in causes:
            d[c.causeDescription]=WorkOrder.objects.raw(""" select count(workorder.id) as id from workorder
            inner join assets on assets.id=workorder.woAsset_id
             where woCauseCode_id={0} and (datecreated between '{1}' and '{2}')
             and assets.assetIsLocatedAt_id={3}""".format(c.id,start,end,loc))[0].id
        return d
    #EM
    @staticmethod
    def getEmCount(start,end):
        return WorkOrder.objects.raw("select COALESCE(count(id),0) as id from workorder where datecreated between '{0}' and '{1}' and isem=1".format(start,end))[0].id
    @staticmethod
    def getEmCount2(start,end,loc):
        return WorkOrder.objects.raw("""select COALESCE(count(workorder.id),0) as id from workorder
        inner join assets on assets.id=workorder.woAsset_id
        where (datecreated between '{0}' and '{1}') and isem=1 and assets.assetIsLocatedAt_id={2}""".format(start,end,loc))[0].id
    #EM
    @staticmethod
    def getEms(start,end,loc=None):
        if(not loc):
            return WorkOrder.objects.filter(isScheduling=False,visibile=True,datecreated__range=[start,end],isEM=1)
        else:
            return WorkOrder.objects.filter(woAsset__assetIsLocatedAt__id=loc, isScheduling=False,visibile=True,datecreated__range=[start,end],isEM=1)

    #TAviz Change spare part
    @staticmethod
    def getTaviz(start,end,loc=None):
        if(not loc):
            return WorkOrder.objects.filter(isScheduling=False,visibile=True,id__in=(WorkorderPart.objects.filter(woPartWorkorder__datecreated__range=[start,end],woPartActulaQnty__gt=0).values_list('woPartWorkorder',flat=True))).order_by('-datecreated','-timecreated')
        else:
            return WorkOrder.objects.filter(woAsset__assetIsLocatedAt__id=loc, isScheduling=False,visibile=True,id__in=(WorkorderPart.objects.filter(woPartWorkorder__datecreated__range=[start,end],woPartActulaQnty__gt=0).values_list('woPartWorkorder',flat=True))).order_by('-datecreated','-timecreated')

    # @staticmethod
    # def getTaviz(start,end,loc):
    #     return WorkOrder.objects.filter(isScheduling=False,visibile=True,id__in=(WorkorderPart.objects.filter(woPartWorkorder__datecreated__range=[start,end]).values_list('woPartWorkorder',flat=True)))
    @staticmethod
    def getTavaghof(start,end,loc):
        if(loc is None):
            # return WorkOrder.objects.filter(isScheduling=False,visibile=True,datecreated__range=[start,end]).exclude(Q(woStopCode__isnull=True)|Q(woStopCode__id=15))
            return AssetLife.objects.filter(assetOfflineFrom__range=(start,end)).exclude(Q(assetStopCode__isnull=True)|Q(assetStopCode__id=15))
        else:
            # return WorkOrder.objects.filter(woAsset__assetIsLocatedAt__id=loc, isScheduling=False,visibile=True,datecreated__range=[start,end]).exclude(Q(woStopCode__isnull=True)|Q(woStopCode__id=15))
            return AssetLife.objects.filter(assetOfflineFrom__range=(start,end)).filter(Q(assetLifeAssetid__assetIsLocatedAt__id=loc)|Q(assetLifeAssetid__id=loc)).exclude(Q(assetStopCode__isnull=True)|Q(assetStopCode__id=15))
    @staticmethod
    def getNewWO(start,end):
        return WorkOrder.objects.filter(isScheduling=False,visibile=True,datecreated__range=[start,end],woStatus=1)
    @staticmethod
    def copy(ids,assetlist,request):
        print("kire khar")
        with transaction.atomic():
            kl=ids
            print(kl,'k1')
            print(assetlist)
             ##### Create Wo #########
            for assets in assetlist:
                    Ast=Asset.objects.get(id=assets)
                    stableWo=WorkOrder.objects.get(id=kl)
                    oldWo=WorkOrder.objects.get(id=kl)
                    stableWo.pk=None
                    stableWo.visibile=True
                    stableWo.woAsset=Ast


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
                        wn=WorkorderUserNotification.objects.filter(woNotifWorkorder=oldWo)
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
                        object_repr     = 'دستور کار موردی',
                        action_flag     = CHANGE,
                        change_message= request.META.get('REMOTE_ADDR')
                    )
    @staticmethod
    def log(request,form,id):
        if(id):
            LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(form.instance).pk,
                object_id       = form.instance.id,
                object_repr     = 'دستور کار موردی',
                action_flag     = CHANGE,
                change_message= request.META.get('REMOTE_ADDR')
            )
        else:
            LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(form.instance).pk,
                object_id       = form.instance.id,
                object_repr     = 'دستور کار موردی',
                action_flag     = ADDITION,
                change_message= request.META.get('REMOTE_ADDR')
            )
    @staticmethod
    def manageStopCode(request,form):
        if(form.instance.woStopCode):
            try:
                assetlife=AssetLife.objects.none()
                if(iscreated==1):
                    if(form.instance.woStopCode.stopCode):
                        # print("here")
                        AssetUtility.createNewAssetStatus(form.instance)
                else:
                        # print("update")
                        AssetUtility.updateAssetLife(form.instance)
            except AssetLife.DoesNotExist:
                print("error")

            except Exception as e:
                print(e)
    @staticmethod
    def refreshView(request):
            books=[]
            if(request.user.username!="admin" and not request.user.groups.filter(name='operator').exists()):
                books = WorkOrder.objects.filter(isScheduling=False,visibile=True).filter(Q(RequestedUser__userId=request.user)|Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')

            else:
                books = WorkOrder.objects.filter(isScheduling=False).filter(visibile=True).order_by('-datecreated','-timecreated')
            return books

    @staticmethod
    def download_csv(request, queryset):
        opts = queryset.model._meta
        model = queryset.model
        response = HttpResponse(content='text/csv')
        # force download.
        response['Content-Disposition'] = 'attachment;filename=export.csv'
        response.write(codecs.BOM_UTF8)
        # the csv writer
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
        download_csv.short_description = "Download selected as csv"

    @staticmethod
    def create_task_when_wo_created(request,form):

        wo=form.instance
        data=dict()
        if(wo.CompleteUserTask.all().count()==0):
            to=Tasks.objects.create(workOrder=wo,taskTypes=1,taskDescription=wo.summaryofIssue,taskAssignedToUser=wo.assignedToUser,taskStartDate=wo.datecreated,taskStartTime=wo.timecreated,taskTimeEstimate=0.1)
            data = render_to_string('cmms/tasks/partialTaskList.html', {
                'task': wo.CompleteUserTask.all(),
                'perms': PermWrapper(request.user),
                'ispm':False
            })
        return data
    @staticmethod
    def create_task_when_wo_created_fromAPI(request,woid):

        wo=WorkOrder.object.get(id=woid)

        data=dict()
        if(wo.CompleteUserTask.all().count()==0):
            to=Tasks.objects.create(workOrder=wo,taskTypes=1,taskDescription=wo.summaryofIssue,taskAssignedToUser=wo.assignedToUser,taskStartDate=wo.datecreated,taskStartTime=wo.timecreated,taskTimeEstimate=0.1)

        return True
    @staticmethod
    def create_notification(request,woid):

        wo=WorkOrder.object.get(id=woid)
        asset_user=AssetUser.objects.filter(AssetUserAssetId=wo.woAsset)
        for i in asset_user:
            WorkorderUserNotification.objects.create(woNotifWorkorder=wo,woNotifUser=i.AssetUserUserId)


        return True
