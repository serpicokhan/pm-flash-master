from cmms.models import SysUser,WorkOrder,Attendance,Tasks
import jdatetime
import datetime
from datetime import  timedelta
from django.core.paginator import *
from django.db.models import Q

class UserUtility:


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
    def getOveralView(userID,start,end):
        if(userID):
            # print(" select get_closed_wo_byuser({0},'{1}','{2}') 
            #as id,get_assoc_wo_byuser({0},'{1}','{2}') as assoc ,
            #get_logged_labour_hour_byuser({0},'{1}','{2}') as  logged from workorder where datecreated between '{1}' and '{2}' limit 1".format(userID,start,end))
            return WorkOrder.objects.raw(" select get_closed_wo_byuser({0},'{1}','{2}') as id,get_assoc_wo_byuser({0},'{1}','{2}') as assoc ,get_logged_labour_hour_byuser({0},'{1}','{2}') as  logged from workorder inner join tasks on tasks.workorder_id=workorder.id  where tasks.taskStartDate between '{1}' and '{2}' limit 1".format(userID,start,end))
            # wos=Tasks.objects.filter(taskAssignedToUser__id=userID).values('workOrder')
            # n1=WorkOrder.objects.filter(datecreated__range=[start,end]).filter(Q(id__in=wos)|Q(assignedToUser=userID)).count()
            # tasks=Tasks.objects.filter(workOrder__in=WorkOrder.objects.filter(datecreated__range=[start,end],id__in=wos))
            # total_duration = timedelta()
            # for task in tasks:
            #     if task.taskDateCompleted and task.taskTimeCompleted and task.taskStartDate and task.taskStartTime:
            #         # Combine the start date and time into a single datetime object
            #         start_datetime = datetime.datetime.combine(task.taskStartDate, task.taskStartTime)
            #         # Combine the completion date and time into a single datetime object
            #         end_datetime = datetime.datetime.combine(task.taskDateCompleted, task.taskTimeCompleted)
            #         # Calculate the duration for this task
            #         duration = end_datetime - start_datetime
            #         total_duration += duration
            # n2=WorkOrder.objects.filter(datecreated__range=[start,end],woStatus=7).filter(Q(id__in=wos)|Q(assignedToUser=userID)).count()
            # n3=total_duration
            # return n1,n2,n3
        if(unitId):

            return SysUser.objects.raw(" select get_closed_wo_unit({0},'{1}','{2}'),get_assoc_wo_unit({0},'{1}','{2}'),get_logged_labour_hour_unit({0},'{1}','{2}')".format(unitID,start,end))
    @staticmethod
    def getDetailWoView(userID,start,end):
        if(userID):
            
            # print(" select distinct(workorder.id) as id , get_labour_hour_wo({0},workorder.id) as hour from workorder inner join tasks on tasks.workorder_id=workorder.id where datecreated between '{1}' and '{2}' and (tasks.taskAssignedToUser_id={0})".format(userID,start,end))
            # prin
            return WorkOrder.objects.raw(""" select (workorder.id) as id , 
                            COALESCE(get_labour_hour_wo({0},workorder.id),0) /60
                            as hour from workorder inner join tasks on
                            tasks.workorder_id=workorder.id where
                            tasks.taskStartDate between '{1}' and '{2}'
                            and (tasks.taskAssignedToUser_id={0} or workorder.assignedToUser_id={0})  
                            and visibile=1""".format(userID,start,end))

    @staticmethod
    def getHozurTimeGid(dt1,dt2,gid):
        n1=Attendance.objects.raw("select get_unint_member_attendance({0},'{1}','{2}') as id".format(gid,dt1,dt2))[0].id
        return n1
    @staticmethod
    def getHozurTimeGid2(dt1,dt2,gid,loc):
        n1=Attendance.objects.raw("select get_unint_member_attendance2({0},'{1}','{2}',{3}) as id".format(gid,dt1,dt2,loc))[0].id
        return n1
    @staticmethod
    def getHozurTimeUser(dt1,dt2,uid):

        n1=Attendance.objects.raw("select sum(attendanceTime+ezafekar) as id from attendance where name_id ={0} and (datecreated between '{1}' and '{2}')".format(uid,dt1,dt2))
        return n1
    @staticmethod
    def getuser_work_hour_mtype(dt1,dt2,uid):
        return SysUser.objects.raw("""    select COALESCE( sum(timestampdiff(minute,cast(concat(taskStartDate,
         ' ', taskStartTime) as datetime),cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0)
          as id , m.name as name,m.id from tasks
                 inner JOIN sysusers on tasks.taskAssignedToUser_id=sysusers.id

                 inner JOIN workorder on tasks.workOrder_id=workorder.id
                 inner join maintenancetype as m on workorder.maintenanceType_id=m.id

                 where
                 tasks.taskDateCompleted between '{1}' and '{2}' and workorder.assignedToUser_id={0}
                 and workorder.isScheduling=0 and workorder.visibile=1
                 group by m.id """.format(uid,dt1,dt2))
    @staticmethod
    def is_manager(uid):
        user1=SysUser.objects.get(userId=uid)
        return (user1.userId.groups.filter(name= 'manager').exists())
