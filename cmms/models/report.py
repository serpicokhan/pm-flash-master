#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb


##################### Asset Consuming Reference #########################
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now

class Report(models.Model):
    open_work_order=1
    close_work_order=2
    inventory_control=3
    asset_report=4
    user_report=5
    business_metric=6
    customr_report=7
    forecasting_report=8
    scheduled_maintenance=9

    Category=(
        (open_work_order,'دستور کار فعال'),
        (close_work_order,'دستور کار غیر فعال'),
        (inventory_control,'کنترل انبار'),
        (asset_report,'دارایی'),
        (user_report,'کاربران'),
        (business_metric,'اندازه گیری کسب و کار'),
        (customr_report,'شخصی سازی شده'),
        (forecasting_report,'پیش بینی'),
        (scheduled_maintenance,'نگهداری زمانبندی شده'),
    )
    #Asset Consuming Reference
    reportName=models.CharField("نام گزارش",max_length = 100,null=True,blank=True)
    reportCategory=models.IntegerField("نوع گزارش", choices=Category,null=True,blank=True)
    reportClassName=models.CharField("نام کلاس",max_length = 100,null=True,blank=True)
    reportDetails=models.TextField("شرح",null=True,blank=True)
    reportTemplate=models.CharField("نام قالب",max_length = 100,null=True,blank=True)
    reportFav=models.BooleanField("گزارش مورد علاقه",default=True)
    timeStamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.reportName
    class Meta:
        db_table = "reports"
        # permissions = (
        #     ("can_", "Can drive"),
        #     ("can_vote", "Can vote in elections"),
        #     ("can_drink", "Can drink alcohol"),
        # )
