from cmms.models import AdminSetting
import jdatetime
import datetime
from decimal import Decimal
import locale
class AdminSettingUtility:

    @staticmethod
    def getList():
        return AdminSetting.objects.values_list('settingAsset',flat=True)
