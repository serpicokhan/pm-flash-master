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
from cmms.models.business import *
class Stock(models.Model):
    def __str__(self):
        return "{}#{}".format(self.stockItem,self.location)
    def getmin(self):
        return self.minQty-self.qtyOnHand
    def getlastprice(self):
        return 1
    def getTotalPrice(self):
        return self.getmin()*self.getlastprice()
    def get_fav_suplier(self):
        # (BusinessPart.objects.filter(BusinessPartPart=self.stockItem,businessPartisDefault=True)[:1],"kir khar")
        try:
            wo= BusinessPart.objects.filter(BusinessPartPart=self.stockItem,businessPartisDefault=True)
            return wo[0].businessPartBusiness.name
        except:
            return "بدون تامین کننده منتخب"
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
