import jdatetime
import datetime
from datetime import datetime  as mydt1

from datetime import timedelta,date,timezone
import pytz
from django.shortcuts import get_list_or_404, get_object_or_404
from django.forms.models import model_to_dict
from dateutil.relativedelta import *

import sys
from cmms.models import WorkOrder,Schedule,WorkorderTask,WorkorderFile,WorkorderPart,WorkorderUserNotification,Tasks
class ScheduleUtility:
    @staticmethod
    # make new work order accoring to it's schedule
    def CreateNewWO(schId):
        try:
            Newsch=Schedule.objects.get(pk=schId)
            print("line 17 scheutil next wo:",Newsch.schNextWo)
            # while(True):
            #     pass

            schIsNewFlag=True

            if(Newsch.schChoices==0):
                if(Newsch.schNextWo is None):
                    print("line 20 sch schenext is noen")
                    stableWo=WorkOrder.objects.get(id=Newsch.workOrder_id)
                    # print("line 20 sch_utility",stableWo)
                    stableWo.pk=None
                    print("line 20 sch_utility",stableWo)
                else:
                    stableWo=Newsch.schNextWo
                    schIsNewFlag=False
                oldWo=WorkOrder.objects.get(id=Newsch.workOrder_id)
                s=Newsch.schTriggerTime
                if(Newsch.schHowOften==1):
                    # d=Newsch.schHourRep
                    d=0#از همین ساعت شروع شود
                    if(Newsch.schCreateOnStartDate):
                    # print(s,"!!!!!!!!!!!!!")
                        xxx=mydt1.now()
                        next_t=mydt1(year=Newsch.shStartDate.year,month=Newsch.shStartDate.month,day=Newsch.shStartDate.day,hour=s,minute=0,second=0)+timedelta(hours=d)
                        print(next_t,"   !!nextt")
                        if(next_t>=xxx):
                            print("!")
                            Newsch.schnextTime=mydt1(year=Newsch.shStartDate.year,month=Newsch.shStartDate.month,day=Newsch.shStartDate.day,hour=s,minute=0,second=0)+timedelta(hours=d)
                        else:

                            Newsch.schnextTime=mydt1(year=xxx.year,month=xxx.month,day=xxx.day,hour=xxx.hour,minute=0,second=0)+timedelta(hours=Newsch.schHourRep)
                            print("2",Newsch.schnextTime)

                    else:
                        xxx=mydt1.now()
                        sch_must_run_at=mydt1(year=xxx.year,month=xxx.month,day=xxx.day,hour=s,minute=0,second=0)
                        if(xxx>sch_must_run_at):
                            d=Newsch.schHourRep
                            Newsch.schnextTime=mydt1(year=xxx.year,month=xxx.month,day=xxx.day,hour=s,minute=0,second=0)+timedelta(hours=d)
                        else:
                            d=0
                            Newsch.schnextTime=mydt1(year=xxx.year,month=xxx.month,day=xxx.day,hour=s,minute=0,second=0)+timedelta(hours=d)

                    print(Newsch.schnextTime)
                elif(Newsch.schHowOften==2):
                    d=0
                    # print(Newsch.schCreateOnStartDate)
                    if(not Newsch.schCreateOnStartDate):
                        d=Newsch.schDailyRep
                    Newsch.schnextTime=mydt1(year=Newsch.shStartDate.year,month=Newsch.shStartDate.month,day=Newsch.shStartDate.day,hour=s,minute=0,second=0)+timedelta(d)
                elif(Newsch.schHowOften==3):
                    dtList=[0,0,0,0,0,0,0]
                    cd=mydt1(year=Newsch.shStartDate.year,month=Newsch.shStartDate.month,day=Newsch.shStartDate.day,hour=s,minute=0,second=0)
                    if(Newsch.isSunday==True):
                        print("Sunday: is True")
                        dtList[6]=1

                    if(Newsch.isMonday==True):
                        print("Monday: is True")
                        dtList[0]=1

                    if(Newsch.isTuesday==True):
                        print("Tuesday: is True")
                        dtList[1]=1

                    if(Newsch.isWednenday==True):
                        print("Wendsday: is True")
                        dtList[2]=1

                    if(Newsch.isThursday==True):
                        print("Thursday: is True")
                        dtList[3]=1

                    if(Newsch.isFriday==True):
                        print("Friday: is True")
                        dtList[4]=1

                    if(Newsch.isSaturday==True):
                        print("saturday: is True")
                        dtList[5]=1
                    if(Newsch.schCreateOnStartDate):
                        key1=True
                        while(key1):
                            while(dtList[cd.weekday()]!=1):
                                cd+=timedelta(1)
                            # print(cd.isocalendar()[1],date.today().isocalendar()[1])
                            # if(cd.isocalendar()[1]==date.today().isocalendar()[1]):
                            if(cd>mydt1.now()):
                                    Newsch.schnextTime=cd
                                    key1=False
                            else:
                                    cd+=timedelta(days=1)

                            print(cd)
                    else:
                            cd+=timedelta((Newsch.schWeeklyRep)*7)
                            while(cd.weekday()!=5):
                                cd-=timedelta(1)
                            while(dtList[cd.weekday()]!=1):
                                cd+=timedelta(1)
                            Newsch.schnextTime=cd


                elif(Newsch.schHowOften==4):
                    ddd=mydt1.now()
                    xxx=mydt1(year=Newsch.shStartDate.year,month=Newsch.shStartDate.month,day=Newsch.shStartDate.day,hour=s,minute=0,second=0)
                    # print(Newsch.shStartDate)
                    # print(Newsch.schDayofMonthlyRep,'!!!!!!')
                    cd=jdatetime.date.fromgregorian(day=xxx.day,month=xxx.month,year=xxx.year,hour=s,minute=0,second=0)#datetime.now()
                    t1=jdatetime.date(cd.year,cd.month,Newsch.schDayofMonthlyRep,hour=s,minute=0,second=0)# jdatetime.date.fromgregorian(day=Newsch.schDayofMonthlyRep,month=xxx.month,year=xxx.year)#datetime.now()# t1=jdatetime.date.fromgregorian(date=datetime.now())
                    print("t1,cd",t1,cd)
                    print(t1)
                    # while cd.day!=Newsch.schDayofMonthlyRep:
                    #     cd+=timedelta(1)
                    if(Newsch.schCreateOnStartDate):
                        t3=t1.togregorian()
                        ttt=mydt1(year=t3.year,month=t3.month,day=t3.day,hour=s,minute=0,second=0)
                        if(ttt>=ddd):
                        #
                        #         # kdate=jdatetime.date.fromgregorian(
                        #         # if(cd.month+Newsch.schMonthlyRep>12)
                        #         # cd=jdatetime.date(cd.year,((cd.month+(Newsch.schMonthlyRep)%12),cd.day)
                                xxx=t1.togregorian() #+relativedelta(months=+Newsch.schMonthlyRep)
                        #         print("l1")
                        else:
                            xxx=t1.togregorian()+relativedelta(months=+(Newsch.schMonthlyRep))
                    else:
                        xxx=t1.togregorian()+relativedelta(months=+(Newsch.schMonthlyRep))

                    # print("l2")
                            #ss+=relativedelta(months=+sch.schMonthlyRep-1)

                    z=jdatetime.date.fromgregorian(day=xxx.day,month=xxx.month,year=xxx.year,hour=s,minute=0,second=0)#datetime.now()

                    # time = datetime.time(1, 30)

                    Newsch.schnextTime=mydt1.combine(jdatetime.date(z.year,z.month,Newsch.schDayofMonthlyRep).togregorian(),mydt1.strptime("{}0".format(s),"%H%M").time())


                elif(Newsch.schHowOften==5):
                    xxx=mydt1.now()
                    cd=jdatetime.datetime.fromgregorian(day=xxx.day,month=xxx.month,year=xxx.year)#datetime.now()
                    #cd=jdatetime.date.fromgregorian(date=datetime.now())
                    dt1=jdatetime.datetime(year=cd.year,month=Newsch.schMonthOfYearRep,day=Newsch.schDayOfMonthOfYearRep)
                    xdt=dt1.togregorian()
                    if(Newsch.schCreateOnStartDate):
                        if(dt1<cd.togregorian()):
                            # dt1=jdatetime.date().year,Newsch.schMonthOfYearRep,Newsch.schDayOfMonthOfYearRep)
                            xdt=xdt+relativedelta(years=+Newsch.schYearlyRep)
                        else:
                            xdt=xdt+relativedelta(years=+(Newsch.schYearlyRep-1))
                    else:
                        xdt=xdt+relativedelta(years=+(Newsch.schYearlyRep))
                    Newsch.schnextTime=mydt1.combine(xdt,datetime.time(s,0,0))

                stableWo.datecreated=Newsch.schnextTime.date()
                stableWo.timecreated=Newsch.schnextTime.time()
                stableWo.dateCompleted=None
                if(stableWo.estimatedCompilation):
                    stableWo.requiredCompletionDate=stableWo.datecreated+timedelta(stableWo.estimatedCompilation)
                else:
                    stableWo.requiredCompletionDate=stableWo.datecreated+timedelta(1)

                stableWo.visibile=False
                stableWo.isScheduling=False
                stableWo.isPartOf=Newsch.workOrder
                # Newsch.schNextWo=WorkOrder.objects.create(datecreated=Newsch.schnextTime.date(),timecreated=Newsch.schnextTime.time(),visibile=False,isScheduling=False,isPartOf=Newsch.workOrder)

                stableWo.isPm=True
                stableWo.save()
                print(schIsNewFlag)
                if(schIsNewFlag):
                    print(stableWo,"line 183")
                    Newsch.schNextWo=stableWo
                    Newsch.save()
                Newsch.save()
                #################
                wt=Tasks.objects.filter(workOrder=oldWo)
                wt2=Tasks.objects.filter(workOrder=stableWo)
                if(wt2!=None):
                    print("workOrder")
                    for f in wt2:
                        f.delete()

                if(wt!=None):
                    print("workOrder")
                    for f in wt:
                        print(f)
                        f.pk=None
                        f.workOrder=stableWo
                        f.taskStartDate=Newsch.schnextTime.date()
                        f.taskStartTime=Newsch.schnextTime.time()
                        f.save()
                ##############
                wp=WorkorderPart.objects.filter(woPartWorkorder=oldWo)
                wp2=WorkorderPart.objects.filter(woPartWorkorder=stableWo)
                if(wp2!=None):
                    for f in wp2:
                        f.delete()
                if(wp!=None):
                    for f in wp:
                        f.pk=None
                        f.woPartWorkorder=stableWo
                        f.save()
            #     ###############
                wf=WorkorderFile.objects.filter(woFileworkorder=oldWo)
                wf2=WorkorderFile.objects.filter(woFileworkorder=stableWo)
                if(wf2!=None):

                    for f in wf2:
                        f.delete()
                if(wf!=None):

                    for f in wf:
                        f.pk=None
                        f.woFileworkorder=stableWo
                        f.save()

            #     ################
            #     # try:
            #     #     wn=get_object_or_404(WorkorderUserNotification,woNotifWorkorder=oldWo)
            #     #     if(wn):
            #     #         wn.pk=None
            #     #         wn.woNotifWorkorder=stableWo
            #     #         wn.save()
            #     # except Exception as error:
            #     #     print(error)
            #
            #
            #
            #         #dt2=jdatetime.date(cd.year+sch.schMonthOfYearRep,sch.schMonthOfYearRep,sch.schDayOfMonthOfYearRep)
            elif(Newsch.schChoices==1):
                if(Newsch.shMeterReadingHasTiming==True):
                    Newsch.shMeterNextVal=Newsch.shMeterReadingStartAt+Newsch.shMeterReadingEvreyQnty
                    #Newsch.shMeterNextVal=Newsch.shMeterReadingEvreyQnty+Newsch.shMeterReadingStartAt
                    print("something")
                    Newsch.save()

                # stableWo.datecreated=datetime.now()
                # stableWo.timecreated=datetime.now()


        except Exception as e:
            print(e)
            exc_type, exc_obj, tb = sys.exc_info()
            print(tb.tb_lineno)
            print("wwww not saved")
    ######################
    @staticmethod
    def ForecastGeneratedWOParts():
        utc=pytz.UTC
        parts=dict()
        three_months =utc.localize( mydt1.now() + relativedelta(months=+13))
        #در زمان حرکت می کند
        time_bar=mydt1.now()

        wos=WorkOrder.objects.filter(running=True,isScheduling=True)
        sch=Schedule.objects.filter(workOrder__in=wos)
        for c in sch:
            if(c.schChoices==0):
                while(c.schnextTime<three_months ):
                    if(c.shHasEndDate and c.schnextTime>c.shEndDate):
                        break
                    swo=Workorder.objects.get(pk=c.workOrder)
                    swo_parts=WorkorderPart.objects.filter(woPartWorkorder=swo)
                    for p in swo_parts:
                        parts[str(p.woPartPart.id)]=parts[str(p.woPartPart.id)]+p.woPartPlannedQnty
                    c=generate_next_time(c)
        return parts
    #############################################
    @staticmethod
    def generate_next_time(Newsch):
        if(Newsch.schHowOften==1):
            d=Newsch.schHourRep
            Newsch.schnextTime=Newsch.schnextTime+timedelta(hours=d)
        elif(Newsch.schHowOften==2):
            d=Newsch.schDailyRep
            Newsch.schnextTime=Newsch.schnextTime+timedelta(d)
        elif(Newsch.schHowOften==3):
            dtList=[0,0,0,0,0,0,0]
            cd=Newsch.schnextTime+timedelta(+1)
            if(Newsch.isSunday==True):
                print("Sunday: is True")
                dtList[6]=1

            if(Newsch.isMonday==True):
                print("Monday: is True")
                dtList[0]=1

            if(Newsch.isTuesday==True):
                print("Tuesday: is True")
                dtList[1]=1

            if(Newsch.isWednenday==True):
                print("Wendsday: is True")
                dtList[2]=1

            if(Newsch.isThursday==True):
                print("Thursday: is True")
                dtList[3]=1

            if(Newsch.isFriday==True):
                print("Friday: is True")
                dtList[4]=1

            if(Newsch.isSaturday==True):
                print("saturday: is True")
                dtList[5]=1

            while(dtList[cd.weekday()]!=1):
                cd+=timedelta(1)
            if(cd.isocalendar()[1]==Newsch.schnextTime.isocalendar()[1]):
                Newsch.schnextTime=cd

            else:

                cd+=timedelta((Newsch.schWeeklyRep-1)*7)
                Newsch.schnextTime=cd
            print(cd,"@@@@@@@@@@@@")
            print(Newsch.schnextTime,"###########")
        elif(Newsch.schHowOften==4):
            cd=jdatetime.date.fromgregorian(day=(Newsch.schnextTime.day+1),month=Newsch.schnextTime.month,year=Newsch.schnextTime.year)#datetime.now()
            # t1=jdatetime.date.fromgregorian(day=Newsch.schnextTime.day,month=Newsch.schnextTime.month,year=Newsch.schnextTime.year)#datetime.now()# t1=jdatetime.date.fromgregorian(date=datetime.now())
            # while cd.day!=Newsch.schDayofMonthlyRep:
            #     cd+=timedelta(1)
            #
            # if(cd.month==t1.month):
            #         cd+=timedetal(month=Newsch.schMonthlyRep)#jdatetime.date(cd.year,((cd.month+Newsch.schMonthlyRep)%12)+1,cd.day)
            # else:
            # cd=jdatetime.date(cd.year,((cd.month+Newsch.schMonthlyRep-1)%12)+1,cd.day)
            # cd+=timedelta(month=Newsch.schMonthlyRep)
            # cd += relativedelta(months=+Newsch.schMonthlyRep)
                    #ss+=relativedelta(months=+sch.schMonthlyRep-1)

            cd=jdatetime.date(day=(Newsch.schDayofMonthlyRep),month=(cd+timedelta(Newsch.schMonthlyRep*30)).month,year=(cd+timedelta(Newsch.schMonthlyRep*30)).year)
            print(cd)


            Newsch.schnextTime=mydt1.combine(cd.togregorian(),datetime.datetime.now().time())
        elif(Newsch.schHowOften==5):
            #cd=jdatetime.date.fromgregorian(date=datetime.now())
            # dt1=jdatetime.date(Newsch.schnextTime.year,Newsch.schnextTime.month,Newsch.schnextTime.day)
            # Newsch.schnextTime=cd.togregorian()
            # cd=jdatetime.datetime.fromgregorian(day=xxx.day,month=xxx.month,year=xxx.year)#datetime.now()
            #cd=jdatetime.date.fromgregorian(date=datetime.now())
            # dt1=jdatetime.datetime.fromgregorian(year=cd.year,month=Newsch.schMonthOfYearRep,day=Newsch.schDayOfMonthOfYearRep)
            # print(dt1)
            dt1=Newsch.schnextTime
            # xdt=dt1.togregorian()
            # if(dt1<cd.togregorian()):
                # dt1=jdatetime.date().year,Newsch.schMonthOfYearRep,Newsch.schDayOfMonthOfYearRep)
            dt1=dt1+relativedelta(years=+Newsch.schYearlyRep)
            Newsch.schnextTime=dt1
        return Newsch
    #############################################
    @staticmethod
    def GenerateUpcommingWo(stdate,enddate,asset,category,user,maintenanceType):
        wos=[]
        woList=[]
        if(len(category)>0):
            wos=WorkOrder.objects.filter(woAsset__assetCategory__id__in=category,running=True,isScheduling=True)
        elif(len(asset)>0):
            wos=WorkOrder.objects.filter(woAsset__id__in=asset,running=True,isScheduling=True)
        else:
            wos=WorkOrder.objects.filter(running=True,isScheduling=True)
        if(len(user)>0):
                wos=wos.filter(assignedToUser__id__in=user)
        if(len(maintenanceType)>0):
                wos=wos.filter(maintenanceType_id__in=maintenanceType)

        three_months = enddate if enddate else mydt1.now(timezone.utc) + relativedelta(months=+40)
        #در زمان حرکت می کند
        time_bar=mydt1.now()
        sch=Schedule.objects.filter(workOrder__in=wos)
        # print("#####",sch)

        for c in sch:
            i=0
            if(c.schChoices==0):
                #.replace(tzinfo=None)
                while(c.schnextTime.date()<=three_months ):
                    # print(c.schnextTime,c.shEndDate,"**************")
                    if(c.shHasEndDate and c.schnextTime.date()>c.shEndDate):
                        break
                    swo=WorkOrder.objects.get(id=c.workOrder.id)
                    swo.datecreated=c.schnextTime.date()
                    swo.timecreated=c.schnextTime.time()
                    woList.append(swo)
                    c=ScheduleUtility.generate_next_time(c)




        wolist= sorted(woList,key=lambda x:x.datecreated)
        # print(wolist,"??????????????")
        return wolist
    @staticmethod
    def GenerateUpcommingWo2(stdate,enddate,maintenanceType):
        wos=[]
        woList=[]
        if(len(maintenanceType)>0):
                wos=WorkOrder.objects.filter(maintenanceType_id__in=maintenanceType,isScheduling=True,running=True)
        else:
            wos=WorkOrder.objects.filter(isScheduling=True,running=True)


        three_months = enddate if enddate else mydt1.now(timezone.utc) + relativedelta(months=+40)
        #در زمان حرکت می کند
        time_bar=mydt1.now()
        sch=Schedule.objects.filter(workOrder__in=wos)
        # print("#####",sch)

        for c in sch:
            i=0
            if(c.schChoices==0):
                #.replace(tzinfo=None)
                while(c.schnextTime.date()<=three_months ):
                    print(c.schnextTime,c.shEndDate,"**************")
                    if(c.shHasEndDate and c.schnextTime.date()>c.shEndDate):
                        break
                    swo=WorkOrder.objects.get(id=c.workOrder.id)
                    swo.datecreated=c.schnextTime.date()
                    swo.timecreated=c.schnextTime.time()
                    woList.append(swo)
                    c=ScheduleUtility.generate_next_time(c)




        wolist= sorted(woList,key=lambda x:x.datecreated)
        # print(wolist,"??????????????")
        return wolist
