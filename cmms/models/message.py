from django.db import models
from cmms.models import SysUser
from datetime import datetime
from django.utils.timezone import now
import jdatetime
class Message(models.Model):
    read=3
    unread=2
    MessageStatus=(
    (read,'read'),
    (unread,'unread')
    )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
        (Highest,'خیلی زیاد'),
        (High,'زیاد'),
        (Medium,'متوسط'),
        (Low,'پایین'),
        (Lowest,'خیلی پایین'),
    )
    def getdate(self):
        if self.sentTime.date()==datetime.now():
            return "{}".format(self.datetime.time())
        else:
            return jdatetime.date.fromgregorian(date=self.sentTime)
    msgPririty=models.IntegerField("پیامهای سیستمی",choices=Priority,null=True,blank=True)
    messageStatus=models.IntegerField("وضعیت",choices=MessageStatus)
    sentTime=models.DateTimeField(auto_now_add=True)
    fromUser=models.ForeignKey(SysUser,on_delete=models.CASCADE,related_name="fromuser",verbose_name="از:")
    toUser=models.ForeignKey(SysUser,on_delete=models.CASCADE,related_name="touser",verbose_name="به:")
    subject=models.CharField("موضوع",max_length=200,blank=True,null=True)
    Message=models.TextField(null=True,blank=True)
    workOrder=models.ForeignKey('WorkOrder',on_delete=models.CASCADE,related_name="workordermsg",verbose_name="به:",null=True,blank=True)
    class Meta:
        db_table="message"
