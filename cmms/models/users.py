#python manage.py makemigrations
#After that you just have to run migrate command for syncing database .

#python manage.py migrate --run-syncdb
from django.db import models
from datetime import datetime
import os
from django.contrib.auth.models import User
import jdatetime
from django.utils.timezone import now
# from cmms.models.Asset import *
class testuser(models.Model):
    # password=models.CharField(max_length=20)
    massage=models.CharField("مشخصات کامل",max_length = 50)
    class Meta:
        db_table="testuser"


class SysUser(models.Model):
    def __str__(self):
        return "{}".format(self.fullName)
    def get_userStatus(self):
                 if(self.userStatus==True):
                     return "<i class='fa fa-play'></i>								"
                 else:
                     return "<i class='fa fa-stop'></i>"
    def getName(self):

        xxxx=UserGroups.objects.filter(userUserGroups=self.id)
        st=[]
        for i in xxxx:
            st.append(i.groupUserGroups)
        # print(''.join(str(e) for e in st))
        return '<br/>'.join(str(e) for e in st)


    Dashboard=1
    WorkOrderAssignedToMe=2
    MessageCenterInbox=3
    WorkOrders=4
    Location=(
        (Dashboard,'داشبورد'),
        (WorkOrderAssignedToMe,'درخواستهای انتسابی به من'),
        (MessageCenterInbox,'صندوق ورودی پیامها'),
        (WorkOrders,'درخواست'),
    )
    userId = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    password=models.CharField(max_length=20)
    token=models.CharField(max_length=200,null=True,blank=True)
    fullName=models.CharField("مشخصات کامل",max_length = 50)
    personalCode=models.CharField("کد پرسنلی",max_length = 50)
    title=models.CharField("عنوان",max_length = 50,null=True,blank=True)
    email=models.EmailField("ایمیل",max_length=70,blank=True, null= True, unique= True)
    tel1=models.CharField("تلفن",max_length = 50,null=True,blank=True)
    tel2=models.CharField("تلفن 2",max_length = 50,null=True,blank=True)
    addr1=models.CharField("آدرس",max_length = 50,null=True,blank=True)
    addr2=models.CharField("آدرس 2",max_length = 50,null=True,blank=True)
    city=models.CharField("شهر",max_length = 50,null=True,blank=True)
    state=models.CharField("استان",max_length = 50,null=True,blank=True)
    country=models.CharField("کشور",max_length = 50,null=True,blank=True)
    postalCode=models.CharField("کدپستی",max_length = 50,null=True,blank=True)
    hourlyRate=models.FloatField("نرخ دستمزد ساعتی",null=True, blank=True,default=0)
    defaultLoginLocation=models.FloatField("صفحه پیش فرض", choices=Location,null=True,blank=True)
    profileImage = models.ImageField(upload_to='images/',default=None,blank=True)

    userStatus=models.BooleanField("وضعیت",default=True)

    class Meta:
        db_table="sysusers"
        ordering = ['title']

class Attendance(models.Model):
    def get_datecreated_jalali(self):
        if(self.datecreated):
            return jdatetime.date.fromgregorian(day=self.datecreated.day,month=self.datecreated.month,year=self.datecreated.year)


    name=models.ForeignKey(SysUser, on_delete=models.CASCADE,null=True,blank=True,verbose_name='نام کاربر')
    datecreated = models.DateField("تاریخ حضور",default=datetime.now, blank=True,null=True)
    attendanceTime=models.FloatField("زمان حضور",default=8)
    Ezafekar=models.FloatField("اضافه کار",default=8)


    def __str__(self):
        return self.name

    class Meta:
       db_table = "attendance"
       unique_together = ('name', 'datecreated',)

class UserGroup(models.Model):
    def __str__(self):
        if(self.userUserLocation):
            return "{}:{}".format(self.userGroupName,self.userUserLocation)
        else:
            return "{}".format(self.userGroupName)

    userGroupCode=models.CharField("کد",max_length=50)
    userGroupName=models.CharField("نام",max_length=50)

    userGroupIsPartOF=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,verbose_name='زیرمجموعه')
    userUserLocation=models.ForeignKey('Asset',on_delete=models.CASCADE,blank=True,null=True,verbose_name='واحد')
    userGroupZarib=models.FloatField('ضریب حضور',null=True,blank=True)
    userGroupZaribTamir=models.FloatField('ضریب تعمیر',null=True,blank=True)
    userGroupZaribService=models.FloatField('ضریب سرویس',null=True,blank=True)
    userGroupZaribProject=models.FloatField('ضریب پروژه',null=True,blank=True)

    class Meta:
        db_table="usergroup"

class UserGroups(models.Model):


    userUserGroups=models.ForeignKey(SysUser,on_delete=models.CASCADE,blank=True,null=True)
    groupUserGroups=models.ForeignKey(UserGroup,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        db_table="usergroups"
class UserFile(models.Model):
    def get_ext(self):
        v=os.path.splitext(self.userFile.name)
        return v[len(v)-1]
    def get_size(self):
        return " MB {0:.2f}".format(self.userFile.size/1048576)

    userFile=models.FileField(upload_to='documents/')
    userFileUser=models.ForeignKey(SysUser,on_delete=models.CASCADE,blank=True,null=True)
    userFiledateAdded=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="userfile"
class UserCertification(models.Model):
    def getStartdate(self):
        return jdatetime.date.fromgregorian(date=self.userCertificationStart)
    def getEnddate(self):
        return jdatetime.date.fromgregorian(date=self.userCertificationEnd)
    certType1=1
    certType2=2
    certType3=3
    userCertList=((certType1,"نوع مدرک 1"),
                  (certType2,"نوع مدرک 2"),
                  (certType3,"نوع مدرک 3"))
    userCertificationName=models.CharField("عنوان",max_length=50)
    userCertificationUser=models.ForeignKey(SysUser,on_delete=models.CASCADE,blank=True,null=True)
    userCertificationType=models.IntegerField("نوع مدرک",choices=userCertList,null=True,blank=True)
    userCertificationDesc=models.TextField("توضیجات",blank=True,null=True)
    userCertificationStart=models.DateField("تاریخ اعتبار از",blank=True,null=True)
    userCertificationEnd=models.DateField("تاریخ اعتبار از",blank=True,null=True)

    class Meta:
        db_table="usercertification"
class UserGroupMaintenanceZarib(models.Model):
    groupUGMZ=models.ForeignKey(UserGroup,on_delete=models.CASCADE)

    maintenanceTypeUGMZ=models.ForeignKey('MaintenanceType',on_delete=models.CASCADE,verbose_name="نوع نگهداری")
    zaribUGMZ=models.FloatField('ضریب پروژه',null=True,blank=True)
    class Meta:
        db_table="usergroupmaintenancezarib"
        unique_together = ('groupUGMZ', 'maintenanceTypeUGMZ',)
