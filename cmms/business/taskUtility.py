from cmms.models.task import *
from cmms.models.workorder import *
from datetime import datetime
from django.core.paginator import *
class TaskUtility:
    #get cost of a task by human cost between 2 date
    @staticmethod
    def getTotalWorkHour(start,end):
        return Tasks.objects.raw("select sum(t1.taskTimeSpent * t2.hourlyRate) as id from tasks as t1 join sysusers as t2 on t1.taskAssignedToUser_id=t2.id join workorder as t3 on t1.workorder_id=t3.id where t3.datecreated between '{0}' and '{1}'".format(start,end))
        #select sum(DATEDIFF(CONCAT(`taskStartDate`,' ',`taskStarttime`),CONCAT(`taskDateCompleted`,' ',`taskTimeCompleted`)) * t2.hourlyRate) from tasks as t1 join sysuser as t2 on t1.taskAssignedToUser_id=t2.id join workorder as t3 on t1.workorder_id=t3.id where t3.datecreated
    @staticmethod
    def getWorkOrderHour(id):
        #id
        #n1= Tasks.objects.raw("select format(sum(TIMESTAMPDIFF(SECOND,concat(taskstartdate,' ',taskstarttime),concat(taskDateCompleted,' ',tasktimeCompleted))/3600),0) as id from tasks where workorder_id={}".format(id))
        n1= Tasks.objects.raw("select sum(taskTimeSpent) as id from tasks where workorder_id={}".format(id))
        if(n1[0].id):
            return n1[0].id
        return 0
    @staticmethod
    def getTaskHour(start,end):
        #n1= Tasks.objects.raw("select format(sum(TIMESTAMPDIFF(SECOND,concat(taskstartdate,' ',taskstarttime),concat(taskDateCompleted,' ',tasktimeCompleted))/3600),0) as id from tasks where id={}".format(id))
        #n1= Tasks.objects.raw("select sum(taskTimeSpent) as id from tasks where workorder_id={}".format(id))
        diff=end-start
        # print(start)
        # print(end)
        # print(diff.days)
        return diff.total_seconds()/3600
    ###################
    #eq Cost
    @staticmethod
    def getAssetTimeCostByResource(assetId,start,end):
        # print('''select sum(t1.taskTimeSpent * t2.hourlyRate)
        # as id from tasks as t1 join sysusers as t2 on t1.taskAssignedToUser_id=t2.id
        #  join workorder as t3 on t1.workorder_id=t3.id where t3.datecreated between '{0}' and '{1}'  and t3.woasset_id={2}'''.format(start,end,assetId))
        # return Tasks.objects.raw('''select sum(t1.taskTimeSpent * t2.hourlyRate)
        # as id from tasks as t1 join sysusers as t2 on t1.taskAssignedToUser_id=t2.id
        # join workorder as t3 on t1.workorder_id=t3.id where t3.datecreated between '{0}' and '{1}'  and t3.woasset_id={2}'''.format(start,end,assetId))
        return Tasks.objects.raw('''select sum(timediff(cast(concat(t1.taskDateCompleted, ' ',
         t1.taskTimeCompleted) as datetime), cast(concat(t1.taskStartDate, ' ', t1.taskStartTime)
         as datetime)) * t2.hourlyRate) as id from tasks as t1 join sysusers as t2 on t1.taskAssignedToUser_id=t2.id join workorder as t3 on t1.workorder_id=t3.id
        where t3.datecreated between '{0}' and '{1}'  and t3.woasset_id={2}'''.format(start,end,assetId))
    #####################
    #this report is userd in userlist.html user detail part
    @staticmethod
    def getMonthlyWorkHour(uid):
        jdt1=jdatetime.datetime.now()
        jdt2=jdatetime.date(jdt1.year, jdt1.month, 1)
        endDate=datetime.now().date()
        stDate= jdt2.togregorian()
        return Tasks.objects.raw('''select id,sum(TIMESTAMPDIFF(HOUR, cast(concat(t1.taskStartDate, ' ', t1.taskStartTime)
         as datetime),cast(concat(t1.taskDateCompleted, ' ',
          t1.taskTimeCompleted) as datetime))) as k from tasks t1 where taskAssignedToUser_id ={0} and (taskStartDate between '{1}' and '{2}') '''.format(uid,stDate,endDate))
    #####################
        #this report is userd in userlist.html user detail part
    @staticmethod
    def getYearlyWorkHour(uid):
        jdt1=jdatetime.datetime.now()
        jdt2=jdatetime.date(jdt1.year, 1, 1)
        endDate=datetime.now().date()
        stDate= jdt2.togregorian()
        return Tasks.objects.raw('''select id,sum(TIMESTAMPDIFF(HOUR, cast(concat(t1.taskStartDate, ' ', t1.taskStartTime)
         as datetime),cast(concat(t1.taskDateCompleted, ' ',
          t1.taskTimeCompleted) as datetime))) as k from tasks t1  where taskAssignedToUser_id ={0} and (taskStartDate between '{1}' and '{2}') '''.format(uid,stDate,endDate))
    #################################################

    @staticmethod
    #check start < end
    def checkTaskDateRange(taskInstance):
        print("##################")
        print(taskInstance.taskStartDate,taskInstance.taskStartTime)
        dt1=datetime.combine(taskInstance.taskStartDate,taskInstance.taskStartTime)
        print(taskInstance.taskDateCompleted,taskInstance.taskTimeCompleted)
        dt2=datetime.combine(taskInstance.taskDateCompleted,taskInstance.taskTimeCompleted)
        if(dt1<=dt2):
            return 1
        else:
            return -1

    @staticmethod
    def checkTsVsWs(taskInstance):
        return WorkOrder.objects.raw("SELECT ts_vs_ws ({0},'{1}') AS id".format(taskInstance.workOrder.id,datetime.combine(taskInstance.taskStartDate,taskInstance.taskStartTime)))[0].id
    @staticmethod
    def checkTeVsWe(taskInstance):
        return WorkOrder.objects.raw("SELECT ts_vs_ws ({0},'{1}') AS id".format(taskInstance.workOrder.id,datetime.combine(taskInstance.taskDateCompleted,taskInstance.taskTimeCompleted)))[0].id

    @staticmethod
    def taskchecker(validVal,taskInstance):
        validVal[0]=TaskUtility.checkTaskDateRange(taskInstance)
        validVal[1]=TaskUtility.checkTsVsWs(taskInstance)
        validVal[2]=TaskUtility.checkTeVsWe(taskInstance)
        return validVal

    @staticmethod
    def checkErr(*kerr):
        print(kerr)
        err_msg=''
        err_code=0
        if(kerr[0]==-1):
            err_msg='تاریخ شروع فعالیت باید کمتر از تاریخ اتمام باشد'
            err_code=1
        if(kerr[1]==-1):
            err_msg='تاریخ شروع فعالیت بایستی بعد از تاریخ ایجاد دستور کار باشد'
            err_code=1
        if(kerr[2]==-1):
            err_msg='تاریخ اتمام فعالیت باید قبل از تاریخ اتمام دستور کار باشد'
            err_code=1
        return err_code,err_msg
    @staticmethod
    def register(taskgroupid,workorderid):
        #tasks template
        ts=TaskTemplate.objects.filter(taskTemplateTaskGroup=taskgroupid)
        wo=WorkOrder.objects.get(id=workorderid)
        esTime=0
        for c in ts:
            esTime=esTime+c.taskTemplateTimeEstimate
            Tasks.objects.create(taskTypes=c.taskTemplateTypes,taskStartDate=None,taskStartTime=None,taskDateCompleted=None,taskTimeCompleted=None,taskMetrics=c.taskTemplateMetrics,taskDescription=c.taskTemplateDescription,taskTimeEstimate=c.taskTemplateTimeEstimate,workOrder=wo)
        wo.estimatedLabor=esTime
        wo.save()


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
    def getWorkHourByGid(dt1,dt2,gid):
        n1=Tasks.objects.raw("""select floor(COALESCE( sum(timestampdiff(minute,cast(concat(taskStartDate, ' ',
        taskStartTime) as datetime)
        ,cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0)/60) as id from tasks
         inner JOIN usergroups on tasks.taskAssignedToUser_id=usergroups.userUserGroups_id
         inner JOIN workorder on tasks.workOrder_id=workorder.id
         where  usergroups.groupUserGroups_id={0}
         and tasks.taskDateCompleted between '{1}' and '{2}'
         and workorder.isScheduling=0
         ; """.format(gid,dt1,dt2))[0].id
        return n1;
    @staticmethod
    def getGroupMaintenance(dt1,dt2,gid,mid):
        n1=Tasks.objects.raw("""select floor(COALESCE( sum(timestampdiff
                             (minute,cast(concat(taskStartDate, ' ', taskStartTime) as datetime)
                             ,cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0)/60)
                              as id from tasks
         inner JOIN sysusers on tasks.taskAssignedToUser_id=sysusers.id
         inner join usergroups on sysusers.id=usergroups.userUserGroups_id
         inner join usergroup on usergroups.groupUserGroups_id=usergroup.id
         inner JOIN workorder on tasks.workOrder_id=workorder.id
         inner join assets on workorder.woAsset_id=assets.id

         where  workorder.maintenancetype_id={3} and usergroup.id={0}
         and tasks.taskDateCompleted between '{1}' and '{2}'
          and workorder.isScheduling=0
         ;
         ; """.format(gid,dt1,dt2,mid))[0].id
        return n1;
