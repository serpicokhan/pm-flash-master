#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb
from django.db import models
from datetime import datetime
import jdatetime
from django.utils.timezone import now
from cmms.models.users import *
from cmms.models.workorder import *
from cmms.models.assetcategory  import *
#from cmms.models.workorder import WorkOrder
from cmms.utils import *
class Tasks(models.Model):
    def get_total_work_time(self):
        times= Tasks.objects.raw("select floor(COALESCE((timestampdiff(minute,cast(concat(taskStartDate, ' ', taskStartTime) as datetime),        cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0)) as id from tasks where id={0}".format(self.id) )[0].id
        times=times/60
        return '{0:02.0f}:{1:02.0f}'.format(*divmod(times * 60, 60))

    General=1
    Text=2
    meterReading=3


    TaskType1=(

        (General,'عمومی'),
        (Text ,'متنی'),
        (meterReading,'متریک'),

    )
    taskTypes=models.IntegerField("انتخاب نوع فعالیت", choices=TaskType1,null=True,blank=True)
    taskMetrics=models.ForeignKey("AssetMeterTemplate",verbose_name="واحد اندازه گیری",null=True,blank=True,on_delete=models.CASCADE)
    taskDescription=models.CharField("توضیحات",max_length = 100,null=True,blank=True)
    #result related to asset and measured according to Asset
    taskResult=models.FloatField("نتیجه",max_length = 50,null=True,blank=True)
    taskAssignedToUser = models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="اختصاص به کاربر",null=True,blank=True,related_name="assignedToUserTask")
    taskStartDate = models.DateField(" تاریخ شروع",null=True, blank=True)
    taskStartTime = models.TimeField("زمان شروع",default=datetime.now,null=True, blank=True)
    taskTimeEstimate=models.FloatField("زمان تقریبی( به ساعت)",null=True,blank=True)
    taskCompletedByUser = models.ForeignKey(SysUser,on_delete=models.CASCADE,verbose_name="کاربر تکمیل کننده",null=True,blank=True,related_name="CompleteUserTask")
    taskDateCompleted = models.DateField("تاریخ تکمیل",null=True, blank=True)
    taskTimeCompleted = models.TimeField("زمان پایان",default=datetime.now,null=True, blank=True)
    taskTimeSpent=models.FloatField("زمان صرف شده",null=True,blank=True)
    taskCompletionNote=models.CharField("یادداشت تکمیلی",max_length = 100,null=True,blank=True)
    workOrder = models.ForeignKey('WorkOrder',on_delete=models.CASCADE,null=True,blank=True,related_name="CompleteUserTask")
    #woId=models.FloatField(null=True,blank=True)
    class Meta:
      db_table = "tasks"
class WorkorderTask(models.Model):
    task=models.ForeignKey(Tasks,on_delete=models.SET_NULL,null=True,related_name="worordertaskrelated")
    workorder=models.ForeignKey('WorkOrder',on_delete=models.CASCADE,related_name="worordertaskwordrelated")
    class Meta:
        db_table="workordertask"
class TaskGroup(models.Model):
    taskGroupName=models.CharField("نام گروه",max_length = 50,null=True,blank=True)
    def getTaskNum(self):
        return TaskTemplate.objects.raw('select count(id) as id from tasktemplate  where taskTemplateTaskGroup_id={0} '.format(self.id))[0].id
    class Meta:
        db_table='taskgroup'
class TaskTemplate(models.Model):
    General=1
    Text=2
    meterReading=3


    TaskType1=(

        (General,'عمومی'),
        (Text ,'متنی'),
        (meterReading,'متریک'),

    )
    taskTemplateTypes=models.IntegerField("انتخاب نوع فعالیت", choices=TaskType1,null=True,blank=True)
    taskTemplateMetrics=models.ForeignKey("AssetMeterTemplate",verbose_name="واحد اندازه گیری",null=True,blank=True,on_delete=models.CASCADE)
    taskTemplateDescription=models.CharField("توضیحات",max_length = 100)
    taskTemplateTimeEstimate=models.FloatField("زمان تقریبی( به ساعت)",null=True,blank=True)
    taskTemplateTaskGroup = models.ForeignKey(TaskGroup,on_delete=models.CASCADE,null=True,blank=True,related_name="taskgroup",verbose_name='متعلق به')
    class Meta:
        db_table='tasktemplate'
class TaskGroupAssetCategory(models.Model):
    def get_TaskGroupAssetCategoryTik(self):
             if(self.includeSubCategory==True):
                 return "<i class='fa fa-check'>										</i>								"
             else:
                 return "<i class='fa fa-times'> </i>"
    TaskGroup = models.ForeignKey(TaskGroup,on_delete=models.CASCADE,null=True,blank=True)
    assetCategory = models.ForeignKey(AssetCategory,on_delete=models.CASCADE,null=True,blank=True,verbose_name='دسته دارایی')
    includeSubCategory=models.BooleanField("شامل زیر مجموعه دسته بندی ها",default=True,blank=True)
    class Meta:
        db_table='taskgroupassetcategory'
class TaskGroupFile(models.Model):
    def get_ext(self):
        v=os.path.splitext(self.taskGroupFile.name)
        return v[len(v)-1]
    def get_size(self):
        return " MB {0:.2f}".format(self.taskGroupFile.size/1048576)

    taskGroupFile=models.FileField(upload_to='documents/')
    taskGroupFileTaskGroup=models.ForeignKey(TaskGroup,on_delete=models.CASCADE,blank=True,null=True)
    taskGroupFiledateAdded=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="taskgroupfile"
