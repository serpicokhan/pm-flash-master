#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb


##################### Asset Consuming Reference #########################
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
import os

class Project(models.Model):
    projectName=models.CharField('نام',max_length=100)
    projectDescription=models.TextField('شرح')
    ProjectStartDate=models.DateField('تاریخ شروع پروژه',default=datetime.now)
    ProjectEndDate=models.DateField('تاریخ پایان پروژه',default=datetime.now)
    ProjectActualStartDate=models.DateField('تاریخ شروع واقعی پروژه',default=datetime.now)
    ProjectActualEndDate=models.DateField('تاریخ واقعی اتمام پروژه',default=datetime.now,null=True,blank=True)
    def __str__(self):
        return "{}".format(self.projectName)

    def get_ProjectActualStartDate_jalali(self):
        return  jdatetime.date.fromgregorian(day=self.ProjectActualStartDate.day,month=self.ProjectActualStartDate.month,year=self.ProjectActualStartDate.year)
    def get_ProjectActualEndDate_jalali(self):
        return  jdatetime.date.fromgregorian(day=self.ProjectActualEndDate.day,month=self.ProjectActualEndDate.month,year=self.ProjectActualEndDate.year)
    class Meta:
        db_table = "project"
class ProjectUser(models.Model):
          ProjectUserId=models.ForeignKey(Project,on_delete=models.CASCADE,blank=True,null=True,verbose_name="دارایی")
          ProjectUserUserId=models.ForeignKey(SysUser,on_delete=models.CASCADE,blank=True,null=True,verbose_name="کاربر ")
          class Meta:
              db_table="projectuser"


class ProjectFile(models.Model):
    def get_ext(self):
        v=os.path.splitext(self.projectFile.name)
        return v[len(v)-1]
    def get_size(self):
        return " MB {0:.2f}".format(self.projectFile.size/1048576)

    projectFile=models.FileField(upload_to='documents/')
    projectFileProjectId=models.ForeignKey('project',on_delete=models.CASCADE,blank=True,null=True)
    projectFiledateAdded=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="projectfile"
