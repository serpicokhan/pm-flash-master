from django.db import models
from cmms.models.Asset import Asset
class AdminSetting(models.Model):
    settingAsset = models.ForeignKey(Asset,on_delete=models.CASCADE,null=True,blank=True)
    settingTimestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.settingAsset.__str__()

    class Meta:
       db_table = "adminsetting"
