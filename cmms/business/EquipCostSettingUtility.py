from cmms.models import EquipmentCostSetting
import jdatetime
import datetime
from decimal import Decimal
import locale
class EquipCostSettingUtility:

    @staticmethod
    def getList():
        return EquipmentCostSetting.objects.values_list('settingEqAsset',flat=True)
    def getListByName():
        return EquipmentCostSetting.objects.all()
