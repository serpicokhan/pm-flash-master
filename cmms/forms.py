
from django import forms
from cmms.models import *
from django.conf import settings
import logging
from django.forms import ModelForm, inlineformset_factory

from cmms.business.DateJob import *
import datetime
from datetime import datetime,date
from datetime import timedelta
from django.shortcuts import get_object_or_404
import hazm
from hazm import stopwords_list
from hazm import word_tokenize, sent_tokenize
from cmms.component.field import *
import os
import sys
from django.core.exceptions import ValidationError

class CopyAssetForm(forms.Form):
    assetname2= forms.ModelChoiceField(label="نام دستگاه",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':''}))

class WorkOrderForm(forms.ModelForm):

    workInstructions = forms.CharField( label="دستورالعمل",widget=forms.Textarea(attrs={'rows': 15, 'cols': 100}),required=False )
    completionNotes = forms.CharField( label="یادداشت تکمیلی",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )
    adminNote = forms.CharField( label="یادداشت مدیر",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )
    woasset_ = forms.CharField(label='دسته بندی',required=False,widget=forms.TextInput(attrs={'autocomplete':'off'}))

    # RequestedUser = forms.IntegerField( required=False )
    def clean_woTags(self):
        str1= self.cleaned_data['summaryofIssue']
        # print("********************")
        #print(str1)
        stops = set(stopwords_list())
        words = [word for word in word_tokenize(str1) if word not in stops]
        value= ', '.join(str(e) for e in words)
        # print("********************")
        #print(value)
        return value

    # def clean_requiredCompletionDate(self):
    #     value=DateJob.getTaskDate2( self.cleaned_data['requiredCompletionDate'])
    #     # print(value,'****************************')
    #     return value
    # def clean_datecreated(self):
    #      print("datecreated")
    #      print(self.cleaned_data['datecreated'],"datecreated")
    #      value=DateJob.getTaskDate( self.cleaned_data['datecreated'])

         # return value
    def clean_dateCompleted(self):
        if(self.cleaned_data['dateCompleted']):
             print(self.cleaned_data['dateCompleted'],'datecompleted')
             value=DateJob.getDate2( self.cleaned_data['dateCompleted'])
             return value
        else:
            return None
    def clean_summaryofIssue(self):
         value= self.cleaned_data['summaryofIssue']
         return value

    #CustomerId = forms.ModelChoiceField(queryset=Customer.objects.all())
    class Meta:
        model = WorkOrder
        fields = '__all__'

class MyModelChoiceField(ModelChoiceField):

   def to_python(self, value):
        # try:
        #     value = super(MyModelChoiceField, self).to_python(value)
        # except self.queryset.model.DoesNotExist:
        #     key = self.to_field_name or 'pk'
        #     value = Stock.objects.filter(**{key: value})
        #     if not value.exists():
        #        raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
        #     else:
        #        value= value.first()

        return value
class WorkOrderForm2(forms.ModelForm):

    # def to_python(self, value):
    #         if value in self.empty_values:
    #             return None
    #         try:
    #             key = self.woPart
    #             value = self.queryset.get(**{key: value})
    #         except (ValueError, TypeError, self.queryset.model.DoesNotExist):
    #             raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
    #         return value
    # def __init__(self,*args,**kwargs):
    #
    #     super (WorkOrderForm2,self ).__init__(*args,**kwargs) # populates the post
    #     try:
    #             self.fields['woPart'].queryset = Stock.objects.none() #AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=WorkOrder.objects.get(id=workorder).woAsset)
    #     except Exception as ex:
    #         print(ex)
    # workInstructions = forms.CharField( label="دستورالعمل",widget=forms.Textarea(attrs={'rows': 15, 'cols': 100}),required=False )
    # completionNotes = forms.CharField( label="یادداشت تکمیلی",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )
    pertTime = forms.FloatField(required=False)
    myAsset = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    # woPart =  forms.ModelChoiceField(label="نام کاربر",queryset=Stock.objects.none(),required=False)
    woPart =  MyModelChoiceField(label="نام کاربر",queryset=Stock.objects.none(),required=False,empty_label=None)



    # RequestedUser = forms.IntegerField( required=False )
    unitgroups = forms.ModelMultipleChoiceField(queryset=UserGroup.objects.all(),required=False)
    # woPart = forms.ModelMultipleChoiceField(queryset=Stock.objects.all(),required=False)
    # assignedToUser=forms.ModelMultipleChoiceField(queryset=SysUser.objects.filter(userStatus=True),required=False)
    assignedToUser = forms.ModelChoiceField(label="گروه کاری",queryset=SysUser.objects.filter(userStatus=True),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    woPartQty=forms.FloatField(required=False,initial=0)
    timecreated=forms.TimeField(required=False)

    def clean(self):

            self.is_valid()
            cleaned_data=super(WorkOrderForm2, self).clean()

            #if(self.is_valid()):
            try:
                datecreated=cleaned_data.get('datecreated','')

                woStatus=cleaned_data.get('woStatus','')
                RequestedUser=cleaned_data.get('RequestedUser','')
                maintenanceType=cleaned_data.get('maintenanceType','')
                woAsset=cleaned_data.get('woAsset','')
                summaryofIssue=cleaned_data.get('summaryofIssue','')
                completionNotes=(cleaned_data.get('completionNotes',''))
                woCauseCode=cleaned_data.get('woCauseCode','')
                Project=cleaned_data.get('Project','')
                dateCompleted=cleaned_data.get('dateCompleted','')
                timeCompleted=cleaned_data.get('timeCompleted','')
                # print("##########")
                # print(cleaned_data.get('assignedToUser',''))
                # print("###############")
                assignedToUser=cleaned_data.get('assignedToUser','')
                woStopCode=cleaned_data.get('woStopCode','')

                try:
                    woPart=self.woPart.to_python(cleaned_data.get('woPart',''))#cleaned_data.get('woPart','')
                except:
                    pass
                # print("wopart",woPart)
                woPartQty=cleaned_data.get('woPartQty','0')
                pertTime=cleaned_data.get('pertTime','')
                timecreated=cleaned_data.get('timecreated','')
                isEM=cleaned_data.get('isEM',False)

                #wo tags
                stops = set(stopwords_list())
                words = [word for word in word_tokenize(summaryofIssue) if word not in stops]
                woTags= ', '.join(str(e) for e in words)
                isPm=False
            except Exception as e:
                    # data2["error"]=e
                    # print(e,"!@#!@")
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(e)


                #woId=cleaned_data.get('woId','')
                #WorkOrder=cleaned_data.get('workOrder','')
                # result="312312"
                # print("######################",assignedToUser)
            return cleaned_data




    #CustomerId = forms.ModelChoiceField(queryset=Customer.objects.all())
    class Meta:
        model = WorkOrder
        fields = ['unitgroups','datecreated','RequestedUser', 'maintenanceType', 'woAsset','Project','dateCompleted','timeCompleted','summaryofIssue','assignedToUser','woStopCode','completionNotes','woCauseCode','isEM','woStatus']
class SearchFormSetForm(forms.Form):
    mainType=MaintenanceType.objects.all()

    # renderformat = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all())
    to_date = forms.CharField(label='date 2')
    from_date = forms.CharField(label='date 1', initial=DateJob.getTodayDate())
    # MaintenanceType = forms.CharField(label='Your name', max_length=100)


class MiniWorkorderForm(forms.ModelForm):
    # def clean(self):
    #             self.is_valid()
    #             cleaned_data=super(MiniWorkorderForm, self).clean()

    def clean_woStatus(self):
         value=1
         return value
    def clean_maintenanceType(self):
         print("!!!!!!!@#@!#!@#@!#@#@")
         value=MaintenanceType.objects.get(name="تعمیر")
         return value
    def clean_woTags(self):
        str1= self.cleaned_data['summaryofIssue']
        # print("********************")
        #print(str1)
        stops = set(stopwords_list())
        words = [word for word in word_tokenize(str1) if word not in stops]
        value= ', '.join(str(e) for e in words)
        # print("********************")
        #print(value)
        return value


    class Meta:
        model = WorkOrder
        fields = ('summaryofIssue','woAsset','maintenanceType','woTags','woStatus')


class TaskForm(forms.ModelForm):
    def __init__(self,workorder=None,*args,**kwargs):

        super (TaskForm,self ).__init__(*args,**kwargs) # populates the post
        try:
            if(workorder):
                print("!!!!!!!!!!!!!!!!!")
                bg_groups=BMGAsset.objects.filter(BMGAsset=WorkOrder.objects.get(id=workorder).woAsset).values_list('BMGGroup',flat=True)
                tmp_=BMGTemplate.objects.filter(BMGGroup__in=bg_groups).values_list('BMGTemplate',flat=True)
                books=AssetMeterTemplate.objects.filter(id__in=tmp_).order_by('-id')
                self.fields['taskMetrics'].queryset = books #AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=WorkOrder.objects.get(id=workorder).woAsset)
            else:
                self.fields['taskMetrics'].queryset = AssetMeterTemplate.objects.none()
        except Exception as ex:
            print(ex)



    taskDescription = forms.CharField( label="توضیحات",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )
    taskCompletionNote = forms.CharField( label="یادداشت تکمیلی",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )

    def clean(self):
                self.is_valid()
                cleaned_data=super(TaskForm, self).clean()

            #if(self.is_valid()):
                try:
                    taskDescription=cleaned_data.get('taskDescription','')
                    taskCompletionNote=cleaned_data.get('taskCompletionNote','')

                    taskTypes=cleaned_data.get('taskTypes','')
                    taskMetrics=cleaned_data.get('taskMetrics','')
                    taskAssignedToUser=cleaned_data.get('taskAssignedToUser','')
                    taskStartDate=(cleaned_data.get('taskStartDate',''))
                    taskTimeEstimate=cleaned_data.get('taskTimeEstimate','')
                    taskDateCompleted=cleaned_data.get('taskDateCompleted','')
                    taskCompletedByUser=cleaned_data.get('taskCompletedByUser','')
                    taskTimeSpent=cleaned_data.get('taskTimeSpent','')
                    taskResult=cleaned_data.get('taskResult','')
                    task_inspection=cleaned_data.get('task_inspection','')
                    workOrder=cleaned_data.get('workOrder','')
                    #woId=cleaned_data.get('woId','')
                    #WorkOrder=cleaned_data.get('workOrder','')
                    result="312312"
                    # print("everything is goo")
                except :
                    print("error is here!!")
                    return cleaned_data

    # def clean_taskStartDate(self):
    #     # value=DateJob.getTaskDate( self.cleaned_data['taskStartDate'])
    #     dt1=self.cleaned_data['taskStartDate']
    #     value=dt1
    #     if(dt1==""):
    #         value= ""
    #     y=None
    #     #
    #     y=str(dt1).split("-")
    #     # #y=str(dt).split("-")
    #     if(len(y)==3):
    #         year=int(y[0])
    #         month=int(y[1])
    #         day=int(y[2])
    #         #     print(jdatetime.date(year,month,day).togregorian(),"$$$$$$$$$$$$$$$$$$$")
    #         # value=jdatetime.date(year,month,day).togregorian()
    #         tt=JalaliDate(year, month, day).to_gregorian()
    #         print(tt,"kkkkk")
    #     return value
    # def clean_taskDateCompleted(self):
    #     if(self.cleaned_data['taskDateCompleted']):
    #          # value=DateJob.getTaskDate( self.cleaned_data['taskDateCompleted'])
    #          value=self.cleaned_data['taskDateCompleted']
    #          return value
    #     else:
    #         return None

    class Meta:
         model = Tasks
         fields = '__all__'



class TaskForm2(forms.ModelForm):
    def __init__(self,workorder=None,*args,**kwargs):
        super (TaskForm2,self ).__init__(*args,**kwargs) # populates the post
        print("here!!!!!!!!!2222")
        try:
            print(workorder)
            if(workorder):
                print("!!!!!!!!!!!!!!!!!")
                bg_groups=BMGAsset.objects.filter(BMGAsset=WorkOrder.objects.get(id=workorder).woAsset).values_list('BMGGroup',flat=True)
                tmp_=BMGTemplate.objects.filter(BMGGroup__in=bg_groups).values_list('BMGTemplate',flat=True)
                books=AssetMeterTemplate.objects.filter(id__in=tmp_).order_by('-id')
                self.fields['taskMetrics'].queryset = books #AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=WorkOrder.objects.get(id=workorder).woAsset)
            else:
                self.fields['taskMetrics'].queryset = AssetMeterTemplate.objects.none()
        except Exception as ex:
            print(ex)
    taskDescription = forms.CharField( label="توضیحات",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )
    def clean(self):
                self.is_valid()
                cleaned_data=super(TaskForm2, self).clean()
                taskDescription=cleaned_data.get('taskDescription','')
                taskTypes=cleaned_data.get('taskTypes','')
                taskMetrics=cleaned_data.get('taskMetrics','')
                taskAssignedToUser=cleaned_data.get('taskAssignedToUser','')
                taskTimeEstimate=cleaned_data.get('taskTimeEstimate','')
                workOrder=cleaned_data.get('workOrder','')
                return cleaned_data
    class Meta:
         model = Tasks
         fields = ['taskTypes', 'taskMetrics', 'taskDescription', 'taskAssignedToUser','taskTimeEstimate','workOrder']

class TaskTemplateForm(forms.ModelForm):
    taskTemplateDescription = forms.CharField( label="توضیحات",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=True )
    # taskCompletionNote = forms.CharField( label="یادداشت تکمیلی",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )

    def clean(self):
                self.is_valid()
                cleaned_data=super(TaskTemplateForm, self).clean()
            #if(self.is_valid()):
                tasktemplateDescription=cleaned_data.get('tasktemplateDescription','')
                tasktemplateCompletionNote=cleaned_data.get('tasktemplateCompletionNote','')
                tasktemplateTypes=cleaned_data.get('tasktemplateTypes','')
                tasktemplateMetrics=cleaned_data.get('tasktemplateMetrics','')


                taskTemplateTaskGroup=cleaned_data.get('taskTemplateTaskGroup','')

                return cleaned_data



    class Meta:
         model = TaskTemplate
         fields = '__all__'
class TaskGroupForm(forms.ModelForm):
    taskGroupName = forms.CharField( label="دستورالعمل",required=True )

    class Meta:
        model = TaskGroup
        fields = '__all__'
class TaskGroupFileForm(forms.ModelForm):
    class Meta:
         model = TaskGroupFile
         fields = ('taskGroupFile',)
class TaskGroupAssetCategoryForm(forms.ModelForm):

    def clean(self):


                self.is_valid()
                cleaned_data=super(TaskGroupAssetCategoryForm, self).clean()
                TaskGroup=cleaned_data.get('TaskGroup','')
                assetCategory=cleaned_data.get('assetCategory','')
                includeSubCategory=cleaned_data.get('includeSubCategory','')


                return cleaned_data


    class Meta:
         model = TaskGroupAssetCategory
         fields = '__all__'
###########################################################
class WoAssetForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(WoAssetForm, self).clean()
                assetTypes=cleaned_data.get('assetTypes','')
                assetName=cleaned_data.get('assetName','')
                assetCode=cleaned_data.get('assetCode','')
                assetIsPartOf=cleaned_data.get('assetIsPartOf','')
                assetIsLocatedAt=cleaned_data.get('assetIsLocatedAt','')


                return cleaned_data

    class Meta:
         model = Asset
         fields = ('assetTypes','assetName','assetCode','assetIsPartOf','assetIsLocatedAt')

###################################################################################
class WoPartForm(forms.ModelForm):
    # part=forms.CharField(widget=forms.HiddenInput(),required=False)
    mypart = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    # myPart = forms.ModelChoiceField(label="نام قطعه",queryset=Part.objects.all()[:10])

    def clean(self):
                self.is_valid()
                cleaned_data=super(WoPartForm, self).clean()
                woPartWorkorder=cleaned_data.get('woPartWorkorder','')
                # woPartPart=cleaned_data.get('woPartPart','')
                woPartPlannedQnty=cleaned_data.get('woPartPlannedQnty','')
                woPartActulaQnty=cleaned_data.get('woPartActulaQnty','')
                woPartStock=cleaned_data.get('woPartStock','')
                # if woPartStock and WorkorderPart.objects.get(woPartWorkorder=woPartWorkorder,woPartStock=woPartStock):
                #         raise forms.ValidationError("not unique")
                return cleaned_data


    class Meta:
         model = WorkorderPart
         fields = '__all__'

#########################################################################################

class WoMeterForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(WoMeterForm, self).clean()
                woMeterReadingworkorder=cleaned_data.get('woMeterReadingworkorder','')
                woMeterReadingLocation=cleaned_data.get('woMeterReadingLocation','')
                woMeterReadingMeterReading=cleaned_data.get('woMeterReadingMeterReading','')
                woMeterReadingMeterReadingUnit=cleaned_data.get('woMeterReadingMeterReadingUnit','')
                timestamp=datetime.datetime.now()
                print("ewqewqewq")
                print(woMeterReadingLocation)
                return cleaned_data


    class Meta:
         model = WorkorderMeterReading
         fields = '__all__'
#########################################################################################

class WoPertForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(WoPertForm, self).clean()
                woPertWorkorder=cleaned_data.get('woPertWorkorder','')
                woPertPert=cleaned_data.get('woPertPert','')
                wpPertTime=cleaned_data.get('wpPertTime','')

                return cleaned_data


    class Meta:
         model = WorkorderPert
         fields = '__all__'



#########################################################################################

class WoMiscForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(WoMiscForm, self).clean()
                miscCoastWorkorder=cleaned_data.get('miscCoastWorkorder','')
                miscCoastType=cleaned_data.get('miscCoastType','')
                miscCoastdescription=cleaned_data.get('miscCoastdescription','')
                estimatedQnty=cleaned_data.get('estimatedQnty','')
                estimatedUnitCoast=cleaned_data.get('estimatedUnitCoast','')
                estimatedTotalCoast=cleaned_data.get('estimatedTotalCoast','')
                qnty=cleaned_data.get('qnty','')
                actualUnitCoast=cleaned_data.get('actualUnitCoast','')
                actualTotlaCoast=cleaned_data.get('actualTotlaCoast','')
                miscCoastIndividual=cleaned_data.get('miscCoastIndividual','')

                return cleaned_data


    class Meta:
         model = MiscCost
         fields = '__all__'


#########################################################################################

class WoNotifyForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(WoNotifyForm, self).clean()
                woNotifWorkorder=cleaned_data.get('woNotifWorkorder','')
                woNotifUser=cleaned_data.get('woNotifUser','')
                woNotifOnAssignment=cleaned_data.get('woNotifOnAssignment','')
                woNotifOnStatusChange=cleaned_data.get('woNotifOnStatusChange','')
                woNotifOnCompletion=cleaned_data.get('woNotifOnCompletion','')
                woNotifOnTaskCompleted=cleaned_data.get('woNotifOnTaskCompleted','')
                woNotifOnOnlineOffline=cleaned_data.get('woNotifOnOnlineOffline','')

                return cleaned_data


    class Meta:
         model = WorkorderUserNotification
         fields = '__all__'
#########################################################################################



class WoFileForm(forms.ModelForm):

    def clean_woFileworkorder(self):
         woFileworkorder=1
         return woFileworkorder
    class Meta:
         model = WorkorderFile
         fields = ('woFile',)

#########################################################################################
class AssetFileForm(forms.ModelForm):
    class Meta:
         model = AssetFile
         fields = ('assetFile',)


#########################################################################################
CHOICES=[(0,'درخواست بر اساس زمانبندی'),
      (1,'درخواست بر اساس اندازه گیری'),
      (2,'درخواست بر اساس وقوع رویداد')]
COMPARISON=[(0,'بزرگتر از'),
             (1,'کوچکتر از'),
             ]
TimeCHOICES=[
       (1,'ساعتی'),
       (2,'روزانه'),
       (3,'هفتگی'),
       (4,'ماهانه'),
       (5,'سالانه'),]
timeSchedulingChoices=[(0,'12:00 AM'),(1,'1:00 AM'),(2,'2:00 AM'),(3,'3:00 AM'),(4,'4:00 AM'),(5,'5:00 AM'),(6,'6:00 AM'),(7,'7:00 AM'),(8,'8:00 AM'),(9,'9:00 AM'),(10,'10:00 AM'),(11,'11:00 AM'),(12,'12:00 PM'),
                      (13,'1:00 PM'),(14,'2:00 PM'),(15,'3:00 PM'),(16,'4:00 PM'),(17,'5:00 PM'),(18,'6:00 PM'),(19,'7:00 PM'),(20,'8:00 PM'),(21,'9:00 PM'),(22,'10:00 PM'),(23,'11:00 PM')]
FixedOrFloating=[(True,'ثابت'),
                (False,'شناور')]
HasEnded=[(0,'نامحدود'),
(1,'اتمام در تاریخ'),]

class ScheduleForm(forms.ModelForm):
    #schnextTime=forms.DateTimeField(required=False)
    #workOrder=forms.IntegerField(required=False)
    schTriggerTime=forms.ChoiceField(choices=timeSchedulingChoices,required=False,label="زمان راه اندازی")
    schChoices=forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),required=False)
    schHowOften=forms.ChoiceField(choices=TimeCHOICES, widget=forms.RadioSelect(),required=False)
    schHourIsFixed=forms.ChoiceField(choices=FixedOrFloating, widget=forms.RadioSelect(),required=False)
    schDayIsFixed=forms.ChoiceField(choices=FixedOrFloating, widget=forms.RadioSelect(),required=False)
    schMonthIsFixed=forms.ChoiceField(choices=FixedOrFloating, widget=forms.RadioSelect(),required=False)
    schYearIsFixed=forms.ChoiceField(choices=FixedOrFloating, widget=forms.RadioSelect(),required=False)
    #schMeterReadingIsFixed=forms.ChoiceField(choices=FixedOrFloating, widget=forms.RadioSelect(),required=False)
    #shHasEndDate=forms.ChoiceField(choices=HasEnded, widget=forms.RadioSelect(),required=False)
    #shReadingHasEndDate=forms.ChoiceField(choices=HasEnded, widget=forms.RadioSelect(),required=False)
    def clean(self):
                self.is_valid()
                cleaned_data=super(ScheduleForm, self).clean()
                schChoices=cleaned_data.get('schChoices','')
                schHowOften=cleaned_data.get('schHowOften','')
                schHourRep=cleaned_data.get('schHourRep','')
                schHourIsFixed=cleaned_data.get('schHourIsFixed','')
                workOrder=cleaned_data.get('workOrder','')
                shHasEndDate=cleaned_data.get('shHasEndDate','')
                schWeeklyRep=cleaned_data.get('schWeeklyRep','')
                isSaturday=cleaned_data.get('isSaturday','')
                isSunday=cleaned_data.get('isSunday','')
                isMonday=cleaned_data.get('isMonday','')
                isTuesday=cleaned_data.get('isTuesday','')
                isWednenday=cleaned_data.get('isWednenday','')
                isThursday=cleaned_data.get('isThursday','')
                isFriday=cleaned_data.get('isFriday','')

                schDayofMonthlyRep=cleaned_data.get('schDayofMonthlyRep','')
                schMonthlyRep=cleaned_data.get('schMonthlyRep','')
                schMonthIsFixed=cleaned_data.get('schMonthIsFixed','')

                schYearlyRep=cleaned_data.get('schYearlyRep','')

                schMonthOfYearRep=cleaned_data.get('schMonthOfYearRep','')
                schDayOfMonthOfYearRep=cleaned_data.get('schDayOfMonthOfYearRep','')
                schYearIsFixed=cleaned_data.get('schYearIsFixed','')
                #shMeterReadingEvreyQnty
                shMeterReadingEvreyQnty=cleaned_data.get('shMeterReadingEvreyQnty','')
                shMeterReadingMetrics=cleaned_data.get('shMeterReadingMetrics','')
                shMeterReadingStartAt=cleaned_data.get('shMeterReadingStartAt','')
                shMeterReadingEndBy=cleaned_data.get('shMeterReadingEndBy','')
                schMeterReadingIsFixed=cleaned_data.get('schMeterReadingIsFixed','')
                shMeterReadingWhenMetric=cleaned_data.get('shMeterReadingWhenMetric','')
                shMetricComparison=cleaned_data.get('shMetricComparison','')
                shMeterReadingWhenQnty=cleaned_data.get('shMeterReadingWhenQnty','')
                schHasEndReading=cleaned_data.get('schHasEndReading','')
                shStartDate=cleaned_data.get('shStartDate','')
                shEndDate=cleaned_data.get('shEndDate','')
                schEvent=cleaned_data.get('schEvent','')
                schAsset=cleaned_data.get('schAsset','')
                schnextTime=datetime.now()
                shMeterReadingHasTiming=cleaned_data.get('shMeterReadingHasTiming','')
                #shStartTime2=cleaned_data.get('shStartTime2')
                shReadingHasEndDate=0
                schNextWo=cleaned_data.get('schNextWo','')
                print(schNextWo,'FFFFFFFFFFFFFFFFFFFFFFFF')
                schTriggerTime=cleaned_data.get('schTriggerTime',0)
                schCreateOnStartDate=cleaned_data.get('schTriggerTime',False)
                #schChoices=1
                #schHowOften=1
                #schHourRep=1
                #schHourIsFixed=True
                return cleaned_data
    # def clean_shStartDate(self):
    #     #nexttime=shStartDate+timedelta(days=1)
    #     value=DateJob.getDateTime3(self.cleaned_data['shStartDate'])
    #
    #
    #     return value

    class Meta:
         model = Schedule
         fields = '__all__'
