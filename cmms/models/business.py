from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now

from cmms.models.Asset import *
from cmms.models.parts import *
from cmms.models.users import *

class Business(models.Model):
    def __str__(self):
         return "{}:{}".format(self.code,self.name)
    name=models.CharField("نام",max_length = 50)
    code=models.CharField("کد",max_length = 50)
    primaryContact=models.CharField("مشخصات تماس",max_length = 100,null=True,blank=True)
    phone=models.CharField("تلفن",max_length = 50,null=True,blank=True)
    phone2=models.CharField("تلفن 2",max_length = 50,null=True,blank=True)
    fax=models.CharField("فکس",max_length = 50,null=True,blank=True)
    webSite=models.CharField("سایت",max_length = 50,null=True,blank=True)
    primaryEmail=models.CharField("ایمیل اصلی",max_length = 50,null=True,blank=True)
    secondyEmail=models.CharField("ایمیل 2",max_length = 50,null=True,blank=True)
    primaryCurrency=models.CharField("واحد پول",max_length = 50,null=True,blank=True)
    notes=models.CharField("یادداشت",max_length = 100,null=True,blank=True)
    isSupplier=models.BooleanField("تامین کننده",default=False)
    insManufacturer=models.BooleanField("سازننده",default=False)
    isServiceProvider=models.BooleanField("سرویس پروایدر",default=False)
    isOwner=models.BooleanField("مالک",default=False)
    isCustomer=models.BooleanField("مشتری",default=False)
    address=models.CharField("آدرس",max_length = 100,null=True,blank=True)
    city=models.CharField("شهر",max_length = 50,null=True,blank=True)
    state=models.CharField("استان",max_length = 50,null=True,blank=True)
    postalCode=models.CharField("کد پستی",max_length = 50,null=True,blank=True)
    country=models.CharField("کشور",max_length = 100,null=True,blank=True)
    class Meta:
        db_table="business"
class BusinessFile(models.Model):
   def get_ext(self):
       v=os.path.splitext(self.businessFile.name)
       return v[len(v)-1]
   def get_size(self):
       return " MB {0:.2f}".format(self.businessFile.size/1048576)

   businessFile=models.FileField(upload_to='documents/')
   businessFileBusinessId=models.ForeignKey('Business',on_delete=models.CASCADE,blank=True,null=True)
   businessFiledateAdded=models.DateTimeField(auto_now_add=True)

   class Meta:
        db_table="businessfiles"

class BusinessAsset(models.Model):
    BusinessAssetAsset= models.ForeignKey('Asset',on_delete=models.CASCADE,verbose_name="نام دارایی",null=True,blank=True)
    Supplier=0
    Manufacture=1
    ServiceProvider=2
    Owner=3
    Customer=4

    BType=(
    (Supplier,"تامین کننده"),
    (Manufacture,"سارننده"),
    (ServiceProvider,"خدماتی"),
    (Owner,"مالک"),
    (Customer,"مشتری")

    )
    def get_assetBusinessIsDefault(self):
             if(self.businessAssetisDefault==True):
                 return "<i class='fa fa-check'>										</i>								"
             else:
                 return "<i class='fa fa-times'> </i>"

    businessAssetBusiness= models.ForeignKey(Business,on_delete=models.CASCADE,verbose_name="کسب و کار",null=True,blank=True)
    businessAssetBusinessType=models.IntegerField("نوع کسب و کار",choices=BType,blank=True,null=True)
    businessAssetSupplierPartNumber=models.CharField("پارت نامبر تامین کننده",max_length=100,blank=True,null=True)
    businessAssetCatalog=models.CharField("دسته بندی",max_length=100,blank=True,null=True)
    businessAssetisDefault=models.BooleanField("تامین کننده مورد علاقه",default=False)
    businessAssetVendorPrice=models.FloatField("قیمت تامین کننده",null=True,blank=True)
    class Meta:
        db_table="businessasset"

class BusinessPart(models.Model):

    BusinessPartPart= models.ForeignKey('Part',on_delete=models.CASCADE,verbose_name="نام قطعه",null=True,blank=True)
    Supplier=0
    Manufacture=1
    ServiceProvider=2
    Owner=3
    Customer=4

    BType=(
    (Supplier,"تامین کننده"),
    (Manufacture,"سارننده"),
    (ServiceProvider,"خدماتی"),
    (Owner,"مالک"),
    (Customer,"مشتری")

    )
    def get_partBusinessIsDefault(self):
             if(self.businessPartisDefault==True):
                 return "<i class='fa fa-check'>										</i>								"
             else:
                 return "<i class='fa fa-times'> </i>"

    businessPartBusiness= models.ForeignKey(Business,on_delete=models.CASCADE,verbose_name="تامین کننده",null=True,blank=True)
    businessPartBusinessType=models.IntegerField("نوع کسب و کار",choices=BType,blank=True,null=True)
    businessPartSupplierPartNumber=models.CharField("پارت نامبر تامین کننده",max_length=100,blank=True,null=True)
    businessPartCatalog=models.CharField("دسته بندی",max_length=100,blank=True,null=True)
    businessPartisDefault=models.BooleanField("تامین کننده مورد علاقه",default=False)
    businessPartVendorPrice=models.FloatField("قیمت تامین کننده",null=True,blank=True)
    class Meta:
        db_table="businesspart"


class BusinessUser(models.Model):
    user= models.ForeignKey('Part',on_delete=models.CASCADE,verbose_name="نام قطعه",null=True,blank=True)
    business= models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="پرسنل",null=True,blank=True)
    class Meta:
        db_table="businessuser"
