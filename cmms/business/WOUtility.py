from cmms.models import WorkOrder,Project,SysUser
import jdatetime
import datetime

# from datetime import datetime
from django.core.paginator import *
from cmms.business.misccost import *
from cmms.business.taskUtility import *
from cmms.business.PartUtility import  *
from cmms.business.EquipCostSettingUtility import *
from decimal import Decimal
from cmms.utils import *
from django.db.models import Q
import locale
class WOUtility:

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
    #GET Wo on demand completed between 2 dates
    @staticmethod
    def GetCompletedWorkOrderNum(start,end,isScheduling):
        #print("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and isPartOf_id {2} and isScheduling=0".format(start,end,isScheduling))
        return WorkOrder.objects.raw("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and isPartOf_id {2} and isScheduling=0".format(start,end,isScheduling))
    #########################################################################################
    @staticmethod
    def GetOnTimeCompletedWorkOrderNum(start,end,isScheduling):

        return WorkOrder.objects.raw("select count(id) as id from workorder where datecompleted <= requiredCompletionDate and (datecompleted between '{0}' and '{1}') and  wostatus=7 and isPartOf_id {2}".format(start,end,isScheduling))

    #########################################################################################
    @staticmethod
    def GetTotalCompletedWorkOrderNum(start,end):
        return WorkOrder.objects.raw("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and isScheduling=0".format(start,end))


    #########################################################################################
    @staticmethod
    def GetTotalOnTimeCompletedWorkOrderNum(start,end):
        return WorkOrder.objects.raw("select count(id) as id from workorder where datecompleted <requiredCompletionDate and (datecompleted between '{0}' and '{1}') and  wostatus=7 and isScheduling=0".format(start,end))
    #########################################################################################
    @staticmethod
    def getWoReqNum(start,end):

        return WorkOrder.objects.raw("SELECT  count(id) as id  from workorder where datecreated between '{0}' and '{1}' and isScheduling=0".format(start,end))
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
    def getResources(start,end):
        return WorkOrder.objects.raw("""SELECT fullname as id,format((ontime*100.0/totalCompleted),0) as p1,format(hour,1) as hour,total,format(totalcompleted*100/total,2) as t2,format(totalcompleted,0) as totalcompleted
                                        FROM ( SELECT count(id) as ontime, workorder.assignedToUser_id as u1
                                               FROM workorder

                                               where workorder.datecreated between '{0}' and '{1}' and workorder.wostatus=7 and workorder.datecompleted <=workorder.requiredCompletionDate
                                             group by (u1)) AS A
                                        JOIN ( SELECT count(id) as totalCompleted, workorder.assignedToUser_id as u2
                                               FROM workorder

                                               where workorder.datecreated between '{0}' and '{1}' and workorder.wostatus=7 group by (u2)) AS B

                                        ON A.u1=B.u2

                                        left join (SELECT sum(TIMESTAMPDIFF(HOUR, cast(concat(taskStartDate, ' ', taskStartTime)
                                         as datetime),cast(concat(taskDateCompleted, ' ',
                                          taskTimeCompleted) as datetime))) as hour,taskAssignedToUser_id as u3 FROM `tasks` group by taskAssignedToUser_id) as C
                                        on A.u1=C.u3
                                        left join(select count(id) as total ,workorder.assignedToUser_id as u3 from workorder where workorder.datecreated between '{0}' and '{1}'
                                        group by u3) as D
                                        on A.u1=D.u3
                                        left join sysusers on A.u1=sysusers.id
                                        """.format(start,end))
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
        return WorkOrder.objects.raw(""" select * from workorder where (woStatus IN (1,2,4,5,6,9) or woStatus is NULL ) and datecreated between '{0}' and '{1}'  and isScheduling=0 and  isPartOf_id is not null and ((curdate()>requiredCompletionDate and dateCompleted is null) or (datecompleted> requiredCompletionDate))""".format(start,end))

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

        n1 = WorkOrder.objects.filter(woPriority__in=(1,2),isScheduling=False, datecreated__range=(start, end),woStatus__in=(1,4,5,6,9)).count()
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
        return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=False).filter(summaryofIssue__contains=searchStr,visibile=True).order_by('-id')

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
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)

        if(len(priority)>0):
            whereConition+=" and  woPriority in {0}".format(priority)

        print("""select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate,
        cast(concat(dateCompleted, ' ', timeCompleted) as datetime) as t5,
        cast(concat(requiredCompletionDate, ' ', requiredCompletionTime) as datetime) as t6


        from workorder
        left join maintenancetype b on workorder.maintenancetype_id=b.id
        left join assets a on workorder.woasset_id=a.id
        {0}
        having t6<t5

         order by workorder.id
         """.format(whereConition))

        return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate,
        cast(concat(dateCompleted, ' ', timeCompleted) as datetime) as t5,
        cast(concat(requiredCompletionDate, ' ', requiredCompletionTime) as datetime) as t6


        from workorder
        left join maintenancetype b on workorder.maintenancetype_id=b.id
        left join assets a on workorder.woasset_id=a.id
        {0}

        having t6<t5

         order by workorder.id
         """.format(whereConition))
    @staticmethod
    def getOpenWorkOrdersDetailReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        whereConition="where datecreated between '{0}' and '{1}' and wostatus in (1,2,4,5,6,9) and isScheduling=0".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(asset)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)

        if(len(priority)>0):
            whereConition+=" and  woPriority in {0}".format(priority)

        return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id
        inner join assets a on workorder.woasset_id=a.id
        {0} order by workorder.id
         """.format(whereConition))
    @staticmethod
    def getCloseWorkOrdersDetailReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        whereConition="where datecreated between '{0}' and '{1}' and wostatus in (7,8) and isScheduling=0".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(asset)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)

        if(len(priority)>0):
            whereConition+=" and  woPriority in {0}".format(priority)

        return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id
        inner join assets a on workorder.woasset_id=a.id
        {0} order by workorder.id
         """.format(whereConition))
    @staticmethod
    def getAllWorkOrdersDetailReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        whereConition="where datecreated between '{0}' and '{1}'  and isScheduling=0".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(asset)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)

        if(len(priority)>0):
            whereConition+=" and  woPriority in {0}".format(priority)

        return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id
        inner join assets a on workorder.woasset_id=a.id
        {0} order by workorder.id
         """.format(whereConition))
    @staticmethod
    def getRequestedWorkOrdersListReport(start,end,asset,assetCategory,maintenanceType,priority):

        whereConition="where datecreated between '{0}' and '{1}'  and isScheduling=0 and wostatus=1".format(start ,end)

        if(len(asset)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)

        if(len(priority)>0):
            whereConition+=" and  woPriority in {0}".format(priority)

        return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        timestampdiff(day,cast(concat(datecreated, ' ', timecreated) as datetime),NOW()) as t3,pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate,estimatedLabor

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id
        inner join assets a on workorder.woasset_id=a.id
        {0} order by workorder.id
         """.format(whereConition))
    @staticmethod
    def getOpenWorkOrdersListReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        whereConition="where datecreated between '{0}' and '{1}' and wostatus in (1,2,4,5,6,9) and isScheduling=0".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(asset)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)

        if(len(priority)>0):
            whereConition+=" and  woPriority in {0}".format(priority)

        return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate,
        woPriority,estimatedLabor

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id
        inner join assets a on workorder.woasset_id=a.id
        {0} order by workorder.id
         """.format(whereConition))
    @staticmethod
    def getOpenPMWorkOrdersListReport(start,end,assignedUser,asset,assetCategory,maintenanceType,priority):

        whereConition="where datecreated between '{0}' and '{1}' and wostatus in (1,2,4,5,6,9) and isScheduling=0 and isPartOf_id is not null".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(asset)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)

        if(len(priority)>0):
            whereConition+=" and  woPriority in {0}".format(priority)

        return WorkOrder.objects.raw(""" select workorder.id as id, summaryofIssue,woStatus,b.name,pdate(datecreated) as date1, timecreated as time1,
        pdate(requiredCompletionDate) as date2,requiredCompletionTime as time2,
        timestampdiff(day,cast(concat(requiredCompletionDate, ' ', requiredCompletiontime) as datetime),NOW()) as duedate,
        woPriority,estimatedLabor

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id
        inner join assets a on workorder.woasset_id=a.id
        {0} order by workorder.id
         """.format(whereConition))
    @staticmethod
    def getOpenWorkOrderGraphReport(start,end,assignedUser,asset,assetCategory,maintenanceType):

        whereConition="where datecreated between '{0}' and '{1}' and wostatus in (1,2,4,5,6,9) and isScheduling=0 ".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(asset)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)


        print((""" select count(workorder.id) as id, b.name as name ,b.id as k

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id


        {0}
        group by b.name,b.id

        order by workorder.id
         """.format(whereConition)))
        return WorkOrder.objects.raw("""  select count(workorder.id) as id, b.name as name ,b.id as k

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id


        {0}
        group by b.name,b.id

        order by workorder.id
         """.format(whereConition))

    @staticmethod
    def getCloseWorkOrderGraphReport(start,end,assignedUser,asset,assetCategory,maintenanceType):

        whereConition="where datecreated between '{0}' and '{1}' and wostatus in (7,8) and isScheduling=0 ".format(start ,end)
        if(len(assignedUser)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(assignedUser))
        if(len(asset)>0):
            whereConition+=" and  assignedToUser_id in {0}".format(str(asset))
        if(len(assetCategory)>0):
            whereConition+=" and  woAsset_id in {0}".format(str(assetCategory))

        if(len(maintenanceType)>0):
            whereConition+=" and  maintenanceType_id in {0}".format(maintenanceType)


        print((""" select count(workorder.id) as id, b.name as name ,b.id as k

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id


        {0}
        group by b.name,b.id

        order by workorder.id
         """.format(whereConition)))
        return WorkOrder.objects.raw("""  select count(workorder.id) as id, b.name as name ,b.id as k

        from workorder
        inner join maintenancetype b on workorder.maintenancetype_id=b.id


        {0}
        group by b.name,b.id

        order by workorder.id
         """.format(whereConition))
    @staticmethod
    def getProjectsReportWithWorkOrderDetails(start,end,woStatus):

        whereConition="where ProjectActualStartDate >= '{0}' and ProjectActualEndDate <='{1}'  ".format(start ,end)
        if(len(woStatus)>0):
            whereConition+=" and  b.woStatus in {0}".format(str(woStatus))

        print("""  select project.id,projectName, projectDescription as name ,
        ProjectActualStartDate,ProjectActualEndDate,b.woStatus
        from project
        left join workorder b on b.project_id=project.id
        {0}
        order by project.id
         """.format(whereConition))

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
        print(""" select count(id) as tedad,causecode as id,causeDescription
        from workOrder a
        inner join causecode b
        on a.woCauseCode=b.id
        where (a.datecreated between '{0}' and '{1}') and isScheduling=0 {2}
        group by(causecode)
        """.format(start,end,whereConition))
        return WorkOrder.objects.raw(""" select count(wocausecode_id) as tedad,causecode as id,causeDescription
        from workOrder a
        inner join causecode b
        on a.wocausecode_id=b.id
        where (a.datecreated between '{0}' and '{1}') and isScheduling=0 {2}
        group by(causecode)
        """.format(start,end,whereConition))
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
        n1=WorkOrder.objects.filter(woStatus=1,datecreated__range=(start,end),isScheduling=False).count();
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
    def getEmCount(start,end):
        return WorkOrder.objects.raw("select COALESCE(count(id),0) as id from workorder where datecreated between '{0}' and '{1}' and isem=1".format(start,end))[0].id
    #EM
    @staticmethod
    def getEms(start,end):
        return WorkOrder.objects.filter(isScheduling=False,visibile=True,datecreated__range=(start,end),isEM=1)
    #TAviz Change spare part
    @staticmethod
    def getTaviz(start,end):
        return WorkOrder.objects.filter(isScheduling=False,visibile=True,id__in=(WorkorderPart.objects.filter(woPartWorkorder__datecreated__range=(start,end)).values_list('woPartWorkorder',flat=True)))
    @staticmethod
    def getTavaghof(start,end):
        return WorkOrder.objects.filter(isScheduling=False,visibile=True,datecreated__range=(start,end)).exclude(Q(woStopCode__isnull=True)|Q(woStopCode__id=15))
    @staticmethod
    def getNewWO(start,end):
        return WorkOrder.objects.filter(isScheduling=False,visibile=True,datecreated__range=(start,end),woStatus=1)
