#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
from cmms.models.workorder import *
from cmms.models.parts import *
from cmms.models.Asset import *
class Stock(models.Model):
    def __str__(self):
        return "{}#{}".format(self.location,self.stockItem)
    stockItem=models.ForeignKey(Part,on_delete=models.CASCADE,verbose_name="نام قطعه")
    location=models.ForeignKey('Asset',on_delete=models.CASCADE,verbose_name="مکان")
    qtyOnHand=models.IntegerField("موجودی",null=True,blank=True)
    minQty=models.IntegerField("حداقل موجودی",null=True,blank=True)
    aisle=models.IntegerField("راهرو",null=True,blank=True)
    row=models.IntegerField("ردیف",null=True,blank=True)
    bin=models.IntegerField("قفسه",null=True,blank=True)




    class Meta:
      db_table = "stocks"
      unique_together = ('stockItem', 'location')
