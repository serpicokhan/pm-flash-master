#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
from cmms.models.workorder import *
from cmms.models.Asset import *
from cmms.utils import *

from cmms.models.event import *
class Schedule(models.Model):
    def get_nextTime_jalali(self):
        if(self.schnextTime):
            return jdatetime.datetime.fromgregorian(date=self.schnextTime)
    CHOICES=[(0,'item 1'),
          (1,'item 2'),
          (2,'item 3')]
    COMPARISON=[(0,'بزرگتر از'),
                (1,'کوچکتر از'),
                ]
    TimeCHOICES=[
          (1,'ساعتی'),
          (2,'روزانه'),
          (3,'هفتگی'),
          (4,'ماهانه'),
          (5,'سالانه'),]
    Month=[(1,'فروردین'),
          (2,'اردیبهشت'),
          (3,'خرداد'),
          (4,'تیر'),
          (5,'مرداد'),
          (6,'شهریور'),
          (7,'مهر'),
                (8,'آبان'),
                (9,'آذر'),
                (10,'دی'),
                (11,'بهمن'),
                (12,'اسفند'),

          ]
    HasEnded=[(0,'ساعتی'),
    (1,'روزانه'),]

    FixedOrFloating=[(True,'ثابت'),
                    (False,'شناور')]
    schChoices=models.IntegerField("اولویت", choices=CHOICES,null=True,default=0)
    schHowOften=models.IntegerField("تکرار", choices=TimeCHOICES,null=True,default=1)

    schHourRep=models.IntegerField("ساعت",null=True,blank=True)
    schHourIsFixed=models.BooleanField("ثابت",default=True,choices=FixedOrFloating,blank=True)

    schDailyRep=models.IntegerField("روز",null=True,blank=True)
    schDayIsFixed=models.BooleanField("ثابت",default=True,choices=FixedOrFloating,blank=True)

    schWeeklyRep=models.IntegerField("هفته",blank=True,null=True)

    isSunday=models.BooleanField("یکشنبه",default=True,blank=True)
    isMonday=models.BooleanField("دوشنبه",default=True,blank=True)
    isTuesday=models.BooleanField("سه شنبه",default=True,blank=True)
    isWednenday=models.BooleanField("چهارشنبه",default=True,blank=True)
    isThursday=models.BooleanField("پنجشنبه",default=True,blank=True)
    isFriday=models.BooleanField("جمعه",default=True,blank=True)
    isSaturday=models.BooleanField("شنبه",default=True,blank=True)

    schMonthlyRep=models.IntegerField("ماه",blank=True,null=True)
    schDayofMonthlyRep=models.IntegerField("روز",blank=True,null=True)
    schMonthIsFixed=models.BooleanField("ثابت",blank=True,choices=FixedOrFloating)

    schYearlyRep=models.IntegerField("ماه",blank=True,null=True)
    schMonthOfYearRep=models.IntegerField("ماه",blank=True,null=True,choices=Month)
    schDayOfMonthOfYearRep=models.IntegerField("روز",blank=True,null=True)
    schYearIsFixed=models.BooleanField("ثابت",default=True,choices=FixedOrFloating,blank=True)
    shStartDate=models.DateField("تاریخ شروع",blank=True,null=True)

    shEndDate=models.DateField("تاریخ شروع",blank=True,null=True)
    #shHasEndDate=models.IntegerField("",choices=HasEnded,null=True,blank=True)
    shHasEndDate=models.BooleanField("تاریخ انقضا",blank=True)

    shMeterReadingEvreyQnty=models.FloatField("هر",null=True,blank=True,default=0)
    shMeterReadingMetrics=models.IntegerField("واحد اندازه گیری",choices=Metric,null=True,blank=True)
    shMeterReadingStartAt=models.FloatField("مقدار شروع",null=True,blank=True)
    shMeterReadingEndBy=models.FloatField("مقذار نهایی",null=True,blank=True)
    schMeterReadingIsFixed=models.BooleanField("ثابت",default=True,choices=FixedOrFloating,blank=True)
    schHasEndReading=models.BooleanField("مقدار پایانی",default=False)
    #shReadingHasEndDate=models.IntegerField("dsadas",choices=HasEnded,null=True,blank=True)
    #shReadingHasEndDate=models.IntegerField("واحد اندازه گیری",null=True,blank=True)

    shMeterReadingHasTiming=models.BooleanField(default=True)
    shMeterReadingWhenQnty=models.FloatField("زمان",null=True,blank=True)
    shMeterReadingWhenMetric=models.IntegerField(choices=Metric,null=True,blank=True)
    shMetricComparison=models.IntegerField(choices=[(0,'بزرگتر از'),(1,'کوچکتر از')],null=True,blank=True)
    schEvent = models.ForeignKey(Events,on_delete=models.CASCADE,null=True,blank=True)


    schnextTime=models.DateTimeField(blank=True,null=True)
    schNextWo=models.ForeignKey('WorkOrder',on_delete=models.CASCADE,null=True,blank=True,related_name="schnextWo")

    schTimestamp=models.DateTimeField(auto_now_add=True)
    #shStartTime2=models.TimeField()










    schAsset=models.ForeignKey(Asset,on_delete=models.CASCADE,null=True,blank=True,related_name="schAsset")
    workOrder = models.ForeignKey('WorkOrder',on_delete=models.CASCADE,null=True,blank=True)
    shMeterNextVal = models.FloatField("مقدار بعدی", null=True, blank=True)



    class Meta:
      db_table = "schedule"
