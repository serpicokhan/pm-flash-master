from django.db import models
from datetime import datetime
from cmms.models import Asset,AssetLife
from cmms.models import SysUser
import jdatetime
Shift=(

    ('A','A'),
    ("B" ,'B'),
    ('C','C'),

)
class RingAmar(models.Model):

    def has_downtime(self):
        asset_code=AssetLife.objects.filter(assetLifeAssetid=self.assetName,assetOfflineFrom=self.assetAmarDate)
        print('count',asset_code.count())
        if(asset_code.count()>0):
            return True
        return False

    ShiftTypes=models.CharField("شیفت", choices=Shift,max_length=1,null=True,blank=True)
    assetName=models.ForeignKey(Asset,on_delete=models.CASCADE,null=True,blank=True,verbose_name="تجهیز",related_name='ringAmar')
    assetStartKilometer=models.DecimalField("کیلومتر پایان شیفت قبل",max_digits=15, decimal_places=3,default=0)
    assetEndKilometer=models.DecimalField("کیلومتر پایان شیفت جاری",max_digits=15, decimal_places=3,default=0)
    assetTotlaKilometer=models.DecimalField("کیلومتر تولید",max_digits=15, decimal_places=3,default=0)
    assetStartTime=models.DecimalField("ساعت پایان شیفت قبل",max_digits=10, decimal_places=3,default=0)
    assetEndTime=models.DecimalField("ساعت پایان شیفت جاری",max_digits=10, decimal_places=3,default=0)
    assetTotalTime=models.DecimalField("ساعت تولید",max_digits=10, decimal_places=3,default=0)
    assetDarsad=models.FloatField("درصد",default=0)
    assetDaf=models.IntegerField("داف",default=0)
    operatorName=models.CharField("نام اپراتور",max_length=100)
    assetAmarDate=models.DateField("تاریخ",default=datetime.now,blank=True,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    userRegisterd=models.ForeignKey(SysUser,on_delete=models.CASCADE,blank=True,null=True,verbose_name="کاربر ثبت کننده")
    def get_jalali(self):
        if(self.assetAmarDate):
            return jdatetime.date.fromgregorian(date=self.assetAmarDate)
        return "بدون تاریخ"

    class Meta:
      db_table = "ringamar"
      ordering = ('-assetAmarDate','-ShiftTypes','-id' )
      unique_together = ['ShiftTypes', 'assetName','assetAmarDate']



class TolidMoshakhase(models.Model):
    mogheiat = models.CharField("موقعیت",max_length=255,unique=True)
    keyfiat = models.CharField("کیفیت",max_length=255)
    vaziat = models.CharField("وضعیت",max_length=255)

    def __str__(self):
        return f"mogheiat: {self.mogheiat}, keyfiat: {self.keyfiat}, vaziat: {self.vaziat}"
    class Meta:
        db_table = "tolidmoshakhase"
class TolidAmar(models.Model):
    # Foreign key to the MyModel model
    tolidmoshakhase = models.ForeignKey('TolidMoshakhase', on_delete=models.CASCADE,null=True)

    # Location field as a ForeignKey (You can replace 'LocationModel' with the actual model name)
    location = models.ForeignKey('Asset', on_delete=models.CASCADE)

    registered_date = models.DateField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tedad = models.FloatField(null=True)
    meghdar = models.FloatField(null=True)
    isheatset = models.BooleanField(null=True)

    def get_jalali(self):
        if(self.registered_date):
            return jdatetime.date.fromgregorian(date=self.registered_date)
        return "بدون تاریخ"

    def __str__(self):
        return f"TolidMara ({self.id}) - Date: {self.registered_date}, Tedad: {self.tedad}, Meghdar: {self.meghdar}"
    class Meta:
        db_table="tolidamar"
