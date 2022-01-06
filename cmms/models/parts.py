#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
import os
class Part(models.Model):
    def __str__(self):
        return "[{}]{}".format(self.partCode,self.partName)
    partName=models.CharField("مشخصات",max_length = 100)
    partDescription=models.CharField("توضیحات",max_length = 100)
    partCode=models.CharField("کد",max_length = 50)
    partCategory=models.ForeignKey('PartCategory',on_delete=models.CASCADE,verbose_name="دسته بندی",null=True,blank=True,related_name='dasdadassa')
    #result related to asset and measured according to Asset
    partMake=models.CharField("ساخته شده توسط",max_length = 100,null=True,blank=True)
    partModel=models.CharField("مدل",max_length = 50,null=True,blank=True)
    partLastPrice=models.FloatField("آخرین قیمت",default=0,null=True,blank=True)
    partAccount=models.CharField("حساب",max_length = 100,null=True,blank=True)
    partChargeDepartment=models.CharField("دپارتمان مسوول",max_length = 100,null=True,blank=True)
    partNotes=models.CharField("یادداشت",max_length = 100,null=True,blank=True)
    partBarcode=models.IntegerField("بارکد",null=True,blank=True)
    partInventoryCode=models.CharField("کد قفسه",max_length = 50,null=True,blank=True)
    class Meta:
      db_table = "parts"
class PartUser(models.Model):
          PartUserPartId=models.ForeignKey(Part,on_delete=models.CASCADE,blank=True,null=True,verbose_name="قطعه")
          PartUserUserId=models.ForeignKey(SysUser,on_delete=models.CASCADE,blank=True,null=True,verbose_name="کاربر ")
          class Meta:
              db_table="partuser"


class PartFile(models.Model):
    def get_ext(self):
        v=os.path.splitext(self.partFile.name)
        return v[len(v)-1]
    def get_size(self):
        return " MB {0:.2f}".format(self.partFile.size/1048576)

    partFile=models.FileField(upload_to='documents/',max_length=200)
    partFilePartId=models.ForeignKey('Part',on_delete=models.CASCADE,blank=True,null=True)
    partFiledateAdded=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="partfile"
class PartCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField("نام",max_length = 50)
    code=models.CharField("کد",max_length = 50,unique=True)
    description=models.CharField("توضیحات",max_length = 50)
    priority=models.IntegerField("اولویت", null=True)

    isPartOf = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name="زیر مجموعه",null=True,blank=True)
    def __str__(self):
        return self.name

    class Meta:
       db_table = "partcategory"
