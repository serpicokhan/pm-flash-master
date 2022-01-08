#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb
import os
from django.db import models
from cmms.models.users import SysUser

from datetime import datetime
import jdatetime

from cmms.models.parts import *
from cmms.models.schedule import *
from cmms.models.Asset import *
from cmms.models.project import *
from cmms.models.stock import *
from cmms.models.task import *
#from cmms.models.task import *
from cmms.utils import *
from django.utils.timezone import now

class KpiException(models.Model):
    stopcode = models.ForeignKey('StopCode',on_delete=models.CASCADE,unique=True,verbose_name='کد توقف')
    # stopCode1=models.CharField("کد توقف",max_length = 100,null=True,blank=True,unique=True)

    def __str__(self):
        return self.stopcode.__str__()

    class Meta:
       db_table = "kpiexception"

class StopCode(models.Model):
    def __str__(self):
        return self.stopDescription
    stopCode=models.CharField("کد توقف",max_length = 100,null=True,blank=True,unique=True)
    stopDescription=models.CharField("شرح توقف",max_length = 100,null=True,blank=True)
    # problemIsActive=models.BooleanField("فعال",default=True,blank=True)
    class Meta:
        db_table="stopcode"
class MeterCode(models.Model):
    def __str__(self):
        return self.meterDescription
    meterCode=models.CharField("کد",max_length = 100,null=True,blank=True,unique=True)
    meterDescription=models.CharField("َشرح",max_length = 100,null=True,blank=True)
    meterAbbr=models.CharField("اختصار",max_length = 5,null=True,blank=True)

    class Meta:

        db_table="metercode"


class MiscCostCode(models.Model):
    def __str__(self):
        return self.miscCostDescription
    miscCostCode=models.CharField("کد",max_length = 100,null=True,blank=True,unique=True)
    miscCostDescription=models.CharField("َشرح",max_length = 100,null=True,blank=True)

    class Meta:
        db_table="misccostcode"

###########################################
class ProblemCode(models.Model):
    def __str__(self):
        return self.problemCode
    problemCode=models.CharField("کد مشکل",max_length = 100,null=True,blank=True,unique=True)
    problemDescription=models.CharField("شرح مشکل",max_length = 100,null=True,blank=True)
    problemIsActive=models.BooleanField("فعال",default=True,blank=True)
    class Meta:
        db_table="problemcode"
###########################################
class PertCode(models.Model):
    def __str__(self):
        return self.pertCode
    pertCode=models.CharField("کد پرت",max_length = 100,null=True,blank=True,unique=True)
    pertDescription=models.CharField("شرح",max_length = 100,null=True,blank=True)
    # problemIsActive=models.BooleanField("فعال",default=True,blank=True)
    class Meta:
        db_table="pertcode"
class WorkorderPert(models.Model):

    woPertWorkorder= models.ForeignKey('WorkOrder',on_delete=models.CASCADE,verbose_name="دستور کار",null=True,blank=True)
    woPertPert= models.ForeignKey('PertCode',on_delete=models.CASCADE,verbose_name="کد پرت",null=True,blank=True)
    wpPertTime = models.FloatField("مقدار پرت (دقیقه)",default=0, null=True)
    # problemIsActive=models.BooleanField("فعال",default=True,blank=True)
    class Meta:
        db_table="workorderpert"
        unique_together = ('woPertWorkorder', 'woPertPert',)
###########################################
class CauseCode(models.Model):
    def __str__(self):
        return self.causeDescription
    causeCode=models.CharField("کد علت",max_length = 100,null=True,blank=True,unique=True)
    causeDescription=models.CharField("شرح علت",max_length = 100,null=True,blank=True)
    causeIsActive=models.BooleanField("فعال",default=True,blank=True)
    class Meta:
        db_table="causecode"
###########################################
class ActionCode(models.Model):
    def __str__(self):
        return self.actionCode
    actionCode=models.CharField("کد اقدام",max_length = 100,null=True,blank=True,unique=True)
    actionDescription=models.CharField("شرح اقدام",max_length = 100,null=True,blank=True)
    actionIsActive=models.BooleanField("فعال",default=True,blank=True)
    class Meta:
        db_table="actioncode"