class AssetForm(forms.ModelForm):
    assetDescription = forms.CharField( label="توضیحات",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )
    assetIsLocatedAt = forms.ModelChoiceField(label="مکان",queryset=Asset.objects.filter(assetTypes=1,assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}),required=False)
    # def clean_assetCategory(self):
    #     last_name = self.cleaned_data['assetCategory']
    #     print(last_name,"$$$$$$$$$$$$$$$$")
    #     return int(last_name)
    asseccategorytxt = forms.CharField(label='دسته بندی',required=False,widget=forms.TextInput(attrs={'autocomplete':'off'}))
    assetispart = forms.CharField(label='دسته بندی',required=False,widget=forms.TextInput(attrs={'autocomplete':'off'}))

    class Meta:
        model = Asset
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        super(AssetForm, self).__init__(*args, **kwargs)
        # self.fields['assetCategory'].queryset = AssetCategory.objects.filter(id__lte=3)
# class AssetSubForm(forms.Form):
#     assetDescription = forms.CharField( label="توضیحات",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )
#     # def clean_assetCategory(self):
#     #     last_name = self.cleaned_data['assetCategory']
#     #     print(last_name,"$$$$$$$$$$$$$$$$")
#     #     return int(last_name)
#     # asseccategorytxt = forms.CharField(label='دسته بندی',required=False,widget=forms.TextInput(attrs={'autocomplete':'off'}))
#             makan= forms.ModelChoiceField(label="نام مکان",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
#             widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))



