from django.db import models
from datetime import datetime
from cmms.models import Asset
from cmms.models import SysUser
Shift=(

    ('A','A'),
    ("B" ,'B'),
    ('C','C'),

)
class RingAmar(models.Model):
    ShiftTypes=models.IntegerField("شیفت", choices=Shift,null=True,blank=True)
    assetName=models.ForeignKey(Asset,on_delete=models.CASCADE,null=True,blank=True,verbose_name="انبار",related_name='ringAmar')
    assetStartKilometer=models.DecimalField("کیلومتر شروع",max_digits=10, decimal_places=0,default=0)
    assetEndKilometer=models.DecimalField("کیلومتر پایان",max_digits=10, decimal_places=0,default=0)
    assetTotlaKilometer=models.DecimalField("کیلومتر تولید",max_digits=10, decimal_places=0,default=0)
    assetStartTime=models.DecimalField("ساعت پایان شیفت قبل",max_digits=10, decimal_places=0,default=0)
    assetEndTime=models.DecimalField("ساعت پایان شیفت جاری",max_digits=10, decimal_places=0,default=0)
    assetTotalTime=models.DecimalField("ساعت تولید",max_digits=10, decimal_places=0,default=0)
    assetDarsad=models.FloatField("درصد",default=0)
    assetDaf=models.IntegerField("داف",default=0)
    operatorName=models.CharField("نام اپراتور",max_length=100)
    assetAmarDate=models.DateField("تاریخ",default=datetime.now,blank=True,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    userRegisterd=models.ForeignKey(SysUser,on_delete=models.CASCADE,blank=True,null=True,verbose_name="کاربر ثبت کننده")