class MaintenanceType(models.Model):

    name=models.CharField("نام",max_length = 50)
    description=models.CharField("توضیحات",max_length = 50)
    color=models.CharField("رنگ",max_length=10,default='#FF0000')
    def __str__(self):
        return self.name

    class Meta:
       db_table = "maintenancetype"

class WorkOrder(models.Model):
    Requested=1
    onHold=2
    Draft=3
    Assigned=4
    Open=5
    workInProgress=6
    closedComplete=7
    closedIncomplete=8
    waitingForPart=9
    invisible=-1
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Status=(
         (Requested,'درخواست شده')  ,
         (onHold,'متوقف'),
         (Assigned,'تخصیص داده شده'),
         (Open,'باز'),
         (workInProgress,'در حال پیشرفت'),
         (closedComplete,'بسته شده کامل'),
         (closedIncomplete,'بسته شده، ناقص'),
         (waitingForPart,'در انتظار قطعه'),

     )
    Priority=(
        (Highest,'خیلی زیاد'),
        (High,'زیاد'),
        (Medium,'متوسط'),
        (Low,'پایین'),
        (Lowest,'خیلی پایین'),
    )
    def get_actual_labour2(self):
        times= Tasks.objects.raw("select floor(COALESCE(sum(timestampdiff(minute,cast(concat(taskStartDate, ' ', taskStartTime) as datetime),        cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0)) as id from tasks where workOrder_id={0}".format(self.id))[0].id
        # times=times/60
        times=times/60
        a='{0:02.0f}:{1:02.0f}'.format(*divmod(times * 60, 60))
        # print(a)
        return a
        # return times
        # return Tasks.objects.all()[0].id
    def __str__(self):
        if(self.isScheduling):
            return "SM{}".format(self.id)
        else:
            return "WO{}".format(self.id)
    def getSchedule(self):
        if(self.isScheduling):
            sch=Schedule.objects.filter(workOrder=self.id)
            print("0000000",sch)
            str=''
            for c in sch:
                print(c.schChoices,'FFFFFFFFFF')

                if(c.schChoices==0):
                    print("goooooooooood")
                    if(c.schHowOften==1):
                        str=str+'هر {} ساعت '.format(c.schHourRep)
                    elif(c.schHowOften==2):
                        str=str+'هر {} روز '.format(c.schHourRep)
                    elif(c.schHowOften==3):
                        str=str+'هر {} هفته <ذق'.format(c.schWeeklyRep)
                    elif(c.schHowOften==4):
                        str=str+'هر {} ماه '.format(c.schMonthlyRep)
                    else:
                        str=str+'هر {} سال '.format(c.schHourRep)
            return str
    def get_woStatus(self):
                 if(self.running==True):
                     return "<i class='fa fa-check'>										</i>								"
                 else:
                     return "<i class='fa fa-times'>										</i>					"




    def get_assoc_user_from_tasks(self):
        users=Tasks.objects.filter(workOrder=self)
        str=[]
        for k in users:
            if(k.taskAssignedToUser):
                str.append(k.taskAssignedToUser.title)
        return ",".join(str)
    def get_pertTime(self):
        perts=WorkorderPert.objects.filter(woPertWorkorder=self)
        sum=0
        for p in perts:
            sum=sum+p.wpPertTime
        return sum



    # def getRelatedTask(self):
    #     return list(cmms.models.task.Tasks.objects.filter(workOrder=self.id))
    def get_dateCreated_jalali(self):
        return jdatetime.date.fromgregorian(date=self.datecreated)
    def get_dateTimeCreated_jalali(self):
        return "{0}".format(jdatetime.date.fromgregorian(date=self.datecreated))
    # def get_datec_jalali(self):
    #     return "{0}".format(jdatetime.date.fromgregorian(date=self.datecreated))
    def get_dateCompelted_jalali(self):
        if(self.dateCompleted):
            return jdatetime.date.fromgregorian(day=self.dateCompleted.day,month=self.dateCompleted.month,year=self.dateCompleted.year)
    def get_dateRequire_jalali(self):
        if(self.requiredCompletionDate):
            return jdatetime.date.fromgregorian(day=self.requiredCompletionDate.day,month=self.requiredCompletionDate.month,year=self.requiredCompletionDate.year)
    def get_omr(self):
        dt1=datetime.combine(self.datecreated,self.timecreated)
        dt2=datetime.now()
        if(self.woStatus==7 or self.woStatus==8):
            if(self.dateCompleted):
                dt3=datetime.combine(self.dateCompleted,self.timeCompleted)
                days=(dt3-dt1).total_seconds()/(3600*24)
                hours=((dt3-dt1).total_seconds()/(3600))%24
            else:
                days=(dt2-dt1).total_seconds()/(3600*24)
                hours=((dt2-dt1).total_seconds()/(3600))%24
        else:
            days=(dt2-dt1).total_seconds()/(3600*24)
            hours=((dt2-dt1).total_seconds()/(3600))%24
        return "{0:.0f} روز ,{1:.0f} ساعت".format(days,hours)
    def get_dirkard(self):
        dt1=datetime.combine(self.requiredCompletionDate,self.requiredCompletionTime)
        dt2=datetime.now()
        if(self.woStatus==7 or self.woStatus==8):
            if(self.dateCompleted):
                dt3=datetime.combine(self.dateCompleted,self.timeCompleted)
                days=(dt3-dt1).total_seconds()/(3600*24)
                hours=((dt3-dt1).total_seconds()/(3600))%24
            else:
                days=(dt2-dt1).total_seconds()/(3600*24)
                hours=((dt2-dt1).total_seconds()/(3600))%24
        else:
            days=(dt2-dt1).total_seconds()/(3600*24)
            hours=((dt2-dt1).total_seconds()/(3600))%24




        return "{0:.0f} روز ,{1:.0f} ساعت".format(days,hours)


    def getPartName(self):
        partname=WorkorderPart.objects.filter(woPartWorkorder=self)
        str=''
        for k in partname:
            str="{0},{1}".format(k.woPartStock.stockItem,str)
        return str
    def getPartQty(self):
        partname=WorkorderPart.objects.filter(woPartWorkorder=self)
        str=''
        for k in partname:
            str="{0},{1}".format(k.woPartActulaQnty,str)
        return str


        #return "ewqewQ"
    woStatus=models.IntegerField("وضعیت درخواست", choices=Status,null=True,blank=True)
    maintenanceType=models.ForeignKey(MaintenanceType,on_delete=models.CASCADE,verbose_name="نوع نگهداری",null=True,blank=True)
    woPriority=models.IntegerField("اولویت", choices=Priority,null=True,blank=True)
    woAsset = models.ForeignKey(Asset,on_delete=models.CASCADE,blank=True,null=True,verbose_name="دارایی")#models.CharField("نام سالن",max_length = 50)
    Project = models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name="پروژه",null=True,blank=True)
    requiredCompletionDate = models.DateField(" تاریخ اتمام مورد نیاز",default=datetime.now, blank=True)
    requiredCompletionTime = models.TimeField("زمان",default=datetime.now, blank=True)
    summaryofIssue = models.CharField("خلاصه مشکل",max_length = 200,null=True,blank=True)
    workInstructions = models.CharField("دستورالعمل",max_length = 50,null=True,blank=True)
    assignedToUser = models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="اختصاص به کاربر",null=True,blank=True,related_name="assignedToUser")
    estimatedLabor = models.FloatField("ساعت کار مورد نیاز (تخمینی)",null=True,blank=True)
    completedByUser = models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="تکمیل درخواست توسط کاربر",null=True,blank=True,related_name="completedByUser")
    actualLabor = models.FloatField("ساعت کار واقعی",null=True,blank=True)
    datecreated = models.DateField("تاریخ ایجاد",default=datetime.now, blank=True,null=True)
    timecreated = models.TimeField("زمان ایجاد", blank=True,null=True)
    dateCompleted = models.DateField(" تاریخ تکمیل(تخمینی)", blank=True,null=True)
    timeCompleted = models.TimeField("زمان تکمیل(تخمین",default=datetime.now, blank=True)
    #Cost Tracking ??????
    account = models.CharField("حساب",max_length = 50,null=True,blank=True)
    chargeDepartment = models.CharField("دپارتمان مسوول",max_length = 50,null=True,blank=True)
    #Completion Notes
    completionNotes = models.CharField("اطلاعات تکمیلی",max_length = 200,null=True,blank=True)
    problemBrief = models.CharField("مشکل (خلاصه)",max_length = 50,null=True,blank=True)
    rootCause = models.CharField("علت اصلی",max_length = 50,null=True,blank=True)
    solution  = models.CharField("راه حل",max_length = 50,null=True,blank=True)
    adminNote  = models.CharField("توضیحات مدیر",max_length = 50,null=True,blank=True)
    allTriggerFire=models.BooleanField("تمامی محرک ها",default=True,blank=True)
    isScheduling=models.BooleanField(default=False,blank=True)
    isEM=models.BooleanField("درخوسات ناخواسته یا EM",default=False,blank=True)
    #estimated compilation days after wo completed
    estimatedCompilation=models.IntegerField("زمان تخمینی تکمیل(روز)",default=1,null=True,blank=True)
    #Create a new work order even if there are work orders not closed from this Scheduled Maintenance
    creatNewWO=models.BooleanField("ایجاد درخواست جدید در صورت بسته نشدن درخوسات قبلی",default=False,blank=True)

    running=models.BooleanField("در حال اجرا",default=False,blank=True)
    #برای مشخص شدن wo های زیر مجموعه schedule maintenance
    isPartOf = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name="زیر مجموعه",null=True,blank=True)
    timeStamp=models.DateTimeField(auto_now_add=True)
    visibile=models.BooleanField(default=True,blank=True)
    # for sending email purpose
    isUpdating=models.BooleanField(default=False,blank=True)
    # Preventive or on demand wo
    # it must be determind in wo creation time
    isPm=models.BooleanField(default=False)
    woTags=models.TextField(null=True,blank=True)
    RequestedUser = models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="درخواست کننده",null=True,blank=True,related_name="RequestedUser")
    woStopCode = models.ForeignKey(StopCode,on_delete=models.CASCADE,verbose_name="کد توقف",null=True,blank=True,related_name="woStopCode")
    woProblemCode = models.ForeignKey(ProblemCode,on_delete=models.CASCADE,verbose_name="کد مشکل",null=True,blank=True,related_name="woProblemCode")
    woCauseCode = models.ForeignKey(CauseCode,on_delete=models.CASCADE,verbose_name="کد علت",null=True,blank=True,related_name="woCauseCode")
    woActionCode = models.ForeignKey(ActionCode,on_delete=models.CASCADE,verbose_name="کد اقدام",null=True,blank=True,related_name="woActionCode")
    #تئقف داشته استفاده
    # hasStop=models.BooleanField(default=False)




    class Meta:
      db_table = "workorder"
