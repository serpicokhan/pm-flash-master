from django.db import models
from cmms.models.Asset import Asset,AssetCategory
class EquipmentCostSetting(models.Model):
    settingEqAsset = models.ForeignKey(Asset,on_delete=models.CASCADE,null=True,blank=True)
    settingEqTimestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.settingEqAsset.__str__()

    class Meta:
       db_table = "equipmentcostSetting"
class AssetTypeSetting(models.Model):
    settingEqAsset = models.ForeignKey(AssetCategory,verbose_name='دسته دارایی',on_delete=models.CASCADE,null=True,blank=True)
    settingLocation = models.ForeignKey('Asset',on_delete=models.CASCADE,null=True,blank=True,verbose_name='مکان')
    settingEqTimestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.settingEqAsset.__str__()

    class Meta:
       db_table = "assettypesetting"
       unique_together = ('settingEqAsset', 'settingLocation')
