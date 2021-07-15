from django.db import models
from datetime import datetime
from cmms.models.Asset import Asset
class PurchaseRequest(models.Model):
    PurchaseRequestAssetName=models.CharField("مشخصات",max_length = 100,null=True,blank=True)
    PurchaseRequestMoreInfo=models.CharField("اطلاعات بیشتر",max_length = 100,null=True,blank=True)
    PurchaseRequestAssetNotInInventory=models.CharField("ناموجود در انبار؟ اطلاعات بیشتری شرح دهید",max_length = 100,null=True,blank=True)
    #not in inventory qty
    PurchaseRequestAssetQty=models.FloatField("تعداد",max_length = 100,null=True,blank=True)
    PurchaseRequestNotInList=models.BooleanField(default=False)

    PurchaseRequestAssetQtyNot=models.FloatField("کمیت",max_length = 100,null=True,blank=True)
    PurchaseRequestAssetQtyNot=models.BooleanField("در صورت عدم تهیه تولید دچار وقفه میشود",default=False)

    PurchaseRequestWO = models.ForeignKey('WorkOrder',on_delete=models.CASCADE,null=True,blank=True,related_name="ImpactedWO")
    PurchaseRequestAsset = models.ForeignKey('Asset',on_delete=models.CASCADE,null=True,blank=True,related_name="ImpactedAsset")
    PurchaseRequestDate = models.DateField("مهلت تا تاریخ",default=datetime.now, blank=True,null=True)
    # PurchaseRequestDate2 = models.DateField("مهلت تا تاریخ",default=datetime.now, blank=True,null=True)
    settingTimestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id

    class Meta:
       db_table = "purchaserequest"
