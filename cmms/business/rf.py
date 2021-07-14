from cmms.models.parts import *
from cmms.models.business import *
class RFUtility():
    @staticmethod
    def getSupplier():
        return Business.objects.all()
