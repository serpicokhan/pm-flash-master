from django.db import models
from cmms.models.workorder import MaintenanceType
class KpiException(models.Model):
    stopcode = models.ForeignKey('StopCode',on_delete=models.CASCADE,unique=True,verbose_name='کد توقف')
    # stopCode1=models.CharField("کد توقف",max_length = 100,null=True,blank=True,unique=True)

    def __str__(self):
        return self.stopcode.__str__()

    class Meta:
       db_table = "kpiexception"