class AssetPartForm(forms.ModelForm):
    mypart=forms.CharField(required=False)

    def clean(self):
                 self.is_valid()
                 cleaned_data=super(AssetPartForm, self).clean()
                 assetPartAssetid=cleaned_data.get('assetPartAssetid','')
                 assetPartPid=cleaned_data.get('assetPartPid','')
                 assetPartQnty=cleaned_data.get('assetPartQnty','')
                 assetPartDescription=cleaned_data.get('assetPartDescription','')



                 return cleaned_data
    class Meta:
        model = AssetPart
        fields = '__all__'
class BOMGroupPartForm(forms.ModelForm):
    mypart=forms.CharField(required=False)
    def clean(self):
                 self.is_valid()
                 cleaned_data=super(BOMGroupPartForm, self).clean()
                 BOMGroupPartPart=cleaned_data.get('BOMGroupPartPart','')
                 BOMGroupPartBOMGroup=cleaned_data.get('BOMGroupPartBOMGroup','')
                 BOMGroupPartQnty=cleaned_data.get('BOMGroupPartQnty','')




                 return cleaned_data
    class Meta:
        model = BOMGroupPart
        fields = '__all__'
class BMGTemplateForm(forms.ModelForm):
    mypart=forms.CharField(required=False)
    def clean(self):
                 self.is_valid()
                 cleaned_data=super(BMGTemplateForm, self).clean()
                 BMGTemplate=cleaned_data.get('BMGTemplate','')
                 BMGroup=cleaned_data.get('BMGroup','')




                 return cleaned_data
    class Meta:
        model = BMGTemplate
        fields = '__all__'
class BOMGroupAssetForm(forms.ModelForm):
    my_asset=forms.CharField(required=False)
    def clean(self):
                 self.is_valid()
                 cleaned_data=super(BOMGroupAssetForm, self).clean()
                 BOMGroupPartAsset=cleaned_data.get('BOMGroupPartAsset','')
                 BOMGroupPartBOMGroup=cleaned_data.get('BOMGroupPartBOMGroup','')
                 return cleaned_data
    class Meta:
        model = BOMGroupAsset
        fields = '__all__'
class BMGAssetForm(forms.ModelForm):
    my_asset=forms.CharField(required=False)
    def clean(self):
                 self.is_valid()
                 cleaned_data=super(BMGAssetForm, self).clean()
                 BMGAsset=cleaned_data.get('BMGAsset','')
                 BMGGroup=cleaned_data.get('BMGGroup','')
                 return cleaned_data
    class Meta:
        model = BMGAsset
        fields = '__all__'

#########################################################################################

class AssetMeterForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):


             self.asset_id = kwargs.pop('asset_id')
             print("######",self.asset_id)
             super(AssetMeterForm,self).__init__(*args,**kwargs)
             bg_groups=BMGAsset.objects.filter(BMGAsset__id=self.asset_id).values_list('BMGGroup',flat=True)
             tmp_=BMGTemplate.objects.filter(BMGGroup__in=bg_groups).values_list('BMGTemplate',flat=True)
             books=AssetMeterTemplate.objects.filter(id__in=tmp_).order_by('-id')
             self.fields['assetWorkorderMeterReading'] = forms.ModelChoiceField(label="دستور کاری",queryset=WorkOrder.objects.filter(woAsset=self.asset_id,isScheduling=False),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}),required=False)
             self.fields['assetMeterMeterReadingUnit'] = forms.ModelChoiceField(label="کمیت",queryset=books,widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}),required=False)
     # assetWOAssoc = forms.CharField()
    #populate and filter select according to its workorder
    # def __init__(self,asset=None,*args,**kwargs):
    #     super (AssetMeterForm,self ).__init__(*args,**kwargs) # populates the post
    #
    #     if(asset):
    #         super (AssetMeterForm,self ).__init__(*args,**kwargs) # populates the post
    #         self.fields['assetWorkorderMeterReading'].queryset = WorkOrder.objects.filter(woAsset=asset)
    #         #print(WorkOrder.objects.filter(woAsset=asset))
        #self.fields['client'].queryset = Client.objects.filter(company=company)
    # def __init__(self,asset=None,*args,**kwargs):
    #     super (AssetMeterForm,self ).__init__(*args,**kwargs) # populates the post
    #     if asset is not None:
    #         self.fields['assetWorkorderMeterReading'].queryset = WorkOrder.objects.filter(woAsset=asset)
        #self.fields['client'].queryset = Client.objects.filter(company=company)



    def clean(self):
                self.is_valid()
                cleaned_data=super(AssetMeterForm, self).clean()
                try:
                    assetMeterLocation=cleaned_data.get('assetMeterLocation','')
                    assetMeterMeterReading=cleaned_data.get('assetMeterMeterReading','')
                    assetMeterMeterReadingUnit=cleaned_data.get('assetMeterMeterReadingUnit','')
                    assetWorkorderMeterReading=cleaned_data.get('assetWorkorderMeterReading',None)
                # print("forms.py,line 354",cleaned_data.get('assetWorkorderMeterReading',''))
                except:
                    pass
                return cleaned_data


    class Meta:
         model = AssetMeterReading
         fields = '__all__'

##############################################################################
class AssetEventForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(AssetEventForm, self).clean()
                AssetEventEventId=cleaned_data.get('AssetEventEventId','')
                AssetEventAssetId=cleaned_data.get('AssetEventAssetId','')
                AssetEventAdditionalDescription=cleaned_data.get('AssetEventAdditionalDescription','')


                return cleaned_data


    class Meta:
         model = AssetEvent
         fields = '__all__'


##############################################################################
class AssetMeterTemplateForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(AssetMeterTemplateForm, self).clean()
                # assetMeterTemplateAsset=cleaned_data.get('assetMeterTemplateAsset','')
                assetMeterTemplateMeter=cleaned_data.get('assetMeterTemplateMeter','')
                assetMeterTemplateDesc=cleaned_data.get('assetMeterTemplateDesc','')


                return cleaned_data


    class Meta:
         model = AssetMeterTemplate
         fields = '__all__'


##############################################################################
class AssetUserForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(AssetUserForm, self).clean()
                AssetUserAssetId=cleaned_data.get('AssetUserAssetId','')
                AssetUserUserId=cleaned_data.get('AssetUserUserId','')



                return cleaned_data


    class Meta:
         model = AssetUser
         fields = '__all__'
########################################################################
class AssetWarantyForm(forms.ModelForm):

    def clean(self):


                self.is_valid()
                cleaned_data=super(AssetWarantyForm, self).clean()
                warantyType=cleaned_data.get('warantyType','')
                warantyProvider=cleaned_data.get('warantyProvider','')
                warantyUsageTermType=cleaned_data.get('warantyUsageTermType','')
                warantyDataAdded=cleaned_data.get('warantyDataAdded','')
                warantyUsageTermType=cleaned_data.get('warantyUsageTermType','')
                warantyCertificationNumber=cleaned_data.get('warantyCertificationNumber','')
                warantyUsageTermType=cleaned_data.get('warantyUsageTermType','')
                warantyLocation=cleaned_data.get('warantyLocation','')
                warantyMeterReadingValueLimit=cleaned_data.get('warantyMeterReadingValueLimit','')
                warantyMeterReadingUnit=cleaned_data.get('warantyMeterReadingUnit','')
                warantyQnty=0
                return cleaned_data


    class Meta:
         model = Waranty
         fields = '__all__'