class WorkorderPart(models.Model):
    woPartWorkorder=models.ForeignKey(WorkOrder,on_delete=models.CASCADE,blank=True,null=True,verbose_name="سفارش کار")
    # woPartPart=models.ForeignKey(Part,on_delete=models.CASCADE,verbose_name="نام قطعه")
    woPartPlannedQnty=models.FloatField("کمیت پیشنهادی",default=0.0,blank=True,null=True)
    woPartActulaQnty=models.FloatField("کمیت واقعی",default=0.0,blank=True,null=True)
    woPartStock=models.ForeignKey(Stock,on_delete=models.CASCADE,null=True,blank=True,verbose_name="انبار")
    timeStamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="workorderpart"
        unique_together = ('woPartWorkorder', 'woPartStock')
class WorkorderMeterReading(models.Model):
    def getRow(self):
         return "{}  {}".format(self.get_woMeterReadingMeterReadingUnit_display(),self.woMeterReadingMeterReading)
    def getdate(self):
        return jdatetime.date.fromgregorian(date=self.timestamp)
    woMeterReadingworkorder=models.ForeignKey(WorkOrder,on_delete=models.CASCADE,blank=True,null=True,verbose_name="سفارش کار")

    woMeterReadingLocation=models.ForeignKey(Asset,on_delete=models.CASCADE,blank=True,null=True,verbose_name="دارایی")
    woMeterReadingMeterReading=models.FloatField("meter reading",default=0.00)
    woMeterReadingMeterReadingUnit=models.ForeignKey("MeterCode",verbose_name="واحد اندازه گیری",on_delete=models.CASCADE,null=True,blank=True,related_name="woMeterReadingMeterReadingUnit")
    timestamp=models.DateField(default=datetime.now, blank=True)
    class Meta:
        db_table="workordermeterreading"
