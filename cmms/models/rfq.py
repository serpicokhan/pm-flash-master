#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
import os
class RFQ(models.Model):
    def __str__(self):
        return "{} {}".format(self.partName,self.partCode)



    rfqQuote=models.CharField("مشخصات",max_length = 100)
    rfqSupplier=models.CharField("توضیحات",max_length = 100)
    rfqCreatedBy=models.CharField("کد",max_length = 50)

    #result related to asset and measured according to Asset

    rfqExpectedResponseTime=models.CharField("ساخته شده توسط",max_length = 100,null=True,blank=True)
    rfqExpectedDeliveryDate=models.CharField("مدل",max_length = 50,null=True,blank=True)
    partLastPrice=models.CharField("آخرین قیمت",max_length = 50,null=True,blank=True)
    partAccount=models.CharField("حساب",max_length = 100,null=True,blank=True)
    partChargeDepartment=models.CharField("دپارتمان مسوول",max_length = 100,null=True,blank=True)
    partNotes=models.CharField("یادداشت",max_length = 100)
    partBarcode=models.IntegerField("بارکد",null=True,blank=True)
    partInventoryCode=models.CharField("کد قفسه",max_length = 50,null=True,blank=True)
    class Meta:
      db_table = "parts"