########################################################################
class AssetBusinessForm(forms.ModelForm):

    def clean(self):


                self.is_valid()
                cleaned_data=super(AssetBusinessForm, self).clean()
                BusinessAssetAsset=cleaned_data.get('BusinessAssetAsset','')
                businessAssetBusiness=cleaned_data.get('businessAssetBusiness','')
                businessAssetBusinessType=cleaned_data.get('businessAssetBusinessType','')
                businessAssetSupplierPartNumber=cleaned_data.get('businessAssetSupplierPartNumber','')
                businessAssetCatalog=cleaned_data.get('businessAssetCatalog','')
                businessAssetisDefault=cleaned_data.get('businessAssetisDefault','')

                return cleaned_data


    class Meta:
         model = BusinessAsset
         fields = '__all__'

########################################################################
class AssetPurchaseForm(forms.ModelForm):

    def clean(self):


                self.is_valid()
                cleaned_data=super(AssetPurchaseForm, self).clean()
                purchaseAssetId=cleaned_data.get('purchaseAssetId','')
                purchaseDateOrdered=cleaned_data.get('purchaseDateOrdered','')
                purchasePriceTotla=cleaned_data.get('purchasePriceTotla','')
                purchaseCurrency=cleaned_data.get('purchaseCurrency','')
                purchaseDateRecieved=cleaned_data.get('purchaseDateRecieved','')
                purchaseDateofExpire=cleaned_data.get('purchaseDateofExpire','')
                purchaseDateRecieved=cleaned_data.get('purchaseDateRecieved','')
                purchasedFrom=cleaned_data.get('purchasedFrom','')
                purchaseUser=cleaned_data.get('purchaseUser','')

                return cleaned_data


    class Meta:
         model = Purchase
         fields = '__all__'
###########################################################################
class AssetLifeForm(forms.ModelForm):
    woName=forms.CharField(label='دستور کار',required=False,widget=forms.TextInput(attrs={'class':'woselector','autocomplete':'off'}))
    # def __init__(self,*args,**kwargs):
    #
    #         self.asset_id = kwargs.pop('asset_id')
    #         print("######",self.asset_id)
    #         super(AssetLifeForm,self).__init__(*args,**kwargs)
    #         self.fields['assetWOAssoc'] = forms.ModelChoiceField(label="دستور کاری",queryset=WorkOrder.objects.filter(woAsset=self.asset_id),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
    # assetWOAssoc = forms.CharField()

    def clean(self):
                self.is_valid()
                cleaned_data=super(AssetLifeForm, self).clean()
                assetLifeAssetid=cleaned_data.get('assetLifeAssetid','')
                assetOfflineFrom=cleaned_data.get('assetOfflineFrom','')
                assetSetOfflineByUser=cleaned_data.get('assetSetOfflineByUser','')
                assetStopCode=cleaned_data.get('assetStopCode','')
                # assetOfflineStatus=cleaned_data.get('assetOfflineStatus','')
                assetWOAssoc=cleaned_data.get('assetWOAssoc','')
                assetOfflineAdditionalInfo=cleaned_data.get('assetOfflineAdditionalInfo','')
                assetEventType=cleaned_data.get('assetEventType','')
                assetEventDescription=cleaned_data.get('assetEventDescription','')
                assetCheckEvent=cleaned_data.get('assetCheckEvent','')
                assetCauseCode=cleaned_data.get('assetCauseCode','')
                if(cleaned_data.get('assetOnlineStatus','')!='-1'):
                    assetOnlineFrom=cleaned_data.get('assetOnlineFrom','')
                    assetSetOnlineByUser=cleaned_data.get('assetSetOnlineByUser','')
                    assetOnlineStatus=cleaned_data.get('assetOnlineStatus','')
                    assetOnlineAdditionalInfo=cleaned_data.get('assetOnlineAdditionalInfo','')
                assetOnlineProducteHourAffected=cleaned_data.get('assetOnlineProducteHourAffected','0')
                return cleaned_data
    class Meta:
         model = AssetLife
         fields = '__all__'
         widgets = {
          'assetOfflineAdditionalInfo': forms.Textarea(attrs={'rows':2, 'cols':15}),
          'assetEventDescription': forms.Textarea(attrs={'rows':2, 'cols':15}),
        }


###########################################################################
class PartForm(forms.ModelForm):
    partcategorytxt = forms.CharField(label='دسته بندی',required=False,widget=forms.TextInput(attrs={'autocomplete':'off'}))
    partDescription = forms.CharField( label="توضیحات",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )

    class Meta:
        model = Part
        fields = '__all__'



class PartForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(PartForm2, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['partName'].required = False
        self.fields['partCode'].required = False
        self.fields['partDescription'].required = False
    # partNote = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    # partNotes = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    # partName = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    # partCode = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    partNotes = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    partLastPrice = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    partModel = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    partBarcode = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    partMake = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    partChargeDepartment = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    partAccount = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())
    def clean(self):
        self.is_valid()
        cleaned_data=super(PartForm2, self).clean()
        partName=cleaned_data.get('partName','')
        partDescription=cleaned_data.get('partDescription','')
        partCode=cleaned_data.get('partCode','')
        # partNote=cleaned_data.get('partNote','')
        return cleaned_data

    class Meta:
        model = Part
        fields = ('partName','partDescription','partCode')
########################################################################

class PartStockForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):

             # self.asset_id = kwargs.pop('asset_id')
             # print("######",self.asset_id)
             super(PartStockForm,self).__init__(*args,**kwargs)
             self.fields['location'] = forms.ModelChoiceField(label="مکان",queryset=Asset.objects.filter(assetIsStock=True),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}))

    def clean(self):
         self.is_valid()
         cleaned_data=super(PartStockForm, self).clean()
         stockItem=cleaned_data.get('stockItem','')
         location=cleaned_data.get('location','')
         qtyOnHand=cleaned_data.get('qtyOnHand','')
         minQty=cleaned_data.get('minQty','')
         row=cleaned_data.get('row','')
         bin=cleaned_data.get('bin','')
         return cleaned_data
    class Meta:
        model = Stock
        fields = '__all__'

######################################################


# class AssetForm(forms.ModelForm):
#
#     class Meta:
#         model = Asset
#         fields = '__all__'

class PartLocationForm(forms.ModelForm):
    def clean(self):
                 self.is_valid()
                 cleaned_data=super(PartLocationForm, self).clean()
                 assetPartAssetid=cleaned_data.get('assetPartAssetid','')
                 assetPartPid=cleaned_data.get('assetPartPid','')
                 assetPartQnty=cleaned_data.get('assetPartQnty','')


                 return cleaned_data
    class Meta:
        model = AssetPart
        fields = '__all__'


##############################################################################
class PartUserForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(PartUserForm, self).clean()
                PartUserPartId=cleaned_data.get('PartUserPartId','')
                PartUserUserId=cleaned_data.get('PartUserUserId','')



                return cleaned_data


    class Meta:
         model = PartUser
         fields = '__all__'
#####################################################################
class PartWarantyForm(forms.ModelForm):

    def clean(self):


                self.is_valid()
                cleaned_data=super(PartWarantyForm, self).clean()
                warantyType=cleaned_data.get('warantyType','')
                warantyProvider=cleaned_data.get('warantyProvider','')
                warantyUsageTermType=cleaned_data.get('warantyUsageTermType','')
                warantyDataAdded=cleaned_data.get('warantyDataAdded','')
                warantyUsageTermType=cleaned_data.get('warantyUsageTermType','')
                warantyCertificationNumber=cleaned_data.get('warantyCertificationNumber','')
                warantyUsageTermType=cleaned_data.get('warantyUsageTermType','')
                warantyStockItem=cleaned_data.get('warantyStockItem','')
                warantyMeterReadingValueLimit=cleaned_data.get('warantyMeterReadingValueLimit','')
                warantyMeterReadingUnit=cleaned_data.get('warantyMeterReadingUnit','')
                warantyQnty=0
                return cleaned_data


    class Meta:
         model = PartWaranty
         fields = '__all__'

class PartBusinessForm(forms.ModelForm):


    def clean(self):


                self.is_valid()
                cleaned_data=super(PartBusinessForm, self).clean()
                BusinessPartPart=cleaned_data.get('BusinessPartPart','')
                businessPartBusiness=cleaned_data.get('businessPartBusiness','')
                businessPartBusinessType=cleaned_data.get('businessPartBusinessType','')
                businessPartSupplierPartNumber=cleaned_data.get('businessPartSupplierPartNumber','')
                businessPartCatalog=cleaned_data.get('businessPartCatalog','')
                businessPartisDefault=cleaned_data.get('businessPartisDefault','')

                return cleaned_data


    class Meta:
         model = BusinessPart
         fields = '__all__'

########################################################################
class PartPurchaseForm(forms.ModelForm):
        #for update purpose ,updating stock
        # prevQNTY = forms.CharField(label="مقدار قبلی",required=False,widget=forms.H())
        def __init__(self,*args,**kwargs):

                 # self.stockID = kwargs.pop('stockID')
                 # print("######",self.asset_id)
                 super(PartPurchaseForm,self).__init__(*args,**kwargs)
                 # self.fields['purchaseStock'] = forms.ModelChoiceField(label="مکان",queryset=Stock.objects.filter(stockItem=stockID),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}))
                 self.fields['purchaseStock'] = forms.ModelChoiceField(label="مکان",queryset=Asset.objects.filter(assetIsStock=True),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}))


        def clean(self):

                self.is_valid()
                cleaned_data=super(PartPurchaseForm, self).clean()
                purchasePartId=cleaned_data.get('purchasePartId','')
                purchaseDateOrdered=cleaned_data.get('purchaseDateOrdered','')
                purchasePriceTotla=cleaned_data.get('purchasePriceTotla','')
                purchaseCurrency=cleaned_data.get('purchaseCurrency','')
                purchaseDateRecieved=cleaned_data.get('purchaseDateRecieved','')
                purchaseDateofExpire=cleaned_data.get('purchaseDateofExpire','')
                purchaseDateRecieved=cleaned_data.get('purchaseDateRecieved','')
                purchasedFrom=cleaned_data.get('purchasedFrom','')
                purchaseUser=cleaned_data.get('purchaseUser','')
                purchasePricePerUnit=cleaned_data.get('purchasePricePerUnit','')
                purchaseStock=cleaned_data.get('purchaseStock','')
                purchaseQuantityReceived=cleaned_data.get('purchaseQuantityReceived','')
                # prevQNTY=cleaned_data.get('prevQNTY','')

                return cleaned_data


        class Meta:
         model = PartPurchase
         fields = '__all__'


class PartFileForm(forms.ModelForm):







    class Meta:
         model = PartFile
         fields = ('partFile',)

#############################################################################
class StockForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):

             # self.asset_id = kwargs.pop('asset_id')
             # print("######",self.asset_id)
             super(StockForm,self).__init__(*args,**kwargs)
             self.fields['location'] = forms.ModelChoiceField(label="مکان",queryset=Asset.objects.filter(assetIsStock=True),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}))

             self.fields['stockItem'].required = False
             self.fields['location'].required = False
             self.fields['qtyOnHand'].required = False
             self.fields['minQty'].required = False
             self.fields['row'].required = False
             self.fields['bin'].required = False
    mypart = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())


    def clean(self):
                 self.is_valid()
                 cleaned_data=super(StockForm, self).clean()
                 # stockItem=cleaned_data.get('stockItem','')
                 location=cleaned_data.get('location','')
                 qtyOnHand=cleaned_data.get('qtyOnHand','')
                 minQty=cleaned_data.get('minQty','')
                 row=cleaned_data.get('row','')
                 bin=cleaned_data.get('bin','')
                 return cleaned_data
    class Meta:
        model = Stock
        fields = '__all__'

