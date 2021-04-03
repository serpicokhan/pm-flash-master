import jdatetime
import datetime
from dateutil import parser
from datetime import timedelta
from cmms.utils import *

class DateJob:
    @staticmethod
    def getQDate(dt1):
        cyear=jdatetime.datetime.now().year
        S=('z','p','t','b')
        k=0
        s1=[]
        i=dt1
        pval=0
        while(k<5):
            if(pval>=i):
                x=(cyear-1,S[i])
                s1.append(x)
            else:
                x=(cyear,S[i])
                s1.append(x)
                pval=i
            i=(i+1)%4
            k=k+1
        return s1
    @staticmethod
    def getQDateM(dt1):
        cyear=jdatetime.datetime.now().year
        S=('اسفند','بهمن','دی','آذر','آبان','مهر','شهریور','مرداد','تیر','خرداد','اردیبهشت','فروردین')
        k=0
        s1=[]
        i=dt1
        pval=0
        while(k<13):
            if(pval>=i):
                x=(cyear-1,S[i])
                s1.append(x)
            else:
                x=(cyear,S[i])
                s1.append(x)
                pval=i
            i=(i+1)%12
            k=k+1
        return s1

    @staticmethod
    def findQDate(dt):#dt is tuple like (1397,'z'):
        dt1=utilSDate[dt[1]]
        return ('{0}-{1}'.format(dt[0],dt1[0]),'{0}-{1}'.format(dt[0],dt1[1]))
    @staticmethod
    def findQDateM(dt):#dt is tuple like (1397,'فروردین'):
        dt1=utilMDate[dt[1]]
        return ('{0}-{1}'.format(dt[0],dt1[0]),'{0}-{1}'.format(dt[0],dt1[1]))





    @staticmethod
    def getTaskDate(dt1):
        if(dt1==""):
            return ""

        y=None
        y=str(dt1).split("-")
        #y=str(dt).split("-")
        if(len(y)==3):
            year=int(y[0])
            month=int(y[1])
            day=int(y[2])
            # print(jdatetime.date(year,month,day).togregorian(),"$$$$$$$$$$$$$$$$$$$")
            return jdatetime.date(year,month,day).togregorian()
        else:
            return datetime.date.today()
    #################################################################
    #################################################################

    @staticmethod
    def getDate(dt1):
        print("dt 27",dt1)
        if(not dt1):
            # print("###################$$$$$$$$$$$$$$$$$$$$$$$")
            return datetime.date.today()



        y=None
        if('/' in dt1):
             y=str(dt1).split("/")
        elif('-' in dt1):
             y=str(dt1).split("-")
        # print("###############",39)
        #y=str(dt).split("-")
        if(len(y)==3):
            year=int(y[0])
            month=int(y[1])
            day=int(y[2])
            # print("###############43####$$$$$$$$$$$$$$$$$$$$$$$")
            print(jdatetime.date(year,month,day).togregorian())
            return jdatetime.date(year,month,day).togregorian()
        else:
            return datetime.date.today()
    #################################################################
    #for schedule form only
    @staticmethod
    def getDate2(dt1):
        # print(dt1,"#@#@#@")

        if(not dt1):
            #print("###################$$$$$$$$$$$$$$$$$$$$$$$")
            return datetime.date.today()



        y=None
        y=str(dt1).split("-")
        if(len(y)==3):
            year=int(y[0])
            month=int(y[1])
            day=int(y[2])
            # print("###############43####$$$$$$$$$$$$$$$$$$$$$$$")
            # print(jdatetime.date(year,month,day).togregorian(),"$$$#$#$#$#################")
            return jdatetime.date(year,month,day).togregorian()
        else:
            return datetime.date.today()


    @staticmethod
    def getDateTime(dt):


        y=str(dt).split("-")
        if(len(y)==4):

            year=int(y[0])
            month=int(y[1])
            day=int(y[2])
            print("###########60########$$$$$$$$$$$$$$$$$$$$$$$")
            # print(jdatetime.date(year,month,day).togregorian())
            return jdatetime.date(year,month,day).togregorian()
        else:

            print("###64################$$$$$$$$$$$$$$$$$$$$$$$")

            return datetime.date.today()
    @staticmethod
    #for schedule form
    def getDateTime2(dt):

        # print(dt)
        y=str(dt).split("-")
        if(len(y)==3):

            year=int(y[0])
            month=int(y[1])
            day=int(y[2])
            # print("###########60########$$$$$$$$$$$$$$$$$$$$$$$")
            # print(year,month,day)
            # print(jdatetime.date(year,month,day).togregorian())
            return jdatetime.date(year,month,day).togregorian()
        else:
            return None

            # print("###64################$$$$$$$$$$$$$$$$$$$$$$$")

            return datetime.date.today()
    @staticmethod
    def getCurrentMonthHead():
        today=jdatetime.date.today()
        return jdatetime.date(today.year,today.month,1).togregorian()
    ###################################
    @staticmethod
    def getTodayDate():
        return jdatetime.date.today()
    ############################Convert to hijri date to gregorian#######################
    @staticmethod
    def convert2Date(startHijri,endHijri):
        start=DateJob.getCurrentMonthHead()
        end=DateJob.getTodayDate()
        if((startHijri) and (endHijri)):
            start=DateJob.getTaskDate(startHijri)
            end=DateJob.getTaskDate(endHijri)
        return start,end
    ############################
    @staticmethod
    def converttoTime(timeVal):
        return datetime.datetime.strptime(timeVal, '%H:%M:%S').time()
    ##########################Combine 2 date and time#######################
    @staticmethod
    def combine(dtVal,timeVal):

        return datetime.datetime.combine(dtVal,DateJob.converttoTime(timeVal))
    ###################################################################
