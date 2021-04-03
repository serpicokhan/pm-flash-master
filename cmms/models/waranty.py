#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb


##################### Warranty #########################
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
from cmms.models.workorder import *
from cmms.models.parts import *
from cmms.models.business import *
from cmms.utils import *

class Waranty(models.Model):
    def getdate(self):
         return jdatetime.date.fromgregorian(date=self.warantyDataAdded)
    basic=1
    extended=2

    date=1
    meterReading=2
    productionTime=3



    wType=(
    (basic,"ساده"),
    (extended,"قابل تمدید")

    )
    wUsageType=(
        (date,'تاریخ'),
        (meterReading,'اندازه گیری'),
        (productionTime,'ساعت تولید')

    )
    warantyType=models.IntegerField("نوع گارانتی",choices=wType,null=True,blank=True)
    warantyProvider=models.ForeignKey(Business,on_delete=models.CASCADE,verbose_name="تامین کننده",null=True,blank=True)
    warantyUsageTermType=models.IntegerField("شرایط استفاده از گارانتی", choices=wUsageType,null=True,blank=True)
    warantyDataAdded=models.DateField(" تاریخ  ثبت",auto_now_add=True)
    warantyExpirationDate=models.DateField("تاریخ انقضا",default=datetime.now, blank=True)
    #Asset Consuming Reference
    # warantyStockItem=models.ForeignKey(Part,on_delete=models.CASCADE,verbose_name="نام قطعه",null=True,blank=True)
    warantyLocation=models.ForeignKey(Asset,on_delete=models.CASCADE,verbose_name="مکان",null=True,blank=True)
    warantyQnty=models.IntegerField("تعداد",null=True,blank=True)
    warantyMeterReadingValueLimit=models.IntegerField("مقدار محدودکننده؟؟؟",null=True,blank=True)
    warantyMeterReadingUnit=models.IntegerField ("واحد اندازه گیری",choices=Metric, null=True,blank=True)
    warantyCertificationNumber=models.CharField("شماره گواهی",max_length = 100,null=True,blank=True)
    warantyDescription=models.CharField("توضیحات",max_length = 100,null=True,blank=True)


    class Meta:
        db_table = "waranty"

class PartWaranty(models.Model):
    def getdate(self):
         return jdatetime.date.fromgregorian(date=self.warantyDataAdded)
    basic=1
    extended=2

    date=1
    meterReading=2
    productionTime=3



    wType=(
    (basic,"ساده"),
    (extended,"قابل تمدید")

    )
    wUsageType=(
        (date,'تاریخ'),
        (meterReading,'اندازه گیری'),
        (productionTime,'ساعت تولید')

    )
    warantyType=models.IntegerField("نوع گارانتی",choices=wType,null=True,blank=True)
    warantyProvider=models.ForeignKey(Business,on_delete=models.CASCADE,verbose_name="تامین کننده",null=True,blank=True)
    warantyUsageTermType=models.IntegerField("شرایط استفاده از گارانتی", choices=wUsageType,null=True,blank=True)
    warantyDataAdded=models.DateField(" تاریخ  ثبت",auto_now_add=True)
    warantyExpirationDate=models.DateField("تاریخ انقضا",default=datetime.now, blank=True)
    #Asset Consuming Reference
    warantyStockItem=models.ForeignKey('Part',on_delete=models.CASCADE,verbose_name="نام قطعه",null=True,blank=True)

    warantyQnty=models.IntegerField("تعداد",null=True,blank=True)
    warantyMeterReadingValueLimit=models.IntegerField("مقدار محدودکننده؟؟؟",null=True,blank=True)
    warantyMeterReadingUnit=models.IntegerField ("واحد اندازه گیری",choices=Metric, null=True,blank=True)
    warantyCertificationNumber=models.CharField("شماره گواهی",max_length = 100,null=True,blank=True)
    warantyDescription=models.CharField("توضیحات",max_length = 100,null=True,blank=True)


    class Meta:
        db_table = "partwaranty"
