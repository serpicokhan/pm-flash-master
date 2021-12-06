#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
from cmms.models.workorder import *
from cmms.models.assetcategory import *
from cmms.models.event import *
from cmms.models.machinecategory import *
from cmms.utils import *
from cmms.models.purchase import *
from cmms.models.stock import *
from django.db.models import Count
from django.db.models import Q

class Asset(models.Model):
    def __str__(self):
        if(self.assetIsLocatedAt):
            return "{}-{}-{}".format(self.assetName,self.assetCode if (self.assetCode != None) else 'فاقد کد',self.assetIsLocatedAt.assetName)
        return "{}-{}-{}".format(self.assetName,self.assetCode if (self.assetCode != None) else 'فاقد کد',"بدون مکان")
    def get_location(self):
        if(self.assetIsLocatedAt):

            return "{}".format(self.assetIsLocatedAt)
        else:
            return "-"
    def get_child(self):
        return Asset.objects.filter(Q(assetIsLocatedAt=self.id)|Q(assetIsPartOf=self.id))
    def get_name(self):
        if(self.assetName):
            return "{}:{}".format(self.assetName,self.assetCode)
        return "مشخص نشده"
    def get_assetStatus(self):
                 if(self.assetStatus==True):
                     return "<i class='fa fa-play'></i>								"
                 else:
                     return "<i class='fa fa-stop'></i>"
    def get_assetid(self):

                 return self.assetIsLocatedAt.id

    Location=1
    Equipment=2
    Tool=3


    AssetType=(

        (Location,'مکان'),
        (Equipment ,'ماشین  آلات'),
        (Tool,'ابزارآلات'),

    )

    assetTypes=models.IntegerField("نوع دارایی", choices=AssetType,null=True,blank=True)
    assetName=models.CharField("مشخصات",max_length = 100)
    assetDescription=models.CharField("توضیحات",max_length = 100,null=True,blank=True)
    assetCode=models.CharField("کد",max_length = 50,null=True,blank=True)
    assetIsPartOf = models.ForeignKey('self',on_delete=models.SET_NULL,verbose_name="زیر مجموعه",null=True,blank=True)
    assetIsLocatedAt = models.ForeignKey('self',on_delete=models.SET_NULL,verbose_name="مکان",null=True,blank=True,related_name="location")
    assetCategory=models.ForeignKey(AssetCategory,on_delete=models.SET_NULL,verbose_name="دسته بندی",null=True,blank=True)
    #result related to asset and measured according to Asset

    assetAddress=models.CharField("آدرس",max_length = 100,null=True,blank=True)
    assetCity=models.CharField("شهر",max_length = 50,null=True,blank=True)
    assetState=models.CharField("استان",max_length = 50,null=True,blank=True)
    assetZipcode=models.CharField("کد پستی",max_length = 50,null=True,blank=True)
    assetCountry=models.CharField("کشور",max_length = 100,null=True,blank=True)
    assetAccount=models.CharField("حساب",max_length = 100,null=True,blank=True)
    assetChargeDepartment=models.CharField("دپارتمان مسوول",max_length = 100,null=True,blank=True)
    assetNotes=models.CharField("یادداشت",max_length = 100,null=True,blank=True)
    assetBarcode=models.IntegerField("بارکد",null=True,blank=True)
    assetHasPartOf=models.BooleanField(default=False)
    assetAisel=models.IntegerField("راهرو",null=True,blank=True)
    assetRow=models.IntegerField("ردیف",null=True,blank=True)
    assetBin=models.IntegerField("Bin",null=True,blank=True)
    assetManufacture=models.CharField("سازنده",max_length = 50,null=True,blank=True)
    assetModel=models.CharField("مدل",max_length = 50,null=True,blank=True)
    assetSerialNumber=models.CharField("شماره سریال",max_length = 50,null=True,blank=True)
    assetStatus=models.BooleanField("وضعیت",default=True)
    assetMachineCategory=models.ForeignKey(MachineCategory,on_delete=models.CASCADE,null=True,blank=True,verbose_name="نوع دستگاه")
    assetIsStock=models.BooleanField("انبار",default=False)






    class Meta:
      db_table = "assets"
