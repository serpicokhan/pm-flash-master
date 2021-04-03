import jdatetime
import datetime
from datetime import datetime

from datetime import timedelta,date,timezone
import pytz
from django.shortcuts import get_list_or_404, get_object_or_404
from django.forms.models import model_to_dict
from dateutil.relativedelta import *

import sys
from cmms.models import WorkOrder,Schedule,WorkorderTask,WorkorderFile,WorkorderPart,WorkorderUserNotification
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
                    stableWo.pk=None
                else:
                    stableWo=Newsch.schNextWo
                    schIsNewFlag=False
                oldWo=WorkOrder.objects.get(id=Newsch.workOrder_id)

                if(Newsch.schHowOften==1):
                    d=Newsch.schHourRep
                    Newsch.schnextTime=datetime.now()+timedelta(hours=d)
                elif(Newsch.schHowOften==2):
                    d=Newsch.schDailyRep
                    Newsch.schnextTime=datetime.now()+timedelta(d)
                elif(Newsch.schHowOften==3):
                    dtList=[0,0,0,0,0,0,0]
                    cd=datetime.now()
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
                    if(cd.isocalendar()[1]==date.today().isocalendar()[1]):
                        Newsch.schnextTime=cd
                    else:
                        cd+=timedelta((Newsch.schWeeklyRep-1)*7)
                        Newsch.schnextTime=cd
                elif(Newsch.schHowOften==4):
                    xxx=datetime.now()
                    cd=jdatetime.date.fromgregorian(day=xxx.day,month=xxx.month,year=xxx.year)#datetime.now()
                    t1=jdatetime.date.fromgregorian(day=xxx.day,month=xxx.month,year=xxx.year)#datetime.now()# t1=jdatetime.date.fromgregorian(date=datetime.now())
                    while cd.day!=Newsch.schDayofMonthlyRep:
                        cd+=timedelta(1)

                    if(cd.month==t1.month):

                            # kdate=jdatetime.date.fromgregorian(
                            # if(cd.month+Newsch.schMonthlyRep>12)
                            # cd=jdatetime.date(cd.year,((cd.month+(Newsch.schMonthlyRep)%12),cd.day)
                            xxx=cd.togregorian()+relativedelta(months=+Newsch.schMonthlyRep)
                            print("l1")
                    else:
                        xxx=cd.togregorian()+relativedelta(months=+(Newsch.schMonthlyRep-1))
                        print("l2")
                            #ss+=relativedelta(months=+sch.schMonthlyRep-1)

                    Newsch.schnextTime=datetime.combine(xxx,datetime.now().time())

                elif(Newsch.schHowOften==5):
                    xxx=datetime.now()
                    cd=jdatetime.datetime.fromgregorian(day=xxx.day,month=xxx.month,year=xxx.year)#datetime.now()
                    #cd=jdatetime.date.fromgregorian(date=datetime.now())
                    dt1=jdatetime.datetime(year=cd.year,month=Newsch.schMonthOfYearRep,day=Newsch.schDayOfMonthOfYearRep)
                    print(dt1)
                    xdt=dt1.togregorian()
                    if(dt1<cd.togregorian()):
                        # dt1=jdatetime.date().year,Newsch.schMonthOfYearRep,Newsch.schDayOfMonthOfYearRep)
                        xdt=xdt+relativedelta(years=+Newsch.schYearlyRep)
                    else:
                        xdt=xdt+relativedelta(years=+(Newsch.schYearlyRep-1))




                    Newsch.schnextTime=datetime.combine(xdt,datetime.now().time())
                stableWo.datecreated=Newsch.schnextTime.date()
                stableWo.timecreated=Newsch.schnextTime.time()
                stableWo.visibile=False
                stableWo.isScheduling=False
                stableWo.isPartOf=Newsch.workOrder
                # Newsch.schNextWo=WorkOrder.objects.create(datecreated=Newsch.schnextTime.date(),timecreated=Newsch.schnextTime.time(),visibile=False,isScheduling=False,isPartOf=Newsch.workOrder)


                stableWo.save()
                if(schIsNewFlag):
                    Newsch.schNextWo=stableWo
                Newsch.save()
                #################
                wt=WorkorderTask.objects.filter(workorder=oldWo)
                if(wt!=None):
                    for f in wt:
                        f.pk=None
                        f.workorder=stableWo
                        f.save()
                ##############
                wp=WorkorderPart.objects.filter(woPartWorkorder=oldWo)
                if(wp!=None):
                    for f in wp:
                        f.pk=None
                        f.woPartWorkorder=stableWo
                        f.save()
                ###############
                wf=WorkorderFile.objects.filter(woFileworkorder=oldWo)
                if(wf!=None):

                    for f in wf:
                        f.pk=None
                        f.woFileworkorder=stableWo
                        f.save()

                ################
                # try:
                #     wn=get_object_or_404(WorkorderUserNotification,woNotifWorkorder=oldWo)
                #     if(wn):
                #         wn.pk=None
                #         wn.woNotifWorkorder=stableWo
                #         wn.save()
                # except Exception as error:
                #     print(error)



                    #dt2=jdatetime.date(cd.year+sch.schMonthOfYearRep,sch.schMonthOfYearRep,sch.schDayOfMonthOfYearRep)
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
        three_months =utc.localize( datetime.now() + relativedelta(months=+13))
        #در زمان حرکت می کند
        time_bar=datetime.now()

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
                print("hirekhar2")
            else:
                print("hirekhar")
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


            Newsch.schnextTime=datetime.combine(cd.togregorian(),datetime.now().time())
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

        three_months = enddate if enddate else datetime.now(timezone.utc) + relativedelta(months=+40)
        #در زمان حرکت می کند
        time_bar=datetime.now()
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
    @staticmethod
    def GenerateUpcommingWo2(stdate,enddate,maintenanceType):
        wos=[]
        woList=[]
        if(len(maintenanceType)>0):
                wos=WorkOrder.objects.filter(maintenanceType_id__in=maintenanceType,isScheduling=True,running=True)
        else:
            wos=WorkOrder.objects.filter(isScheduling=True,running=True)


        three_months = enddate if enddate else datetime.now(timezone.utc) + relativedelta(months=+40)
        #در زمان حرکت می کند
        time_bar=datetime.now()
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
