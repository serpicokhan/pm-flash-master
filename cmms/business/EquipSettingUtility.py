from cmms.models import EquipSetting,AssetTypeSetting
import jdatetime
import datetime
from decimal import Decimal
import locale
class EquipSettingUtility:

    @staticmethod
    def getList():
        # print("kirekhar$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # print(EquipSetting.objects.values_list('EqSettingAsset',flat=True))
        return EquipSetting.objects.values_list('EqSettingAsset',flat=True)
class AssetTypeUtility:

    @staticmethod
    def getList():
        # print("kirekhar$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # print(EquipSetting.objects.values_list('EqSettingAsset',flat=True))
        return AssetTypeSetting.objects.all()
