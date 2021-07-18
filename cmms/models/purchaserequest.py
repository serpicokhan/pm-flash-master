from django.db import models
from datetime import datetime
from cmms.models.Asset import Asset
class PurchaseRequest(models.Model):
    def getQTY(self):
        if(self.PurchaseRequestAssetQty):
            return self.PurchaseRequestAssetQty
        return self.
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
    PurchaseRequestStatus=models.IntegerField("وضعیت درخواست", choices=Status,null=True,blank=True)
    PurchaseRequestAssetName=models.CharField("مشخصات",max_length = 100,null=True,blank=True)
    PurchaseRequestMoreInfo=models.CharField("اطلاعات بیشتر",max_length = 100,null=True,blank=True)
    PurchaseRequestAssetNotInInventory=models.CharField("ناموجود در انبار؟ اطلاعات بیشتری شرح دهید",max_length = 100,null=True,blank=True)
    #not in inventory qty
    PurchaseRequestAssetQty=models.FloatField("تعداد",null=True,blank=True)
    PurchaseRequestAssetQtyNot=models.FloatField("کمیت",null=True,blank=True)
    PurchaseRequestAssetNot=models.BooleanField("در صورت عدم تهیه تولید دچار وقفه میشود",default=False)
    PurchaseRequestNotInList=models.BooleanField(default=False)




    PurchaseRequestWO = models.ForeignKey('WorkOrder',on_delete=models.CASCADE,null=True,blank=True,related_name="ImpactedWO")
    PurchaseRequestAsset = models.ForeignKey('Asset',on_delete=models.CASCADE,null=True,blank=True,related_name="ImpactedAsset")
    PurchaseRequestDateTo = models.DateField("مهلت تا تاریخ",default=datetime.now, blank=True,null=True)
    PurchaseRequestDateFrom = models.DateField("تاریخ درخواست",default=datetime.now, blank=True,null=True)
    # PurchaseRequestDate2 = models.DateField("مهلت تا تاریخ",default=datetime.now, blank=True,null=True)
    settingTimestamp=models.DateTimeField(auto_now_add=True)
    PurchaseRequestRequestedUser = models.ForeignKey('SysUser',on_delete=models.CASCADE,verbose_name="کاربر درخواست کننده",null=True,blank=True,related_name="PurchaseRequestdUser")
    PurchaseRequestAuthUser = models.ForeignKey('SysUser',on_delete=models.CASCADE,verbose_name="کاربر مجاز",null=True,blank=True,related_name="PurchaseRequestAuthUser")
    def __str__(self):
        return self.id

    class Meta:
       db_table = "purchaserequest"
# class PurchaseRequestHistory(models.Model):
#     PurchaseRequestID=models.ForeignKey(PurchaseRequest,on_delete=models.CASCADE,null=True,blank=True)
#     PurchaseHistoryDate=models.DateTimeField(auto_now_add=True)
#     class Meta:
#        db_table = "purchaserequesthistory"
