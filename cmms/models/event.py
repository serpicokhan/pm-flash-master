from django.db import models

class Events(models.Model):
    def __str__(self):
        return '{}:{}'.format(self.Code,self.name)
    Code=models.CharField("کد رویداد",max_length=50,blank=True,null=True)
    name=models.CharField("نام رویداد",max_length=50,blank=True,null=True)
    description=models.CharField("توضیح",max_length=50,blank=True,null=True)
    class Meta:
        db_table="events"