class AssetMeterReading(models.Model):
    def getRow(self):
         return "{} {}".format(self.assetMeterMeterReading,self.assetMeterMeterReadingUnit)
    def getdate(self):
        return jdatetime.date.fromgregorian(date=self.timestamp)
    assetMeterLocation=models.ForeignKey(Asset,on_delete=models.CASCADE,blank=True,null=True,verbose_name="دارایی")
    assetMeterMeterReading=models.FloatField("meter reading",default=0.00)
    assetMeterMeterReadingUnit=models.ForeignKey("MeterCode",verbose_name="واحد اندازه گیری",on_delete=models.CASCADE,null=True,blank=True)
    assetWorkorderMeterReading=models.ForeignKey("WorkOrder",on_delete=models.CASCADE,blank=True,null=True,verbose_name="درخواست")
    timestamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="assetmeterreading"


class AssetUser(models.Model):
        AssetUserAssetId=models.ForeignKey(Asset,on_delete=models.CASCADE,blank=True,null=True,verbose_name="دارایی")
        AssetUserUserId=models.ForeignKey(SysUser,on_delete=models.CASCADE,blank=True,null=True,verbose_name="کاربر ")
        class Meta:
            db_table="assetuser"
class AssetEvent(models.Model):
    def getdate(self):
        return jdatetime.date.fromgregorian(date=self.AssetEventDateSubmitted)
    AssetEventEventId=models.ForeignKey(Events,on_delete=models.CASCADE,verbose_name="نوع رویداد",blank=True,null=True)
    AssetEventAssetId=models.ForeignKey(Asset,on_delete=models.CASCADE,blank=True,null=True,verbose_name="دارایی")
    AssetEventAdditionalDescription=models.CharField("توضیحات تکمیلی",max_length=50,blank=True,null=True)
    AssetEventDateSubmitted=models.DateField("تاریخ ارسال",auto_now_add=True)
    class Meta:
        db_table="assetevent"

class AssetFile(models.Model):
    def get_ext(self):
        v=os.path.splitext(self.assetFile.name)
        return v[len(v)-1]
    def get_size(self):
        return " MB {0:.2f}".format(self.assetFile.size/1048576)

    assetFile=models.FileField(upload_to='documents/',max_length=200)
    assetFileAssetId=models.ForeignKey('Asset',on_delete=models.CASCADE,blank=True,null=True)
    assetFiledateAdded=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="assetfile"
class BOMGroup(models.Model):
    def __str__(self):
        return '{}:{}'.format(self.BOMGroupName)
    def getPartNUM(self):
        return BOMGroupPart.objects.filter(BOMGroupPartBOMGroup=self).count()
    BOMGroupName=models.CharField("نام گروه BOM",max_length=50,unique=True)
    class Meta:

        db_table="bomgroup"
class BOMGroupPart(models.Model):
    def __str__(self):
        return '{}:{}'.format(self.BOMGroupPartBOMGroup)
    BOMGroupPartPart=models.ForeignKey('Part',verbose_name="قطعه",on_delete=models.CASCADE,blank=True,null=True)
    BOMGroupPartBOMGroup=models.ForeignKey('BOMGroup',verbose_name="گروه",on_delete=models.CASCADE,blank=True,null=True)
    BOMGroupPartQnty=models.IntegerField("تعداد",blank=True,null=True)
    class Meta:

        db_table="bomgrouppart"
        unique_together = ('BOMGroupPartPart', 'BOMGroupPartBOMGroup')
