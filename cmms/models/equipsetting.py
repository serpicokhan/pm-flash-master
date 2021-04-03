from django.db import models
from cmms.models.Asset import Asset
class EquipSetting(models.Model):
    EqSettingAsset = models.ForeignKey(Asset,on_delete=models.CASCADE,null=True,blank=True)
    EqSettingTimestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.EqSettingAsset.__str__()

    class Meta:
       db_table = "equipsetting"