######################################################
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
class SysUserForm(forms.ModelForm):
    #CustomerId = forms.ModelChoiceField(queryset=Customer.objects.all())


    class Meta:
        model = SysUser
        fields = '__all__'
class SysUserImageForm(forms.ModelForm):
    #CustomerId = forms.ModelChoiceField(queryset=Customer.objects.all())


    class Meta:
        model = SysUser
        fields = ('profileImage', )


class BusinessForm(forms.ModelForm):

    class Meta:
        model = Business
        fields = '__all__'
class BOMGroupForm(forms.ModelForm):
    is_new=forms.IntegerField(label="مقدار قبلی",required=False)

    class Meta:
        model = BOMGroup
        fields = '__all__'
class BatchMeterGroupForm(forms.ModelForm):

    class Meta:
        model = BatchMeterGroup
        fields = '__all__'
class BusinessFileForm(forms.ModelForm):







    class Meta:
         model = BusinessFile
         fields = ('businessFile',)


class BusinessAssetForm(forms.ModelForm):

    def clean(self):


                self.is_valid()
                cleaned_data=super(BusinessAssetForm, self).clean()
                BusinessAssetAsset=cleaned_data.get('BusinessAssetAsset','')
                businessAssetBusiness=cleaned_data.get('businessAssetBusiness','')
                businessAssetBusinessType=cleaned_data.get('businessAssetBusinessType','')
                businessAssetSupplierPartNumber=cleaned_data.get('businessAssetSupplierPartNumber','')
                businessAssetCatalog=cleaned_data.get('businessAssetCatalog','')
                businessAssetisDefault=cleaned_data.get('businessAssetisDefault','')

                return cleaned_data


    class Meta:
         model = BusinessAsset
         fields = '__all__'


class BusinessPartForm(forms.ModelForm):
    mypart = forms.CharField(label="نام قطعه",required=False,widget=forms.TextInput())

    def clean(self):
                self.is_valid()
                cleaned_data=super(BusinessPartForm, self).clean()
                BusinessPartPart=cleaned_data.get('BusinessPartPart','')
                businessPartBusiness=cleaned_data.get('businessPartBusiness','')
                businessPartBusinessType=cleaned_data.get('businessPartBusinessType','')
                businessPartSupplierPartNumber=cleaned_data.get('businessPartSupplierPartNumber','')
                businessPartCatalog=cleaned_data.get('businessPartCatalog','')
                businessPartisDefault=cleaned_data.get('businessPartisDefault','')

                return cleaned_data


    class Meta:
         model = BusinessPart
         fields = '__all__'

#############################################################
class MessageForm(forms.ModelForm):
    toUser = forms.ModelChoiceField(label="مخاطب",queryset=SysUser.objects.filter(userStatus=True))
    def clean_messageStatus(self):
        if(self.isupdated):
            messageStatus=3
        else:
            messageStatus=2

        return messageStatus



    class Meta:
        model = Message
        fields = '__all__'
###############################################################
class ProjectForm(forms.ModelForm):
    def clean_ProjectStartDate(self):
                # self.is_valid()
                # cleaned_data=super(ProjectForm, self).clean()
                value=DateJob.getDate2(self.cleaned_data['ProjectStartDate'])
                return value
    def clean_ProjectEndDate(self):
                # self.is_valid()
                # cleaned_data=super(ProjectForm, self).clean()
                # print("#############",DateJob.getDate2(self.cleaned_data['ProjectEndDate']))
                value=DateJob.getDate2(self.cleaned_data['ProjectEndDate'])
                return value
    def clean_ProjectActualStartDate(self):
                # self.is_valid()
                # cleaned_data=super(ProjectForm, self).clean()
                # print("#############",DateJob.getDate2(self.cleaned_data['ProjectEndDate']))
                value=DateJob.getDate2(self.cleaned_data['ProjectActualStartDate'])
                return value
    def clean_ProjectActualEndDate(self):
                # self.is_valid()
                # cleaned_data=super(ProjectForm, self).clean()
                # print("#############",DateJob.getDate2(self.cleaned_data['ProjectEndDate']))
                value=DateJob.getDate2(self.cleaned_data['ProjectActualEndDate'])
                return value

    class Meta:
        model = Project
        fields = '__all__'
###############################################################
class ProjectUserForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(ProjectUserForm, self).clean()
                ProjectUserId=cleaned_data.get('ProjectUserId','')
                ProjectUserUserId=cleaned_data.get('ProjectUserUserId','')
                return cleaned_data


    class Meta:
         model = ProjectUser
         fields = '__all__'
########################################################################

class ProjectFileForm(forms.ModelForm):







    class Meta:
         model = ProjectFile
         fields = ('projectFile',)


###############################################################
class EventForm(forms.ModelForm):

    class Meta:
        model = Events
        fields = '__all__'
###############################################################
class MaintenanceTypeForm(forms.ModelForm):

    class Meta:
        model = MaintenanceType
        fields = '__all__'
###############################################################
class AttendanceForm(forms.ModelForm):
    def clean_datecreated(self):
        value=DateJob.getDate2( self.cleaned_data['datecreated'])
        # print(value,'****************************')
        return value

    class Meta:
        model = Attendance
        fields = '__all__'
###############################################################
class AssetCategoryForm(forms.ModelForm):

    class Meta:
        model = AssetCategory
        fields = '__all__'
###############################################################
###############################################################
class PartCategoryForm(forms.ModelForm):

    class Meta:
        model = PartCategory
        fields = '__all__'
###############################################################
class MachineCategoryForm(forms.ModelForm):

    class Meta:
        model = MachineCategory
        fields = '__all__'
#############################################
class SysUserForm(forms.ModelForm):

    class Meta:
        model = SysUser
        fields = '__all__'
################################################
class UserFileForm(forms.ModelForm):
    class Meta:
         model = UserFile
         fields = ('userFile',)
################################################
class UserCertificationForm(forms.ModelForm):

    def clean(self):
                self.is_valid()
                cleaned_data=super(UserCertificationForm, self).clean()
                userCertificationName=cleaned_data.get('userCertificationName','')
                userCertificationUser=cleaned_data.get('userCertificationUser','')
                userCertificationType=cleaned_data.get('userCertificationType','')
                userCertificationDesc=cleaned_data.get('userCertificationDesc','')
                userCertificationStart=cleaned_data.get('userCertificationStart','')
                userCertificationEnd=cleaned_data.get('userCertificationEnd','')

                return cleaned_data
    # def clean_userCertificationStart(self):
    #     print("######################")
    #     value=DateJob.getDate(self.cleaned_data['userCertificationStart'])
    #     return value
    # def clean_userCertificationEnd(self):
    #      print("######################")
    #      value=DateJob.getDate(self.cleaned_data['userCertificationEnd'])
    #      return value
    class Meta:
         model = UserCertification
         fields = '__all__'
########################################################################
class ProblemCodeForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(ProblemCodeForm, self).clean()
                problemCode=cleaned_data.get('problemCode','')
                problemDescription=cleaned_data.get('problemDescription','')
                problemIsActive=cleaned_data.get('problemIsActive','')
                return cleaned_data
    class Meta:
         model = ProblemCode
         fields = '__all__'
########################################################################
########################################################################
class StopCodeForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(StopCodeForm, self).clean()
                problemCode=cleaned_data.get('stopCode','')
                problemDescription=cleaned_data.get('stopDescription','')

                return cleaned_data
    class Meta:
         model = StopCode
         fields = '__all__'
class MeterCodeForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(MeterCodeForm, self).clean()
                meterCode=cleaned_data.get('meterCode','')
                meterDescription=cleaned_data.get('meterDescription','')
                meterAbbr=cleaned_data.get('meterAbbr','')

                return cleaned_data
    class Meta:
         model = MeterCode
         fields = '__all__'
class MiscCostCodeForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(MiscCostCodeForm, self).clean()
                miscCostCode=cleaned_data.get('miscCostCode','')
                miscCostDescription=cleaned_data.get('miscCostDescription','')

                return cleaned_data
    class Meta:
         model = MiscCostCode
         fields = '__all__'