########################################################
class MiscCost(models.Model):
    miscCoastWorkorder=models.ForeignKey(WorkOrder,on_delete=models.CASCADE)
    miscCoastType=models.ForeignKey("MiscCostCode",verbose_name="نوع",on_delete=models.CASCADE,null=True,blank=True,related_name="miscCoastWorkorder")
    miscCoastIndividual=models.ForeignKey("Business",verbose_name="پیمانکار",on_delete=models.CASCADE,null=True,blank=True,related_name="miscCoastIndividuals")
    miscCoastdescription=models.CharField("توضیحات",max_length = 100,null=True,blank=True)
    estimatedQnty=models.FloatField("مقدار تخمینی",default=0.0,blank=True,null=True)
    estimatedUnitCoast=models.FloatField("هزینه تخمینی بازای واحد",default=0.0,blank=True,null=True)
    estimatedTotalCoast=models.FloatField("هزینه تخمینی کلی",default=0.0,blank=True,null=True)
    qnty=models.FloatField("مقدار واقعی",default=0.0,blank=True,null=True)
    actualUnitCoast=models.FloatField("هزینه واحد",default=0.0,blank=True,null=True)
    actualTotlaCoast=models.FloatField("هزینه کل",default=0.0,blank=True,null=True)
    timeStamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="misccoast"
 ########################################################
