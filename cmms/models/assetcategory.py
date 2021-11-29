from django.db import models


class AssetCategory(models.Model):
    name=models.CharField("نام",max_length = 50)
    code=models.CharField("کد",max_length = 50)
    description=models.CharField("توضیحات",max_length = 50)
    priority=models.IntegerField("اولویت", null=True)
    isPartOf = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name="زیر مجموعه",null=True,blank=True)
    def __str__(self):
        return self.name

    class Meta:
       db_table = "assetcategory"