class DashAssetForm(forms.ModelForm):
    settingLocation= forms.ModelChoiceField(label="مکان",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
    def clean(self):
                self.is_valid()
                cleaned_data=super(DashAssetForm, self).clean()
                settingEqAsset=cleaned_data.get('settingEqAsset','')
                settingLocation=cleaned_data.get('settingLocation','')

                return cleaned_data
    class Meta:
         model = AssetTypeSetting
         fields = ["settingEqAsset","settingLocation"]
########################################################################
class PertCodeForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(PertCodeForm, self).clean()
                pertCode=cleaned_data.get('pertCode','')
                pertDescription=cleaned_data.get('pertDescription','')

                return cleaned_data
    class Meta:
         model = PertCode
         fields = '__all__'
########################################################################
class UserGroupForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(UserGroupForm, self).clean()
                userGroupCode=cleaned_data.get('userGroupCode','')
                userGroupName=cleaned_data.get('userGroupName','')
                userGroupIsPartOF=cleaned_data.get('userGroupIsPartOF','')
                userUserLocation=cleaned_data.get('userUserLocation','')
                userGroupZarib=cleaned_data.get('userGroupZarib','')
                userGroupZaribTamir=cleaned_data.get('userGroupZaribTamir','')
                userGroupZaribService=cleaned_data.get('userGroupZaribService','')
                userGroupZaribProject=cleaned_data.get('userGroupZaribProject','')
                return cleaned_data
    class Meta:
         model = UserGroup
         fields = '__all__'
########################################################################
class OfflineStatusForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(OfflineStatusForm, self).clean()
                Code=cleaned_data.get('Code','')
                name=cleaned_data.get('name','')
                description=cleaned_data.get('description','')
                return cleaned_data
    class Meta:
         model = OfflineStatus
         fields = '__all__'
########################################################################
class KpiExceptionForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(KpiExceptionForm, self).clean()
                stopcode=cleaned_data.get('stopcode','')

                return cleaned_data
    class Meta:
         model = KpiException
         fields = '__all__'
########################################################################
class CauseCodeForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(CauseCodeForm, self).clean()
                causeCode=cleaned_data.get('causeCode','')
                causeDescription=cleaned_data.get('causeDescription','')
                causeIsActive=cleaned_data.get('causeIsActive','')
                return cleaned_data
    class Meta:
         model = CauseCode
         fields = '__all__'
########################################################################
########################################################################
class EquipmentCostSettingForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(EquipmentCostSettingForm, self).clean()
                settingEqAsset=cleaned_data.get('settingEqAsset','')

                return cleaned_data
    class Meta:
         model = EquipmentCostSetting
         fields = '__all__'
########################################################################
class ActionCodeForm(forms.ModelForm):
    def clean(self):
                self.is_valid()
                cleaned_data=super(ActionCodeForm, self).clean()
                actionCode=cleaned_data.get('actionCode','')
                actionDescription=cleaned_data.get('actionDescription','')
                actionIsActive=cleaned_data.get('actionIsActive','')
                return cleaned_data
    class Meta:
         model = ActionCode
         fields = '__all__'
################################################
class AdSetForm(forms.ModelForm):
    class Meta:
         model = AdminSetting
         fields = '__all__'
#########################################
class PurchaseRequestForm(forms.ModelForm):
    def __init__(self,userid=None,*args,**kwargs):

        super (PurchaseRequestForm,self ).__init__(*args,**kwargs) # populates the post
        try:
            self.fields['PurchaseRequestAsset'].queryset=Asset.objects.none()
            print(self.data)
            if 'PurchaseRequestAssetMakan' in self.data:
                    try:
                        country_id = int(self.data.get('PurchaseRequestAssetMakan'))
                        self.fields['PurchaseRequestAsset'].queryset = Asset.objects.filter(assetIsLocatedAt=country_id).order_by('-id')
                    except (ValueError, TypeError):
                        pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                    self.fields['PurchaseRequestAsset'].queryset = Asset.objects.filter(assetIsLocatedAt=self.instance.PurchaseRequestAssetMakan)


            if(userid):
                user=SysUser.objects.get(userId=userid)
                print(user)
                if(user.userId.username =="admin"):
                    print("not admin")
                    self.fields['PurchaseRequestRequestedUser'].queryset = SysUser.objects.filter(userStatus=True)#books #AssetMeterTemplate.objects.filter(assetMeterTemplateAsset=WorkOrder.objects.get(id=workorder).woAsset)
                else:
                    print(" is admin")
                    self.fields['PurchaseRequestRequestedUser'].queryset = SysUser.objects.filter(userId=userid)

            else:
                self.fields['PurchaseRequestRequestedUser'].queryset = SysUser.objects.none()
        except Exception as ex:
            print(ex)
    mypart=forms.CharField(required=False)
    mywo=forms.CharField(required=False)
    PurchaseRequestAssetMakan= forms.ModelChoiceField(label="نام مکان",required=False,queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
    # PurchaseRequestAsset= forms.ModelChoiceField(required=False,label="دارایی ",queryset=Asset.objects.all(),
    # widget=forms.Select())
    # PurchaseRequestAssetNotInInventory = forms.CharField( label="ناموجود در انبار؟ اطلاعات بیشتری شرح دهید",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )
    PurchaseRequestMoreInfo = forms.CharField( label="اطلاعات بیشتر",widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),required=False )

    def clean_PurchaseRequestDateTo(self):
        if(self.cleaned_data['PurchaseRequestDateTo']):
             # print(self.cleaned_data['PurchaseRequestDateTo'],'datecompleted')
             value=DateJob.getDate2( self.cleaned_data['PurchaseRequestDateTo'])
             return value
        else:
            return None

    class Meta:
        model = PurchaseRequest
        exclude = ('PurchaseRequestNotInList',)


##########################################
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
class SimpleReportForm(forms.Form):
    #
    # def __init__(self):
    #     super(SimpleReportForm, self).__init__()
    #     # self.fields['maintenanceType'].queryset =MaintenanceType.objects.all()

        # print("12312312##########################")

    OPTIONS = (
        ("a", "A"),
        ("b", "B"),
        )

    FRUIT_CHOICES= [
        ('orange', 'Oranges'),
        ('cantaloupe', 'Cantaloupes'),
        ('mango', 'Mangoes'),
        ('honeydew', 'Honeydews'),
    ]
    mainType=MaintenanceType.objects.all()

    # renderformat = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all())
    to_date = forms.CharField(label='date 2')
    from_date = forms.CharField(label='date 1', initial=DateJob.getTodayDate())
    # MaintenanceType = forms.CharField(label='Your name', max_length=100)
class SimpleReportForm2(forms.Form):
    #
    # def __init__(self):
    #     super(SimpleReportForm2, self).__init__()
    #     self.fields['integer'].icon_name = 'icon-home'
    #     # self.fields['maintenanceType'].queryset =MaintenanceType.objects.all()

        # print("12312312##########################")

    OPTIONS = (
        ("a", "A"),
        ("b", "B"),
        )

    FRUIT_CHOICES= [
        ('orange', 'Oranges'),
        ('cantaloupe', 'Cantaloupes'),
        ('mango', 'Mangoes'),
        ('honeydew', 'Honeydews'),
    ]
    # mainType=MaintenanceType.objects.all()

    # renderformat = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    # maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all())
    to_date = forms.CharField(label='date 2')
    from_date = forms.CharField(label='date 1', initial=DateJob.getTodayDate())
    # MaintenanceType = forms.CharField(label='Your name', max_length=100)
class UpcommingScheduledMaintenanceList(forms.Form):
#     Description
# This report lists all of the upcoming active scheduled maintenances that will be created between two dates.
# The dates must be now or any time in the future (up to 13 months).
#
# Instructions
# Click 'Run' and choose all the relevant parameters
#
# Report Category
# Forecasting Reports
    #
    # def __init__(self):
    #     super(SimpleReportForm, self).__init__()
    #     # self.fields['maintenanceType'].queryset =MaintenanceType.objects.all()

        # print("12312312##########################")

    OPTIONS = (
        ("pdf", "pdf"),
        ("b", "B"),
        )


    # mainType=MaintenanceType.objects.all()

    # renderformat = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    test="این گزارش کلیه موارد اصلی برنامه ریزی شده فعال را که بین دو تاریخ ایجاد می شود ، لیست می کند. تاریخ ها باید در حال حاضر یا هر زمان در آینده (حداکثر 13 ماه) باشد."
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,        widget=forms.Select,choices=OPTIONS,)
    startDate = forms.CharField(label='شروع',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='پایان',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
    assignUser = forms.ModelChoiceField(label="انتخاب کاربر",queryset=SysUser.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
    parentAsset = forms.ModelChoiceField(label="دارایی والد",queryset=Asset.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))

    ######################################
# class  LabourHoursByAsset(forms.Form):
#     #     Description
#     # This report lists all of the upcoming active scheduled maintenances that will be created between two dates. The dates must be now or any time in the future (up to 13 months).
#     #
#     # Instructions
#     # Click 'Run' and choose all the relevant parameters
#     #
#     # Report Category
#     # Forecasting Reports
#         #
#         # def __init__(self):
#         #     super(SimpleReportForm, self).__init__()
#         #     # self.fields['maintenanceType'].queryset =MaintenanceType.objects.all()
#
#             # print("12312312##########################")
#
#         OPTIONS = (
#             ("pdf", "pdf"),
#             ("b", "B"),
#             )
#
#
#         # mainType=MaintenanceType.objects.all()
#
#         # renderformat = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
#
#         reportType = forms.MultipleChoiceField(label="خروجی",required=False,        widget=forms.Select,choices=OPTIONS,)
#         assetCategory = forms.ModelChoiceField(label="نوع دارایی",queryset=AssetCategory.objects.all(),required=False,widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
#         parentAsset = forms.ModelChoiceField(label="دارایی والد",queryset=Asset.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
#         maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
#
#         assignUser = forms.ModelChoiceField(label="انتخاب کاربر",queryset=SysUser.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
#         to_date = forms.CharField(label='شروع',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
#         from_date = forms.CharField(label='پایان',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
#         #############################
class  WorkOrderPartUsageHistory(forms.Form):
            #	این نوع گزارش تمامی دسوتور کارهایی را که بین دو تاریخ مشخص قطعه مصرف کرده اند را لیست می کند
            #Report: [new] Work order part usage history, created between two dates
            #Report Category Inventory Control Reports
            OPTIONS = (
                (0, "pdf"),
                (1, "EXCEL"),
                )
            test="تاریخ را انتخاب کنید و سپس کلید اجرا را کلیک کنید"
            reportType = forms.MultipleChoiceField(label="خروجی",required=False,        widget=forms.Select,choices=OPTIONS)
            craeteAfter = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
            craeteBefore = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
            partName=forms.CharField(label='نام قطعه',required=False,widget=forms.TextInput(attrs={'class':'partselector','autocomplete':'off'}))
            part=forms.CharField(widget=forms.HiddenInput(),required=False)
class PartUsageHistory(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    #lists all work orders that have used a part within the time frame given. Managers can use this to spot any trends over time. This report can be customized, MA provides a paid report customization service. See maintenanceassistant.com for more details.

    # Instructions
    # Provide a part to track the usage of and a start and end date for the analysis. Only work orders created in this window will be used.
    #
    # Report Category
    # Inventory Control Reports
    test="تاریخچه مصرف یک قطعه را در بازه زمانی مشخص، پیگیری کنید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,        widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    # partName = forms.ModelChoiceField(label="قطعه",queryset=Part.objects.all(),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}))
    partName=forms.CharField(label='نام قطعه',required=False,widget=forms.TextInput(attrs={'class':'partselector','autocomplete':'off'}))
    part=forms.CharField(widget=forms.HiddenInput(),required=False)

    #####################################################################################
class OveralPartUsageHistory(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    #lists all work orders that have used a part within the time frame given. Managers can use this to spot any trends over time. This report can be customized, MA provides a paid report customization service. See maintenanceassistant.com for more details.

    # Instructions
    # Provide a part to track the usage of and a start and end date for the analysis. Only work orders created in this window will be used.
    #
    # Report Category
    # Inventory Control Reports
    test="گزارش مصرف قطعه بین دو  تاریخ"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,        widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    # partName = forms.ModelChoiceField(label="قطعه",queryset=Part.objects.all(),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}))


#######################################
class AssetList(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    # def __init__(self):
    #     super(AssetList, self).__init__()
    #     print(type(self.assetCatOPTIONS),"::::!!!!!!!!!!!!!!!!!!!!!")
        # self.fields['maintenanceType'].queryset =MaintenanceType.objects.all()

    #lists all work orders that have used a part within the time frame given. Managers can use this to spot any trends over time. This report can be customized, MA provides a paid report customization service. See maintenanceassistant.com for more details.

    # Instructions
    # Provide a part to track the usage of and a start and end date for the analysis. Only work orders created in this window will be used.
    #
    # Report Category
    # Inventory Control Reports
    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    # assetCategory = forms.MultipleChoiceField(label="دسته اموال",required=False,widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}),choices=assetCatOPTIONS)
    # location = forms.ModelChoiceField(label="اموال",queryset=Asset.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    categoryText = GroupedModelChoiceField(label='دسته دارایی',
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',empty_label=None,
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
    # location = forms.CharField(label='مکان',required=False,widget=forms.TextInput(attrs={'class':'assetselector','autocomplete':'off'}))
    # locationVal=forms.CharField(widget=forms.HiddenInput(),required=False)
    locationVal = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetTypes=1),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    ################
    # location = GroupedModelChoiceField(
    #     queryset=Asset.objects.filter(assetTypes=1),#exclude(assetCategory=None),
    #     choices_groupby='assetIsPartOf',
    #     widget=forms.Select(attrs={'class':'selectpicker assetselector','multiple':'','data-live-search':'true'}))
    #################################
        #forms.ModelChoiceField(label="قطعه",queryset=Asset.objects.filter(assetType=1),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}))

        # categoryText=forms.CharField(label='خ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    #####################################################################################
class DowntimeByRepairTypeByAssetCategory(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

    #This report gives a graphical summary of the downtime and reasons
    #for downtime between a specific period for a specific category.
    #Downtime is calculated as the time between setting a system offline to online.
    #Using the input timelines, users can view data by the week, month, quarter, year etc.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class DowntimeByCause(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

    #This report gives a graphical summary of the downtime and reasons
    #for downtime between a specific period for a specific category.
    #Downtime is calculated as the time between setting a system offline to online.
    #Using the input timelines, users can view data by the week, month, quarter, year etc.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class MTTRALL(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

   # this report lists the mean time to repair for all assets.
   # It represents the average time required to complete the repair
   #  on the asset.
   #   MTTR measures of the mean time between the point
   #   at which the failure is first discovered until the
   #   point at which the equipment returns to operation.
   #   Expressed mathematically, it is the total corrective maintenance time divided
   #    by the total number of corrective maintenance actions during a given period of time.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    category = GroupedModelChoiceField(label="دسته بندی",required=False,
        queryset=AssetCategory.objects.all(),empty_label=None,
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1),empty_label=None,
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))

class MTTRByCategory(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

   # this report lists the mean time to repair for all assets.
   # It represents the average time required to complete the repair
   #  on the asset.
   #   MTTR measures of the mean time between the point
   #   at which the failure is first discovered until the
   #   point at which the equipment returns to operation.
   #   Expressed mathematically, it is the total corrective maintenance time divided
   #    by the total number of corrective maintenance actions during a given period of time.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',required=False,
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'})
    )
class MTBFALL(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

   # this report lists the mean time to repair for all assets.
   # It represents the average time required to complete the repair
   #  on the asset.
   #   MTTR measures of the mean time between the point
   #   at which the failure is first discovered until the
   #   point at which the equipment returns to operation.
   #   Expressed mathematically, it is the total corrective maintenance time divided
   #    by the total number of corrective maintenance actions during a given period of time.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
class MTBFByCategory(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

   # this report lists the mean time to repair for all assets.
   # It represents the average time required to complete the repair
   #  on the asset.
   #   MTTR measures of the mean time between the point
   #   at which the failure is first discovered until the
   #   point at which the equipment returns to operation.
   #   Expressed mathematically, it is the total corrective maintenance time divided
   #    by the total number of corrective maintenance actions during a given period of time.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'})
    )
class OverdueWorkOrdersDetailReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )

   # List of open work orders that passed expected completion date.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),empty_label=None,
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),empty_label=None,
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),empty_label=None,
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",empty_label=None,
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class OpenWorkOrdersDetailReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )

   # List of open work orders that passed expected completion date.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class WorkOrdersDetailReportByStatus(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )
    Requested=1
    onHold=2
    Draft=3
    Assigned=4
    Open=5
    workInProgress=6
    closedComplete=7
    closedIncomplete=8
    waitingForPart=9
    invisible=-1
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Status=(
         (Requested,'درخواست شده')  ,
         (onHold,'متوقف'),
         (Assigned,'تخصیص داده شده'),
         (Open,'باز'),
         (workInProgress,'در حال پیشرفت'),
         (closedComplete,'بسته شده کامل'),
         (closedIncomplete,'بسته شده، ناقص'),
         (waitingForPart,'در انتظار قطعه'),

     )

   # List of open work orders that passed expected completion date.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    StatusType = forms.MultipleChoiceField(label="وضعیت",required=False,widget=forms.Select,choices=Status)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class CloseWorkOrdersDetailReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )

   # List of open work orders that passed expected completion date.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class AllWorkOrdersDetailReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )

   # List of open work orders that passed expected completion date.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class OpenWorkOrdersListReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )

   # This report displays the list of all open work orders assigned to a maintenance type
   #, parent asset, asset category, priority, and assigned to user, created between two dates.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class WorkOrdersListReportByStatus(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )
    Requested=1
    onHold=2
    Draft=3
    Assigned=4
    Open=5
    workInProgress=6
    closedComplete=7
    closedIncomplete=8
    waitingForPart=9
    invisible=-1
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Status=(
         (Requested,'درخواست شده')  ,
         (onHold,'متوقف'),
         (Assigned,'تخصیص داده شده'),
         (Open,'باز'),
         (workInProgress,'در حال پیشرفت'),
         (closedComplete,'بسته شده کامل'),
         (closedIncomplete,'بسته شده، ناقص'),
         (waitingForPart,'در انتظار قطعه'),

     )

   # This report displays the list of all open work orders assigned to a maintenance type
   #, parent asset, asset category, priority, and assigned to user, created between two dates.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    statusType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=Status)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class CloseWorkOrdersListReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )

   # This report displays the list of all open work orders assigned to a maintenance type
   #, parent asset, asset category, priority, and assigned to user, created between two dates.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class OpenPMWorkOrdersListReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )

  #This report displays the list of all open PM work orders assigned to a maintenance type,
  # parent asset, asset category, priority, and assigned to user, created between two dates.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assignUser = forms.ModelChoiceField(label="کاربر",queryset=SysUser.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class RequestedWorkOrdersListReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Highest=1
    High=2
    Medium=3
    Low=4
    Lowest=5
    Priority=(
    (Highest,'خیلی زیاد'),
    (High,'زیاد'),
    (Medium,'متوسط'),
    (Low,'پایین'),
    (Lowest,'خیلی پایین'),
    )

   # This report displays the list of all open work orders assigned to a maintenance type
   #, parent asset, asset category, priority, and assigned to user, created between two dates.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))

    priorityType = forms.MultipleChoiceField(label="اولویت",choices=Priority,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class OpenWorkOrderGraphReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )


   # This report displays the list of all open work orders assigned to a maintenance type
   #, parent asset, asset category, priority, and assigned to user, created between two dates.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))


    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class CloseWorkOrderGraphReport(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )


   # This report displays the list of all open work orders assigned to a maintenance type
   #, parent asset, asset category, priority, and assigned to user, created between two dates.


    test="پارامترهای مربوطه را انتخاب کنید و سپس اجرا را فشار دهید"
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
    Asset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))


    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class ProjectsReportWithWorkOrderDetails(forms.Form):

    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    Requested=1
    onHold=2
    Draft=3
    Assigned=4
    Open=5
    workInProgress=6
    closedComplete=7
    closedIncomplete=8
    waitingForPart=9

    Status=(
         (Requested,'درخواست شده')  ,
         (onHold,'متوقف'),
         (Assigned,'تخصیص داده شده'),
         (Open,'باز'),
         (workInProgress,'در حال پیشرفت'),
         (closedComplete,'بسته شده کامل'),
         (closedIncomplete,'بسته شده، ناقص'),
         (waitingForPart,'در انتظار قطعه'),

     )


   # This report displays the list of all open work orders assigned to a maintenance type
   #, parent asset, asset category, priority, and assigned to user, created between two dates.


    test="تاریخ هایی را که پروژه مورد نظر برای شروع و به پایان رسیدن آن وارد شده است وارد<br> کنید. وضعیت WO هایی را که می خواهید در هر پروژه مشاهده کنید ، وارد کنید."
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=assetCatOPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    woStatus = forms.MultipleChoiceField(label="اولویت",choices=Status,widget=forms.Select(attrs={'class':'selectpicker','multiple':''}))
##########################Business metric Forms######################################
class FailureCodeCauseCount(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

# This report details the counts for cause failure codes on closed work orders for a particular period of time.
#
# * This report reports on data provided by functionality only available in the Enterprise CMMS

    test=""
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
##########################Business metric Forms######################################
class FailureCodeProblemCount(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

# This report details the counts for cause failure codes on closed work orders for a particular period of time.
#
# * This report reports on data provided by functionality only available in the Enterprise CMMS

    test=""
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class LabourHoursByAsset(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

# This report details the counts for cause failure codes on closed work orders for a particular period of time.
#
# * This report reports on data provided by functionality only available in the Enterprise CMMS

    test=""
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class LabourHoursByAssetTop10(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

# This report details the counts for cause failure codes on closed work orders for a particular period of time.
#
# * This report reports on data provided by functionality only available in the Enterprise CMMS

    test=""
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class  WorkOrderCostListReport(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

# This report lists the labor, parts and misc cost associated with work orders.
    test="""بر روی "اجرا" کلیک کرده و پارامترهای مربوطه را انتخاب کنید"""
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    parentAsset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class  WorkOrderCostDetailReport(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

# This report lists the labor, parts and misc cost associated with work orders.
    test="""بر روی "اجرا" کلیک کرده و پارامترهای مربوطه را انتخاب کنید"""
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    parentAsset = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
    categoryText = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
class  WorkOrderHoursLoggedbyTechnician(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    assetCatOPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )

# This report lists the labor, parts and misc cost associated with work orders.
    test="""لیست ساعت های سفارش کار برای یک تکنسین خاص در یک بازه زمانی مشخص وارد شده است. مدیران می توانند با استفاده از این ، هر روند را در طول زمان مشاهده کنند. """
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    userLink = forms.ModelChoiceField(label="نام کاربر",queryset=SysUser.objects.all(),widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}))
class SiteAssetSMSummaryReport(forms.Form):
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),
        )
    test="این گزارش دارایی های موجود در تسهیلات و SM های مربوطه را فهرست می کند."
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    asset = forms.ModelChoiceField(label="نام سایت",queryset=Asset.objects.filter(assetTypes=1),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
class UpcomingScheduledMaintenanceWithStockForecasting(forms.Form):
    test='در این گزارش لیست های اصلی برنامه ریزی شده فعال ، فیلتر شده با نوع نگهداری ، که بین دو تاریخ ایجاد می شود ، لیست می کند. این سهام موجود را به صورت دستی ذکر کرده و نشان می دهد که آیا مقدار سهام برای تأمین اعتبار برنامه ریزی شده آینده کافی است یا خیر.'
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    maintenanceType = forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),widget=forms.Select(attrs={'class':'selectpicker','multiple':'', 'data-live-search':'true'}))
class  ListOfOfflineAssets(forms.Form):
    test='لیست دارایی های متوقف'
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    category = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
class AssetOnlineAndOfflineHistory(forms.Form):
    test='این گزارش همه رویدادهای آفلاین / دارایی آنلاین را برای یک دوره معین پرتاب می کند. شما می توانید گزارش را بر اساس دارایی والدین ، ​​طبقه دارایی و دلیل تنظیم دارایی به صورت آفلاین فیلتر کنید.'
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    category = GroupedModelChoiceField(label="دسته بندی",
        queryset=AssetCategory.objects.all(),#exclude(assetCategory=None),
        choices_groupby='isPartOf',
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'})
    )
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    offlinecode = forms.ModelChoiceField(label="علت توقف",queryset=StopCode.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
class PartsReceivedIntoInventory(forms.Form):
    test='این گزارش موجودی است که در یک دوره خاص ، مطابق با کاربر مشخص شده ، در CMMS دریافت می کند.'
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
class InventoryPurchaseTransactionsBetween2Dates(forms.Form):
    test='معاملات موجودی موجودی بین 2 تاریخ'
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
class ListOfLowStockInventoryFilteredByLocation(forms.Form):
    test='لیست موجودی کم فیلتر شده توسط محل'
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
class UserGroupPerformance(forms.Form):
    test='عملکرد'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    usergroup = forms.ModelChoiceField(label="گروه کاری",queryset=UserGroup.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    maintenanceType= forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))

class IstgahReport(forms.Form):
    test='گزارش ایستگاهی'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    usergroup = forms.ModelChoiceField(label="گروه کاری",queryset=UserGroup.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    assetCategory= forms.ModelChoiceField(label="دسته بندی ماشین آلات",queryset=AssetCategory.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    maintenanceType= forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
class Amalkard3MaheReport(forms.Form):
    test='گزارش عملکرد سه ماهه'

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    SOPTIONS = (
        (3, "بهار"),
        (2, "تابستان"),
        (1, "پاییز"),
        (0, "زمستان"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    SType = forms.MultipleChoiceField(label="فصل",required=False,widget=forms.Select,choices=SOPTIONS)
    usergroup = forms.ModelChoiceField(label="گروه کاری",queryset=UserGroup.objects.all().exclude(userGroupCode='other'),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
class TahlilOfflineStatus(forms.Form):
    test='تحلیل علتهای توقف'

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    SOPTIONS = (
        (11, "فروردین"),
        (10, "اردیبهشت"),
        (9, "خرداد"),
        (8, "تیر"),
        (7, "مرداد"),
        (6, "شهریور"),
        (5, "مهر"),
        (4, "آبان"),
        (3, "آذر"),
        (2, "دی"),
        (1, "بهمن"),
        (0, "اسفند"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    SType = forms.MultipleChoiceField(label="ماه",required=False,widget=forms.Select,choices=SOPTIONS)
    causeCode = forms.ModelChoiceField(label="علت خرابی",queryset=CauseCode.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
class ShakhesTamirat(forms.Form):
    test='شاخص تعمیرات'

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    SOPTIONS = (
        (11, "فروردین"),
        (10, "اردیبهشت"),
        (9, "خرداد"),
        (8, "تیر"),
        (7, "مرداد"),
        (6, "شهریور"),
        (5, "مهر"),
        (4, "آبان"),
        (3, "آذر"),
        (2, "دی"),
        (1, "بهمن"),
        (0, "اسفند"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    SType = forms.MultipleChoiceField(label="ماه",required=False,widget=forms.Select,choices=SOPTIONS)
    usergroup = forms.ModelChoiceField(label="گروه کاری",queryset=UserGroup.objects.all().exclude(userGroupCode='other'),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
class UserGroupPerformanceWithGraph(forms.Form):
    test=' ازریابی گروههای کاری'

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    SOPTIONS = (
        (11, "فروردین"),
        (10, "اردیبهشت"),
        (9, "خرداد"),
        (8, "تیر"),
        (7, "مرداد"),
        (6, "شهریور"),
        (5, "مهر"),
        (4, "آبان"),
        (3, "آذر"),
        (2, "دی"),
        (1, "بهمن"),
        (0, "اسفند"),

        )
    SType = forms.MultipleChoiceField(label="ماه",required=False,widget=forms.Select,choices=SOPTIONS)
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    usergroup = forms.ModelChoiceField(label="گروه کاری",queryset=UserGroup.objects.all().exclude(userGroupCode='other'),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    maintenanceType= forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all().exclude(id=1),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    # show_nafar_sat = forms.BooleanField(label="نمایش نفر ساعت",required=False,widget=forms.CheckboxInput(attrs={'class':'check'}))
    # show_sat = forms.BooleanField(label="نمایش ساعت نگهداری",required=False,widget=forms.CheckboxInput(attrs={'class':'check'}))
class TotalTamirPerIstgah(forms.Form):
    test='تعمیرات ایستگاهها بر حسب ساعت'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))


    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )

    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))

    assetCategory = forms.ModelChoiceField(label="نوع دارایی",queryset=AssetCategory.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))

    # show_nafar_sat = forms.BooleanField(label="نمایش نفر ساعت",required=False,widget=forms.CheckboxInput(attrs={'class':'check'}))
    # show_sat = forms.BooleanField(label="نمایش ساعت نگهداری",required=False,widget=forms.CheckboxInput(attrs={'class':'check'}))
class GroupTamirPerIstgah(forms.Form):
    test='تعمیرات ایستگاهها بر حسب ساعت'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))


    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )

    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))

    assetCategory = forms.ModelChoiceField(label="نوع دارایی",queryset=AssetCategory.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    usergroup = forms.ModelChoiceField(label="گروه کاری",queryset=UserGroup.objects.all().exclude(userGroupCode='other'),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
class GroupTamirPerIstgahPerMonth(forms.Form):
    test='تعمیرات گروهی به تفکیک ماه'


    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    SOPTIONS = (
        (11, "فروردین"),
        (10, "اردیبهشت"),
        (9, "خرداد"),
        (8, "تیر"),
        (7, "مرداد"),
        (6, "شهریور"),
        (5, "مهر"),
        (4, "آبان"),
        (3, "آذر"),
        (2, "دی"),
        (1, "بهمن"),
        (0, "اسفند"),

        )
    SType = forms.MultipleChoiceField(label="ماه",required=False,widget=forms.Select,choices=SOPTIONS)

    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))

    assetCategory = forms.ModelChoiceField(label="نوع دارایی",queryset=AssetCategory.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    usergroup = forms.ModelChoiceField(label="گروه کاری",queryset=UserGroup.objects.all().exclude(userGroupCode='other'),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
class HozurTimePerGroup(forms.Form):
    test='ساعت حضور پرسنل واحدها بر حسب نوع نگهداری'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))


    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )

    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    location = forms.ModelChoiceField(label="دارایی",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))

    # assetCategory = forms.ModelChoiceField(label="نوع دارایی",queryset=AssetCategory.objects.all(),
    # widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
    usergroup = forms.ModelChoiceField(label="گروه کاری",queryset=UserGroup.objects.all().exclude(userGroupCode='other'),
    widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
class LogReport(forms.Form):
    test='گزارش فعالیت کاربران'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))


    OPTIONS = (
        ("workorder", "دستورکار"),
        ("asset", "دارایی"),
        ("part", "قطعه"),

        )

    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}),choices=OPTIONS)