class WorkorderUserNotification(models.Model):
    def get_woNotifOnAssignment(self):
        if(self.woNotifOnAssignment==True):
            return "<i class='fa fa-check'>										</i>								"
        else:
            return "<i class='fa fa-times'>										</i>					"

    def get_woNotifOnStatusChange(self):
        if(self.woNotifOnStatusChange==True):
            return "<i class='fa fa-check'>										</i>								"
        else:
            return "<i class='fa fa-times'>										</i>					"

    def get_woNotifOnCompletion(self):
        if(self.woNotifOnStatusChange==True):
            return "<i class='fa fa-check'>										</i>								"
        else:
            return "<i class='fa fa-times'>										</i>					"
    def get_woNotifOnCompletion(self):
          if(self.woNotifOnCompletion==True):
              return "<i class='fa fa-check'>										</i>								"
          else:
              return "<i class='fa fa-times'>										</i>					"
    def get_woNotifOnTaskCompleted(self):
             if(self.woNotifOnTaskCompleted==True):
                 return "<i class='fa fa-check'>										</i>								"
             else:
                 return "<i class='fa fa-times'>										</i>					"
    def get_woNotifOnOnlineOffline(self):
          if(self.woNotifOnOnlineOffline==True):
              return "<i class='fa fa-check'>										</i>								"
          else:
              return "<i class='fa fa-times'>										</i>					"



    woNotifWorkorder=models.ForeignKey(WorkOrder,on_delete=models.CASCADE)
    woNotifUser=models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="کاربر")
    woNotifOnAssignment=models.BooleanField("پیام رسانی هنگام ایجاد درخواست",default=True)
    woNotifOnStatusChange=models.BooleanField("پیام رسانی هنگام تغییر",default=False)
    woNotifOnCompletion=models.BooleanField("پیام رسانی هنگام تکمیل",default=False)
    woNotifOnTaskCompleted=models.BooleanField("پیام رسانی هنگام تکمیل وظیفه",default=False)
    woNotifOnOnlineOffline=models.BooleanField("پیام رسانی هنگام آنلاین آفلاین شدن",default=False)
    class Meta:
        db_table="workorderusernotification"
#############################################
class WorkorderFile(models.Model):
    def get_ext(self):
        v=os.path.splitext(self.woFile.name)
        return v[len(v)-1]
    def get_size(self):
        return " MB {0:.2f}".format(self.woFile.size/1048576)

    woFile=models.FileField(upload_to='documents/',max_length=200)
    woFileworkorder=models.ForeignKey(WorkOrder,on_delete=models.CASCADE,blank=True,null=True)
    woFiledateAdded=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="workorderfile"
class MiniWorkOrder(models.Model):
    class Meta:
        db_table="miniworkorder"
