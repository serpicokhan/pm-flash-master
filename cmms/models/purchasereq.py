from django.db import models
from datetime import datetime
from cmms.models.Asset import Asset
import jdatetime
from django.db import models
from datetime import datetime
from cmms.models.business import *
import os
from cmms.utils import *
class PurchaseRequests(models.Model):
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
    def get_pstatus(self):
                 if(self.PurchaseRequestStatus==1):
                     return "<span class='badge badge-rounded badge-light'>درخواست شده </span>"
                 elif(self.PurchaseRequestStatus==2):
                     return "<span class='badge badge-rounded badge-secondary'> تعلیق </span>"
                 elif(self.PurchaseRequestStatus==6):
                     return "<span class='badge badge-rounded badge-info'> در حال پردازش </span>"
                 elif(self.PurchaseRequestStatus==7):
                     return "<span class='badge badge-rounded badge badge-success'> کامل شده </span>"
                 elif(self.PurchaseRequestStatus==8):
                     return "<span class='badge badge-rounded badge badge-warning'> متوقف </span>"
                 elif(self.PurchaseRequestStatus==5):
                     return "<span class='badge badge-rounded badge badge-danger'> باز</span>"
                 else:
                     return "<span class='badge badge-rounded badge-danger'>نامشخص </span>"
    def get_status_color(self):
         if(self.PurchaseRequestStatus==1):
             return "light"
         elif(self.PurchaseRequestStatus==2):
             return "secondary"
         elif(self.PurchaseRequestStatus==6):
             return "info"
         elif(self.PurchaseRequestStatus==7):
             return "success"
         else:
             return "danger"


    def getQTY(self):
        if(self.PurchaseRequestAssetQty):
            return self.PurchaseRequestAssetQty
        return self.PurchaseRequestAssetQtyNot

    def get_dateCreated_jalali(self):
        return jdatetime.date.fromgregorian(date=self.PurchaseRequestDateTo)
    def is_in_manager(self):
        return (self.PurchaseRequestRequestedUser.userId.groups.filter(name= 'manager').exists())


    PurchaseRequestStatus=models.IntegerField("وضعیت درخواست", choices=Status,null=True,blank=True)
    PurchaseRequestRequestedUser = models.ForeignKey('SysUser',on_delete=models.CASCADE,verbose_name="کاربر درخواست کننده",null=True,blank=True,related_name="PurchaseRequestdUser3")
    PurchaseRequestTayeedUser = models.ForeignKey('SysUser',on_delete=models.CASCADE,verbose_name="کاربر تایید کننده",null=True,blank=True,related_name="PurchaseAdmitter3")
    PurchaseRequestDateTo = models.DateField("تاریخ ", auto_now_add=True)
    PurchaseRequestCompletionDate = models.DateField("تاریخ تکمیل",blank=True,null=True)
    PurchaseRequestPartName=models.ForeignKey("Part",on_delete=models.CASCADE,null=True,blank=True,related_name="RequestedPart3",verbose_name="مشخصات قطعه")
    PurchaseRequestMoreInfo=models.CharField("اطلاعات بیشتر",max_length = 100,null=True,blank=True)
    PurchaseRequestAssetNotInInventory=models.CharField("ناموجود در انبار؟ اطلاعات بیشتری شرح دهید",max_length = 100,null=True,blank=True)
    #not in inventory qty
    PurchaseRequestQty=models.FloatField("تعداد")
    PurchaseRequestQtyNot=models.FloatField("کمیت",null=True,blank=True)
    PurchaseRequestNot=models.BooleanField("در صورت عدم تهیه تولید دچار وقفه میشود",default=False)
    PurchaseRequestNotInList=models.BooleanField(default=False,null=True)
    supplier = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True,related_name="suppliers3")
    # PurchaseRequestWO = models.ForeignKey('WorkOrder',on_delete=models.CASCADE,null=True,blank=True,related_name="ImpactedWO",verbose_name="درخواست مربوطه")
    PurchaseRequestAsset = models.ForeignKey('Asset',on_delete=models.CASCADE,null=True,blank=True,related_name="ImpactedAsset3",verbose_name="تجهیز")
    PurchaseRequestAssetMakan = models.ForeignKey('Asset',on_delete=models.CASCADE,null=True,blank=True,related_name="ImpactedLocation3")
    PurchaseRequestDateTo = models.DateField("مهلت تا تاریخ", auto_now_add=True)
    # PurchaseRequestDateFrom = models.DateField("تاریخ درخواست",blank=True,null=True)
    # PurchaseRequestDate2 = models.DateField("مهلت تا تاریخ",default=datetime.now, blank=True,null=True)
    settingTimestamp=models.DateTimeField(auto_now_add=True)

    PurchaseRequestAuthUser = models.ForeignKey('SysUser',on_delete=models.CASCADE,verbose_name="کاربر مجاز",null=True,blank=True,related_name="PurchaseRequestAuthUser3")
    PurchaseRequestPurchase=models.ForeignKey('MainPurchase',on_delete=models.CASCADE,null=True,blank=True,related_name="mainpurchase3")
    def __str__(self):
        return self.id

    class Meta:
       db_table = "purchaserequests"
       ordering = ('-id', )
       permissions = [
            ("change_request_status", "Can change the status of purchase request status"),

        ]

class MainPurchase(models.Model):
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

    def get_dateCreated_jalali(self):
        return jdatetime.date.fromgregorian(date=self.PurchaseDateTo)


    PurchaseStatus=models.IntegerField("وضعیت درخواست", choices=Status,null=True,blank=True)
    PurchaseRequestedUser = models.ForeignKey('SysUser',on_delete=models.CASCADE,verbose_name="کاربر درخواست کننده",null=True,related_name="PurchaseRequestdUserMain")
    PurchaseTayeedUser = models.ForeignKey('SysUser',on_delete=models.CASCADE,verbose_name="کاربر تایید کننده",null=True,blank=True,related_name="PurchaseAdmitterMain")
    PurchaseDateTo = models.DateField("تاریخ ", auto_now_add=True)
    PurchaseCompletionDate = models.DateField("تاریخ تکمیل",blank=True,null=True)




    class Meta:
       db_table = "mainpurchase"

class RequestFile(models.Model):
    def get_ext(self):
        v=os.path.splitext(self.woFile.name)
        return v[len(v)-1]
    def get_name(self):
        return os.path.basename(str(self.msgFile))
    def get_size(self):
        return " MB {0:.2f}".format(self.woFile.size/1048576)

    msgFile=models.FileField(upload_to='documents/%Y/%m/%d',max_length=200)
    msgFileworkorder=models.ForeignKey(MainPurchase,on_delete=models.CASCADE,blank=True,null=True)
    msgFiledateAdded=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="purchasefile"
class RequestVoice(models.Model):
    def get_ext(self):
        v=os.path.splitext(self.woFile.name)
        return v[len(v)-1]
    def get_name(self):
        return os.path.basename(str(self.msgFile))
    def get_size(self):
        return " MB {0:.2f}".format(self.woFile.size/1048576)

    msgFile=models.FileField(upload_to='documents/%Y/%m/%d',max_length=200)
    msgFileworkorder=models.ForeignKey(MainPurchase,on_delete=models.CASCADE,blank=True,null=True)
    msgFiledateAdded=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="requestvoice"