class SummaryReportByUser(forms.Form):
    test='خلاصه وضعیت کار'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    maintenanceType= forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
    usernames= forms.ModelChoiceField(label="نام کاربر",queryset=SysUser.objects.filter(userStatus=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
class SummaryReportByAsset(forms.Form):
    test='خلاصه وضعیت تجهیز'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    maintenanceType= forms.ModelChoiceField(label="نوع نگهداری",queryset=MaintenanceType.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
    assetname= forms.ModelChoiceField(label="نام دستگاه",queryset=Asset.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
        #
class PartUsageByLocation(forms.Form):
    rcode=100
    test='خلاصه وضعیت تجهیز'
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    makan= forms.ModelChoiceField(label="نام مکان",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}),required=False)
    assetType= forms.ModelChoiceField(label="نوع دارایی",queryset=AssetCategory.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':''}),required=False,empty_label=None)
    assetname= forms.ModelChoiceField(label="نام دستگاه",queryset=Asset.objects.none(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':''}),required=False,empty_label=None)

class PartUsageByLocationandPart(forms.Form):
    test='گزارش مصرف قطعه بر اساس تجهیز و قطعه'
    rcode = 100 #برای استفاده در partialsimplereportform
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))

    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    makan= forms.ModelChoiceField(label="نام مکان",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
    assetType= forms.ModelChoiceField(label="نوع دارایی",queryset=AssetCategory.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':''}))
    assetname= forms.ModelChoiceField(label="نام دستگاه",queryset=Asset.objects.none(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':''}))
    partName=forms.CharField(label='نام قطعه',required=False,widget=forms.TextInput(attrs={'class':'partselector','autocomplete':'off'}))
    part=forms.CharField(widget=forms.HiddenInput(),required=False)
# class PartUsageByLocation(forms.Form):
#     test='گزارش قطعه بر اساس مکان'
#     rcode = 100 #برای استفاده در partialsimplereportform
#     startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
#     endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
#
#     OPTIONS = (
#         (0, "pdf"),
#         (1, "EXCEL"),
#
#         )
#     reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
#     makan= forms.ModelChoiceField(label="نام مکان",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
#     widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
#     assetType= forms.ModelChoiceField(label="نوع دارایی",queryset=AssetCategory.objects.all(),
#     widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':''}))

class AssetMeterLocation(forms.Form):
    test='گزارش مصرف قطعه بر اساس تجهیز و قطعه'
    rcode = 100 #برای استفاده در partialsimplereportform
    startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
    OPTIONS = (
        (0, "pdf"),
        (1, "EXCEL"),

        )
    reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
    makan= forms.ModelChoiceField(label="نام مکان",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
    assetType= forms.ModelChoiceField(empty_label=None,label="نوع دارایی",queryset=AssetCategory.objects.all(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':''}))
    assetname= forms.ModelChoiceField(label="نام دستگاه",queryset=Asset.objects.none(),
    widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':''}))










    # show_nafar_sat = forms.BooleanField(label="نمایش نفر ساعت",required=False,widget=forms.CheckboxInput(attrs={'class':'check'}))
    # show_sat = forms.BooleanField(label="نمایش ساعت نگهداری",required=False,widget=forms.CheckboxInput(attrs={'class':'check'}))
class MTBFByAnalythis(forms.Form):
        test='گزارش شاخص mtbf به صورت پایش دوره ای'
        rcode = 100 #برای استفاده در partialsimplereportform
        # startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        startDate = forms.IntegerField(label='سال',required=True)

        dovre = (
                (0, "1 ماهه"),


            )
        reportType2 = forms.MultipleChoiceField(label="دوره",required=False,widget=forms.Select,choices=dovre)

        OPTIONS = (
                (0, "pdf"),
                (1, "EXCEL"),

            )
        reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
        makan= forms.ModelChoiceField(label="نام مکان",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))

        assetname= forms.ModelChoiceField(label="نام دستگاه",queryset=Asset.objects.none(),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
        behbood = forms.IntegerField(label='بهبود',required=False)
        alarm = forms.IntegerField(label='آلارم',required=False)
class MTBFByAnalythisCauseCode(forms.Form):
        test=' گزارش mtbf  به همراه آنالیز علت'
        rcode = 100 #برای استفاده در partialsimplereportform
        # startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        startDate = forms.IntegerField(label='سال',required=True)

        dovre = (
                (0, "1 ماهه"),


            )
        reportType2 = forms.MultipleChoiceField(label="دوره",required=False,widget=forms.Select,choices=dovre)

        OPTIONS = (
                (0, "pdf"),
                (1, "EXCEL"),

            )
        reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
        makan= forms.ModelChoiceField(label="نام مکان",queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))

        assetname= forms.ModelChoiceField(label="نام دستگاه",queryset=Asset.objects.none(),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
        causeCode = forms.ModelChoiceField(label="علت خرابی",queryset=CauseCode.objects.all(),
        widget=forms.Select(attrs={'class':'selectpicker','multiple':'','data-live-search':'true'}))
        behbood = forms.IntegerField(label='بهبود',required=False)
        alarm = forms.IntegerField(label='آلارم',required=False)
class UpCommingServiceByUserAndDate(forms.Form):
        test=' سرویس های مربوط به یک کاربر'
        startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        # startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        OPTIONS = (
                (0, "pdf"),
                (1, "EXCEL"),

            )
        reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
        user= forms.ModelChoiceField(label="نام کاربر",queryset=SysUser.objects.filter(userStatus=True),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}))
class UpCommingServiceByDate(forms.Form):
        test=' سرویس های دورهای پیش رو'
        startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        assetname= forms.ModelChoiceField(label="نام مکان",empty_label=None,queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':'true'}))
        # startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        OPTIONS = (
                (0, "pdf"),
                (1, "EXCEL"),

            )
        reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
class DueServiceReport(forms.Form):
        test='سرویس های سر رسیده'
        startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        assetname= forms.ModelChoiceField(label="نام مکان",empty_label=None,queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':'true'}))
        # startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        OPTIONS = (
                (0, "pdf"),
                (1, "EXCEL"),

            )
        reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
class OverDueServiceReport(forms.Form):
        test='سرویس های منقضی '
        startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        endDate = forms.CharField(label='تا تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        assetname= forms.ModelChoiceField(label="نام مکان",empty_label=None,queryset=Asset.objects.filter(assetIsLocatedAt__isnull=True),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true','multiple':'true'}))
        # startDate = forms.CharField(label='از تاریخ',required=False,widget=forms.TextInput(attrs={'class':'datepicker'}))
        OPTIONS = (
                (0, "pdf"),
                (1, "EXCEL"),

            )
        reportType = forms.MultipleChoiceField(label="خروجی",required=False,widget=forms.Select,choices=OPTIONS)