class BOMGroupAsset(models.Model):
    def __str__(self):
        return '{}:{}'.format(self.BOMGroupName)
    BOMGroupAssetAsset=models.ForeignKey('Asset',verbose_name="دارایی",on_delete=models.CASCADE,blank=True,null=True)
    BOMGroupAssetBOMGroup=models.ForeignKey('BOMGroup',verbose_name="گروه",on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        db_table="bomgroupasset"
        unique_together = ('BOMGroupAssetAsset', 'BOMGroupAssetBOMGroup')

class AssetPart(models.Model):
    #for knowing which asset is consist of what parts
    #asset id
    assetPartAssetid=models.ForeignKey(Asset,verbose_name="نام دارایی",on_delete=models.CASCADE,blank=True,null=True)
    #part id
    assetPartPid=models.ForeignKey(Part,verbose_name="نام قطعه",on_delete=models.CASCADE,blank=True,null=True)
    assetPartBOMGroupName=models.ForeignKey('BOMGroup',verbose_name="گروه",on_delete=models.CASCADE,blank=True,null=True)
    assetPartQnty=models.IntegerField("تعداد",blank=True,null=True)
    # assetPartStock=models.ForeignKey(Stock,on_delete=models.CASCADE,null=True,blank=True,verbose_name="انبار",related_name='cc2')
    # timeStamp=models.DateTimeField(auto_now_add=True)
    class Meta:

        db_table="assetpart"
class OfflineStatus(models.Model):
    def __str__(self):
        return '{}:{}'.format(self.Code,self.name)
    Code=models.CharField("کد رویداد",max_length=50,blank=True,null=True)
    name=models.CharField("نام رویداد",max_length=50,blank=True,null=True)
    description=models.CharField("توضیح",max_length=50,blank=True,null=True)
    class Meta:
        db_table="offlinestatus"

class AssetLife(models.Model):
    Broken=0
    inStorage=1
    Idle=2
    Retired=3
    underRepair=4
    Unknown=-1
    inProduction=0
    onStandBy=1
    def getdate(self):
        if(self.assetOfflineFrom):
            return jdatetime.date.fromgregorian(date=self.assetOfflineFrom)
        return " "
    def getonlinedate(self):
        if(self.assetOnlineFrom):
            return jdatetime.date.fromgregorian(date=self.assetOnlineFrom)


        return ""

    def getAffectedHour(self):
        d1=datetime.combine(self.assetOfflineFrom,self.assetOfflineFromTime)
        d2=datetime.combine(self.assetOnlineFrom,self.assetOnlineFromTime)
        # return "{0:.2f}".format((d2-d1).total_seconds()/3600)
        d3=(d2-d1).total_seconds()/3600
        return '{0:02.0f}:{1:02.0f}'.format(*divmod(d3 * 60, 60))
    def getAffectedHour_digits(self):
        d1=datetime.combine(self.assetOfflineFrom,self.assetOfflineFromTime)
        d2=datetime.combine(self.assetOnlineFrom,self.assetOnlineFromTime)
        return ((d2-d1).total_seconds()/3600)






    AssetOfflineStatu=((Broken,'خراب'),(inStorage,'در انبار'),(Retired,'از کارافتاده'),(underRepair,'در دست تعمیر'),(Idle,'بیکار'))
    AssetOnlineStatu=((inProduction,'در حال تولید'),(onStandBy,'آماده به کار'))
    assetLifeAssetid=models.ForeignKey(Asset,verbose_name="نام دارایی",on_delete=models.CASCADE,blank=True,null=True)
    assetOfflineFrom=models.DateField("تاریخ خاموشی",default=datetime.now,blank=True,null=True)
    assetOfflineFromTime=models.TimeField("زمان خاموشی",default=datetime.now,blank=True,null=True)
    assetSetOfflineByUser=models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="کاربر",blank=True,null=True,related_name="offlineUser")
    assetOfflineStatus=models.ForeignKey(OfflineStatus,on_delete=models.CASCADE,verbose_name="وضعیت",blank=True,null=True)
    assetWOAssoc=models.ForeignKey('WorkOrder',verbose_name="درخواست مرتبط",on_delete=models.CASCADE,blank=True,null=True)
    assetOfflineAdditionalInfo=models.TextField("اطلاعات اضافی",blank=True,null=True)
    assetEventType=models.ForeignKey(Events,verbose_name="نوع رویداد",on_delete=models.CASCADE,blank=True,null=True)
    assetEventDescription=models.TextField("شرح رویداد",blank=True,null=True)
    ############Online#########
    assetOnlineFrom=models.DateField("تاریخ شروع",default=datetime.now,blank=True,null=True)
    assetOnlineFromTime=models.TimeField("زمان شروع",default=datetime.now,blank=True,null=True)
    assetSetOnlineByUser=models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="کاربر",blank=True,null=True,related_name="onlineUser")
    assetOnlineStatus=models.IntegerField("وضعیت",choices=AssetOnlineStatu,blank=True,null=True)
    assetOnlineAdditionalInfo=models.TextField("اطلاعات اضافی",blank=True,null=True)
    assetOnlineProducteHourAffected=models.IntegerField("ساعت وقفه در تولید",default=0,blank=True,null=True)
    # ######################## Check for create event in time of fault ######################\
    assetCheckEvent=models.BooleanField("ایجاد رویداد",default=False)
    assetStopCode=models.ForeignKey('StopCode',on_delete=models.CASCADE,verbose_name="کد توقف",null=True,blank=True,related_name="assetStopCode")
    #assetCheckEvent2=models.BooleanField("ایجاد رویداد",default=False)
    assetCauseCode = models.ForeignKey('CauseCode',on_delete=models.CASCADE,verbose_name="کد علت",null=True,blank=True,related_name="assetlifeCauseCode")
    class Meta:
        db_table="assetlife"
