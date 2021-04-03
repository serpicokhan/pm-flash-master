#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb


##################### Asset Consuming Reference #########################
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
from cmms.models.workorder import *
from cmms.models.parts import *
from cmms.models.Asset import *
class BOM(models.Model):
    #Asset Consuming Reference
    stockItem=models.ForeignKey(Part,on_delete=models.CASCADE,verbose_name="نام قطعه")
    location=models.ForeignKey(Asset,on_delete=models.CASCADE,verbose_name="مکان")
    qnty=models.IntegerField("تعداد",null=True,blank=True)

    class Meta:
        db_table = "bom"
