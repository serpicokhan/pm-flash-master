# Create your tasks here

from celery import shared_task
from cmms.models import *
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION

# from celery.task.schedules import crontab
from celery.schedules import crontab
# from celery import task
# from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime
from datetime import timedelta,date,time
from dateutil.relativedelta import *
import sys
import locale

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

def createWO_celery23():

        print("1")
@shared_task
def createWO_celery2():

        print("1")
        #SELECT * FROM schedule INNER JOIN workorder ON schedule.workOrder_id=workorder.id
        #WHERE workorder.running=1 and nexttime=currenttime')


        # logger.info("create object")
        todoes=Schedule.objects.filter(schnextTime__contains=datetime.now().date(),schnextTime__hour=datetime.now().hour)
        try:
            for sch in todoes:
                if(sch.schNextWo.visibile==False and sch.workOrder.running==True and sch.schChoices==0):
                    print("wo",sch.schNextWo)
                    print("current nexttime",sch.schnextTime)
                    # LogEntry.objects.log_action(
                    # user_id         = 1,
                    # content_type_id = sch.schChoices,
                    # object_id       = sch.schNextWo.id,
                    # object_repr     = 'celery',
                    # action_flag     = ADDITION,
                    # change_message= sch.schNextWo.summaryofIssue
                    # )
                    h=0
                    d=0
                    m=0
                    y=0
                    nxt_wo=WorkOrder.objects.get(id=sch.schNextWo.id)
                    nxt_wo.visibile=True
                    nxt_wo.save()
                    #####how to find next date

                    if(sch.schHowOften==1):
                        d=sch.schHourRep
                        sch.schnextTime=sch.schnextTime+timedelta(hours=d)
                    elif(sch.schHowOften==2):
                        d=sch.schDailyRep
                        sch.schnextTime=sch.schnextTime+timedelta(d)
                    elif(sch.schHowOften==3):
                        # logger.info("here")
                        cd=datetime.now()
                        if(sch.isSunday==True):
                            while cd.weekday()!=6:
                                cd+=timedelta(1)
                            if(cd.isocalendar()[1]==date.today().isocalendar()[1]):
                                cd+=timedelta((sch.schWeeklyRep)*7)
                            else:
                                cd+=timedelta((sch.schWeeklyRep-1)*7)
                            sch.schnextTime=cd



                        elif(sch.isMonday==True):
                            while cd.weekday()!=0:
                                cd+=timedelta(1)
                            if(cd.isocalendar()[1]==date.today().isocalendar()[1]):
                                cd+=timedelta((sch.schWeeklyRep)*7)
                            else:
                                cd+=timedelta((sch.schWeeklyRep-1)*7)
                            sch.schnextTime=cd
                        elif(sch.isTuesday==True):
                            while cd.weekday()!=1:
                                cd+=timedelta(1)
                            if(cd.isocalendar()[1]==date.today().isocalendar()[1]):
                                cd+=timedelta((sch.schWeeklyRep)*7)
                            else:
                                cd+=timedelta((sch.schWeeklyRep-1)*7)
                            sch.schnextTime=cd
                        elif(sch.isWednenday==True):
                            while cd.weekday()!=2:
                                cd+=timedelta(1)
                            if(cd.isocalendar()[1]==date.today().isocalendar()[1]):
                                cd+=timedelta((sch.schWeeklyRep)*7)
                            else:
                                cd+=timedelta((sch.schWeeklyRep-1)*7)
                            sch.schnextTime=cd
                        elif(sch.isThursday==True):
                            while cd.weekday()!=3:
                                cd+=timedelta(1)
                            if(cb.isocalendar()[1]==date.today().isocalendar()[1]):
                                cd+=timedelta((sch.schWeeklyRep)*7)
                            else:
                                cd+=timedelta((sch.schWeeklyRep-1)*7)
                            sch.schnextTime=cd
                        elif(sch.isFriday==True):
                            while cd.weekday()!=4:
                                cd+=timedelta(1)
                            if(cd.isocalendar()[1]==date.today().isocalendar()[1]):
                                cd+=timedelta((sch.schWeeklyRep)*7)
                            else:
                                cd+=timedelta((sch.schWeeklyRep-1)*7)
                            sch.schnextTime=cd
                        elif(sch.isSaturday==True):
                            while cd.weekday()!=5:
                                cd+=timedelta(1)
                            if(cd.isocalendar()[1]==date.today().isocalendar()[1]):
                                cd+=timedelta((sch.schWeeklyRep)*7)
                            else:
                                cd+=timedelta((sch.schWeeklyRep-1)*7)
                            sch.schnextTime=cd
                    elif(sch.schHowOften==4):
                        cd=jdatetime.date.fromgregorian(date=datetime.now())#datetime.now()
                        # t1=jdatetime.date.fromgregorian(date=datetime.now())
                        cd=jdatetime.date(cd.year,cd.month+sch.schMonthlyRep,sch.schDayofMonthlyRep)
                        z=datetime.combine(cd.togregorian(),datetime.strptime("{}0".format(sch.schnextTime.hour),"%H%M").time())
                        print("z:",z)
                        # while cd.day!=sch.schDayofMonthlyRep:
                        #     cd+=timedelta(1)

                        # if(cd.month==t1.month):
                        #         cd=jdatetime.date(cd.year,((cd.month+sch.schMonthlyRep)%13)+1,sch.schDayofMonthlyRep)
                        # else:
                        #     cd=jdatetime.date(cd.year,((cd.month+sch.schMonthlyRep-1)%13)+1,cd.day)
                        #         #ss+=relativedelta(months=+sch.schMonthlyRep-1)
                        # logger.info(cd)
                        sch.schnextTime=z
                    elif(sch.schHowOften==5):
                        cd=jdatetime.date.fromgregorian(date=datetime.now())
                        cd=jdatetime.date(cd.year+sch.schMonthOfYearRep,sch.schMonthOfYearRep,sch.schDayOfMonthOfYearRep)
                        sch.schnextTime=cd.togregorian()
