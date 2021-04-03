from cmms.models import SysUser,WorkOrder,Attendance
import jdatetime
import datetime
from django.core.paginator import *
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
            print(" select get_closed_wo_byuser({0},'{1}','{2}') as id,get_assoc_wo_byuser({0},'{1}','{2}') as assoc ,get_logged_labour_hour_byuser({0},'{1}','{2}') as  logged from workorder where datecreated between '{1}' and '{2}' limit 1".format(userID,start,end))
            return WorkOrder.objects.raw(" select get_closed_wo_byuser({0},'{1}','{2}') as id,get_assoc_wo_byuser({0},'{1}','{2}') as assoc ,get_logged_labour_hour_byuser({0},'{1}','{2}') as  logged from workorder where datecreated between '{1}' and '{2}' limit 1".format(userID,start,end))
        if(unitId):

            return SysUser.objects.raw(" select get_closed_wo_unit({0},'{1}','{2}'),get_assoc_wo_unit({0},'{1}','{2}'),get_logged_labour_hour_unit({0},'{1}','{2}')".format(unitID,start,end))
    @staticmethod
    def getDetailWoView(userID,start,end):
        if(userID):
            return WorkOrder.objects.raw(" select distinct(workorder.id) as id , get_labour_hour_wo({0},workorder.id) as hour from workorder inner join tasks on tasks.workorder_id=workorder.id where datecreated between '{1}' and '{2}' and (tasks.taskAssignedToUser_id={0})".format(userID,start,end))
    @staticmethod
    def getHozurTimeGid(dt1,dt2,gid):
        n1=Attendance.objects.raw("select get_unint_member_attendance({0},'{1}','{2}') as id".format(gid,dt1,dt2))[0].id
        return n1
