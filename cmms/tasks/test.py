from __future__ import absolute_import, unicode_literals
from cmms.models import *
from celery.task.schedules import crontab
from celery import task
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime
from datetime import timedelta,date,time
from dateutil.relativedelta import *
import sys
import locale

logger = get_task_logger(__name__)


@periodic_task(
    queue='queue1',
    run_every=(crontab(minute='*')),
    name="hourlyWork",
    ignore_result=True
)
def createWO_celery3():
        #SELECT * FROM schedule INNER JOIN workorder ON schedule.workOrder_id=workorder.id
        #WHERE workorder.running=1 and nexttime=currenttime')


        logger.info("create Hourly object")
        dt_start=datetime.now()
        dt_time=datetime.now().time()
        dt_t2=datetime.combine(dt_start, time(dt_time.hour,0))
        dt_t3=dt_t2+timedelta(hours=1)
        todoes=Schedule.objects.filter(schnextTime__gte=dt_t2).filter(schnextTime__lt=dt_t3).filter(schChoices=0).filter(schHowOften=1)
        try:
            for sch in todoes:
                if(sch.schNextWo.visibile==False and sch.workOrder.running==True and sch.schChoices==0):
                    h=0
                    d=0
                    m=0
                    y=0

                    sch.schNextWo.visibile=True
                    sch.schNextWo.save()
                    #####how to find next date

                    if(sch.schHowOften==1):
                        d=sch.schHourRep
                        sch.schnextTime=sch.schnextTime+timedelta(hours=d)











                    #sch.schnextTime=datetime.combine(sch.schnextTime,datetime.now().time())+timedelta(days=sch.schDailyRep)
                    #sch.schnextTime=sch.schnextTime+timedelta(days=sch.schDailyRep)
                    stableWo=WorkOrder.objects.get(id=sch.workOrder_id)
                    oldWo=WorkOrder.objects.get(id=sch.workOrder_id)
                    stableWo.pk=None
                    stableWo.datecreated=sch.schnextTime.date()
                    stableWo.timecreated=sch.schnextTime.time()
                    stableWo.visibile=False
                    stableWo.isScheduling=False
                    stableWo.isPm=True
                    stableWo.isPartOf=sch.workOrder
                    stableWo.save()
                    sch.schNextWo=stableWo
                    sch.save()
                    #######Copy Tasks#########
                    # wt=WorkorderTask.objects.filter(workorder=oldWo)
                    wt=Tasks.objects.filter(workorder=oldWo)
                    if(wt!=None):
                        for f in wt:
                            f.pk=None
                            f.workorder=stableWo
                            f.save()
                    #######Copy Parts#######
                    wp=WorkorderPart.objects.filter(woPartWorkorder=oldWo)
                    if(wp!=None):
                        for f in wp:
                            f.pk=None
                            #اگر مجودی نبود باید تغییر وضعیت بدهد به منتظر قطعه
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
           logger.info(e)
           exc_type, exc_obj, tb = sys.exc_info()

           logger.info(tb.tb_lineno)
           logger.info("form not saved")






@periodic_task(
    queue='queue2',
    run_every=(crontab(hour="*", minute=1)),
    name="somthing",
    ignore_result=True
)
def createWO_celery2():
        #SELECT * FROM schedule INNER JOIN workorder ON schedule.workOrder_id=workorder.id
        #WHERE workorder.running=1 and nexttime=currenttime')


        logger.info("create object")
        todoes=Schedule.objects.filter(schnextTime__contains=datetime.now().date())
        try:
            for sch in todoes:
                if(sch.schNextWo.visibile==False and sch.workOrder.running==True and sch.schChoices==0):
                    h=0
                    d=0
                    m=0
                    y=0

                    sch.schNextWo.visibile=True
                    sch.schNextWo.save()
                    #####how to find next date

                    if(sch.schHowOften==2):
                        d=sch.schDailyRep
                        sch.schnextTime=sch.schnextTime+timedelta(d)
                    elif(sch.schHowOften==3):
                        logger.info("here")
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
                        cd=jdatetime.date(cd.year,((cd.month+sch.schMonthlyRep)%13)+1,sch.schDayofMonthlyRep)
                        # while cd.day!=sch.schDayofMonthlyRep:
                        #     cd+=timedelta(1)

                        # if(cd.month==t1.month):
                        #         cd=jdatetime.date(cd.year,((cd.month+sch.schMonthlyRep)%13)+1,sch.schDayofMonthlyRep)
                        # else:
                        #     cd=jdatetime.date(cd.year,((cd.month+sch.schMonthlyRep-1)%13)+1,cd.day)
                        #         #ss+=relativedelta(months=+sch.schMonthlyRep-1)
                        logger.info(cd)
                        sch.schnextTime=cd.togregorian()
                    elif(sch.schHowOften==5):
                        cd=jdatetime.date.fromgregorian(date=datetime.now())
                        cd=jdatetime.date(cd.year+sch.schMonthOfYearRep,sch.schMonthOfYearRep,sch.schDayOfMonthOfYearRep)
                        sch.schnextTime=cd.togregorian()










                    #sch.schnextTime=datetime.combine(sch.schnextTime,datetime.now().time())+timedelta(days=sch.schDailyRep)
                    #sch.schnextTime=sch.schnextTime+timedelta(days=sch.schDailyRep)
                    stableWo=WorkOrder.objects.get(id=sch.workOrder_id)
                    oldWo=WorkOrder.objects.get(id=sch.workOrder_id)
                    stableWo.pk=None
                    stableWo.datecreated=sch.schnextTime.date()
                    stableWo.timecreated=sch.schnextTime.time()
                    stableWo.visibile=False
                    stableWo.isScheduling=False
                    stableWo.isPartOf=sch.workOrder
                    stableWo.save()
                    sch.schNextWo=stableWo
                    sch.save()
                    #######Copy Tasks#########
                    #wt=WorkorderTask.objects.filter(workorder=oldWo)
                    wt=Tasks.objects.filter(workorder=oldWo)
                    if(wt!=None):
                        for f in wt:
                            f.pk=None
                            f.workorder=stableWo
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
           logger.info(e)
           exc_type, exc_obj, tb = sys.exc_info()

           logger.info(tb.tb_lineno)
           logger.info("form not saved")

#################################
# @periodic_task(
#     queue='queue2',
#     run_every=(crontab(hour="*", minute=1)),
#     name="somthing",
#     ignore_result=True
# )
# def test_celery2():
#         #SELECT * FROM schedule INNER JOIN workorder ON schedule.workOrder_id=workorder.id
#         #WHERE workorder.running=1 and nexttime=currenttime')
#
#
#         logger.info("create object")