#
#
#
#
#
#
#
#
#

                    #sch.schnextTime=datetime.combine(sch.schnextTime,datetime.now().time())+timedelta(days=sch.schDailyRep)
                    #sch.schnextTime=sch.schnextTime+timedelta(days=sch.schDailyRep)
                    stableWo=WorkOrder.objects.get(id=sch.workOrder_id)
                    oldWo=WorkOrder.objects.get(id=sch.workOrder_id)
                    stableWo.pk=None
                    stableWo.datecreated=sch.schnextTime.date()
                    stableWo.timecreated=sch.schnextTime.time()
                    # stableWo.datecreated=datetime.now().date()
                    stableWo.requiredCompletionDate=stableWo.datecreated+timedelta(stableWo.estimatedCompilation)
                    # stableWo.timecreated=datetime.now().time()
                    stableWo.visibile=False
                    stableWo.isScheduling=False
                    stableWo.isPartOf=sch.workOrder
                    stableWo.save()
                    sch.schNextWo=stableWo
                    sch.save()
                    #######Copy Tasks#########
                    #wt=WorkorderTask.objects.filter(workorder=oldWo)
                    wt=Tasks.objects.filter(workOrder=oldWo)
                    if(wt!=None):
                        for f in wt:
                            f.pk=None
                            f.workOrder=stableWo
                            f.save()
                    #######Copy Parts#######
                    wp=WorkorderPart.objects.filter(woPartWorkorder=oldWo)
                    if(wp!=None):
                        for f in wp:
                            f.pk=None
                            f.woPartWorkorder=stableWo
                            f.save()
                    else:
                        print("no Parts")

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
                    except:
                        print("error")

        except Exception as e:
           print(e)
           exc_type, exc_obj, tb = sys.exc_info()

           print(tb.tb_lineno)
           print("form not saved")
@shared_task
def send_email_report():
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    wos=Schedule.objects.all()
    for i in wos:
        print(i.schNextWo)
        print(i.schnextTime)
    LogEntry.objects.log_action(
        user_id         = 1,
        content_type_id = 1,
        object_id       = 1,
        object_repr     = 'celery',
        action_flag     = ADDITION,
        change_message= '1221'
    )
