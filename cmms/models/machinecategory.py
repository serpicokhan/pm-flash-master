from django.db import models
# from cmms.models.users import SysUser

class MachineCategory(models.Model):
    name=models.CharField("نام",max_length = 50)
    description=models.CharField("توضیحات",max_length = 50)

    isPartOf = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name="زیر مجموعه",null=True,blank=True)
    def __str__(self):
        return self.name

    class Meta:
       db_table = "machinecategory"
