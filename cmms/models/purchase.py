from django.db import models
from datetime import datetime


from cmms.models.Asset import *
from cmms.models.business import *
from cmms.models.users import *
from cmms.models import *
import jdatetime
from django.utils.timezone import now
from cmms.utils import *
class Purchase(models.Model):
    def __str__(self):
         return "R#{}".format(self.id)
    purchaseDateOrdered=models.DateField("تاریخ سفارش",blank=True,null=True,default=datetime.now)
    purchasePriceTotla=models.FloatField("قیمت تمام شده",blank=True,null=True)
    purchaseCurrency=models.IntegerField("واحد پول",choices=currency,blank=True,null=True)
    purchaseDateRecieved=models.DateField("تاریخ دریافت",blank=True,null=True)
    purchaseDateofExpire=models.DateField("تاریخ انقضا",blank=True,null=True)
    purchaseAssetId=models.ForeignKey('Asset',on_delete=models.CASCADE,null=True,blank=True,verbose_name="دارایی")
    purchaseUser=models.ForeignKey('SysUser',on_delete=models.CASCADE,blank=True,null=True,verbose_name="کاربر درخواست کننده")
    purchasedFrom = models.ForeignKey('Business',on_delete=models.CASCADE,verbose_name="خرید از",null=True,blank=True)

    class Meta:
        db_table="purchase"
class PartPurchase(models.Model):
    def __str__(self):
         return "R#{}".format(self.id)
    def getDateRecieved(self):
        if(self.purchaseDateRecieved):
            return jdatetime.date.fromgregorian(date=self.purchaseDateRecieved)
        return ""
    def getDateOrdered(self):
        if(self.purchaseDateOrdered):
            return jdatetime.date.fromgregorian(date=self.purchaseDateOrdered)
        return ""
    def getDateofExpire(self):
        if(self.purchaseDateofExpire):
            return jdatetime.date.fromgregorian(date=self.purchaseDateofExpire)
        return ""
    purchaseDateOrdered=models.DateField("تاریخ سفارش",blank=True,null=True,default=datetime.now)
    purchasePriceTotla=models.FloatField("قیمت تمام شده",default=0.0,blank=True,null=True)
    purchaseCurrency=models.IntegerField("واحد پول",choices=currency,blank=True,null=True)
    purchaseDateRecieved=models.DateField("تاریخ دریافت",blank=True,null=True)
    purchaseDateofExpire=models.DateField("تاریخ انقضا",blank=True,null=True)
    purchasePartId=models.ForeignKey('Part',on_delete=models.CASCADE,null=True,blank=True,verbose_name="قطعه")
    purchaseUser=models.ForeignKey('SysUser',on_delete=models.CASCADE,blank=True,null=True,verbose_name="کاربر درخواست کننده")
    purchasedFrom = models.ForeignKey('Business',on_delete=models.CASCADE,verbose_name="خرید از",null=True,blank=True)
    purchaseQuantityReceived=models.FloatField("تعداد",default=0.0)
    purchasePricePerUnit=models.FloatField("قیمت واحد",default=0.0)
    purchaseStock=models.ForeignKey('Asset',on_delete=models.CASCADE,blank=True,null=True,verbose_name="انبار قطعه")

    class Meta:
        db_table="partpurchase"
