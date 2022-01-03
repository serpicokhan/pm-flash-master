'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(newobject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
import sys
import jdatetime
from datetime import date
from datetime import datetime
from datetime import timedelta
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from cmms.models.schedule import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import ScheduleForm
from cmms.business.schedule_utility import ScheduleUtility
from cmms.business.DateJob import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
###################################################################
def list_schedule(request,id=None):
    books = Schedule.objects.all()
    return render(request, 'cmms/schedule/scheduleList.html', {'schedule': books})


###################################################################
@permission_required('cmms.view_schedule')
def js_list_schedule(request,woId):
    data=dict()
    books=Schedule.objects.filter(workOrder=woId)
    if(books.count()>0):
        # print("#@!#!@#!@#@!")

        data['is_not_empty']=True
    else:
        data['is_not_empty']=False


    data['html_schedule_list']= render_to_string('cmms/schedule/partialScheduleList.html', {
        'schedules': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_schedule_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          #if form.is_valid():
             try:
                 if form.is_valid():
                     newItem=form.save()
                     ScheduleUtility.CreateNewWO(newItem.id)
                     data['form_is_valid'] = True
                     books = Schedule.objects.filter(workOrder=woId).order_by('id')
                     data['html_schedule_list'] = render_to_string('cmms/schedule/partialScheduleList.html', {
                         'schedules': books,
                         'perms': PermWrapper(request.user)
                     })
                 else:
                     fmt = getattr(settings, 'LOG_FORMAT', None)
                     lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                     logging.basicConfig(format=fmt, level=lvl)
                     logging.debug( form.errors)
             except Exception as e:
                print(e)
                print("error coour in form saved")
                exc_type, exc_obj, tb = sys.exc_info()
                print(tb.tb_lineno)
                print("form not saved",exc_type, exc_obj)
    context = {'form': form}
    data['html_schedule_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def schedule_delete(request, id):
        print("test")
    # try:
        comp1 = get_object_or_404(Schedule, id=id)
        woId=comp1.workOrder


        data = dict()

        if (request.method == 'POST'):
            if(comp1.schNextWo):
                comp1.schNextWo.delete()
            comp1.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            companies = Schedule.objects.filter(workOrder=woId)
            data['html_schedule_list'] = render_to_string('cmms/schedule/partialScheduleList.html', {
                'schedules': companies,
                'perms': PermWrapper(request.user)
            })
        else:
            context = {'schedule': comp1}
            data['html_schedule_form'] = render_to_string('cmms/schedule/partialScheduleDelete.html',
                context,
                request=request,
            )
        return JsonResponse(data)
    # except Exception as e:
        # print(e)
        # print("error in schedule deleting")


###################################################################
@csrf_exempt
def schedule_create(request):
    woId=-1
    if (request.method == 'POST'):
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            data = request.POST.dict()
            data['schChoices']=body['schChoices']
            data['workOrder']=body['workOrder']
            woId=data['workOrder']
            if(int(data['schChoices']==0)):
                data['schTriggerTime']=(body['schTriggerTime'])
                data['schCreateOnStartDate']=(body['schCreateOnStartDate'])
                # data['shStartDate']=(body['shStartDate'])
                data['shStartDate']=DateJob.getDate2(body['shStartDate'])
                # print(data['shStartDate'],'!!!!!!!!!!!!!!!!!')
                data['shHasEndDate']=True if body['shHasEndDate']==True else False
                # data['schNextWo']=body['schNextWo']
                if(data['shHasEndDate']==True):
                    data['shEndDate']=DateJob.getDate2(body['shEndDate'])
                else:
                    data['shEndDate']=None
                data['schHowOften']=body['schHowOften']
                if(int(data['schHowOften'])==1):
                    data['schHourRep']=body['schHourRep']
                    data['schHourIsFixed']=True if body['schHourIsFixed']=='True' else False
                    data['schDayIsFixed']=False
                    data['schMonthIsFixed']=False
                    data['schMonthIsFixed']=False
                    data['schMeterReadingIsFixed']=False
                    form = ScheduleForm(data)
                elif(int(data['schHowOften']==2)):
                     data['schDailyRep']=body['schDailyRep']
                     data['schDayIsFixed']=True if body['schDailyIsFixed']=='True' else False
                     #data['schDayIsFixed']=False
                     data['schMonthIsFixed']=False
                     data['schYearIsFixed']=False
                     data['schMeterReadingIsFixed']=False
                     form = ScheduleForm(data)
                elif(int(data['schHowOften']==3)):
                     data['schHourIsFixed']=False
                     data['schDayIsFixed']=False
                     data['schMonthIsFixed']=False
                     data['schYearIsFixed']=False
                     data['schWeeklyRep']=body['schWeeklyRep']
                     data['isSaturday']=True if body['isSaturday']=='true' else False
                     data['isSunday']=True if body['isSunday']=='true' else False
                     data['isMonday']=True if body['isMonday']=='true' else False
                     data['isTuesday']=True if body['isTuesday']=='true' else False
                     data['isWednenday']=True if body['isWednenday']=='true' else False
                     data['isThursday']=True if body['isThursday']=='true' else False
                     data['isFriday']=True if body['isFriday']=='true' else False
                     form = ScheduleForm(data)
                elif(int(data['schHowOften']==4)):
                         data['schDayofMonthlyRep']=body['schDayofMonthlyRep']
                         data['schMonthlyRep']=body['schMonthlyRep']
                         data['schMonthIsFixed']=True if body['schMonthIsFixed']=='True' else False
                         form = ScheduleForm(data)
                elif(int(data['schHowOften']==5)):
                         data['schHourIsFixed']=False
                         data['schDayIsFixed']=False
                         data['schMonthIsFixed']=False
                         data['schYearlyRep']=body['schYearlyRep']
                         data['schMonthOfYearRep']=body['schMonthOfYearRep']
                         data['schDayOfMonthOfYearRep']=body['schDayOfMonthOfYearRep']
                         data['schYearIsFixed']=True if body['schYearIsFixed']=='True' else False
                         form = ScheduleForm(data)
            elif(int(data['schChoices']==1)):
                data['schTriggerTime']=0
                data['schCreateOnStartDate']=False
                data['schHourIsFixed']=False
                data['schDayIsFixed']=False
                data['schMonthIsFixed']=False
                data['schYearIsFixed']=False
                data['schAsset']=body['schAsset']

                data['shMeterReadingHasTiming']=True if body['whenreading']==0 else False
                if(int(body['whenreading'])==0):
                    try:
                        data['shMeterReadingEvreyQnty']=body['shMeterReadingEvreyQnty']
                        data['shMeterReadingMetrics']=body['shMeterReadingMetrics']
                        data['shMeterReadingStartAt']=body['shMeterReadingStartAt']
                        data['shMeterReadingEndBy']=body['shMeterReadingEndBy']
                        data['schHasEndReading']=body['schHasEndReading']
                        data['schMeterReadingIsFixed']=True if body['schMeterReadingIsFixed']=='True' else False
                        data['shMeterNextVal']=int(body['shMeterReadingEvreyQnty'])+int(body['shMeterReadingStartAt'])
                    except Exception as e1:
                        print(e1,"line 219")
                else:
                    data['shMeterReadingWhenMetric']=body['shMeterReadingWhenMetric']
                    data['shMetricComparison']=body['shMetricComparison']
                    data['shMeterReadingWhenQnty']=body['shMeterReadingWhenQnty']

                form = ScheduleForm(data)

            else:
                data['schTriggerTime']=0
                data['schCreateOnStartDate']=False
                print("event")
                data['schAsset']=body['schAsset']
                data['schHourIsFixed']=False
                data['schDayIsFixed']=False
                data['schMonthIsFixed']=False
                data['schYearIsFixed']=False
                data["schEvent"]=body["schEvent"]
                form = ScheduleForm(data)













    else:
        print("#$#$#$#$#")
        form = ScheduleForm({'schDayIsFixed':'True','schHourIsFixed':'True','schMonthIsFixed':'True','schHowOften':'1','schChoices':'0','schTriggerTime':1,'shMeterReadingHasTiming':True})

    return save_schedule_form(request, form, 'cmms/schedule/partialScheduleCreate.html',woId)
###################################################################

@csrf_exempt
def schedule_update(request, id):
    company= get_object_or_404(Schedule, id=id)
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['schChoices']=body['schChoices']
        data['workOrder']=body['workOrder']
        print(data['workOrder'])
        woId=data['workOrder']
        if(int(data['schChoices']==0)):
            # print(body['shHasEndDate'],"##################")
            # data['shStartDate']=(body['shStartDate'])
            data['shStartDate']=DateJob.getDate2(body['shStartDate'])
            data['schTriggerTime']=(body['schTriggerTime'])
            data['schCreateOnStartDate']=(body['schCreateOnStartDate'])
            data['shHasEndDate']=True if body['shHasEndDate']==True else False
            # data['schNextWo']=body['schNextWo']
            if(data['shHasEndDate']==True):

                data['shEndDate']=DateJob.getDate2(body['shEndDate'])
            else:
                data['shEndDate']=None
            data['schHowOften']=body['schHowOften']
            if(int(data['schHowOften'])==1):
                data['shStartDate']=DateJob.getDate2(body['shStartDate'])
                data['schTriggerTime']=0
                data['schHourRep']=body['schHourRep']
                data['schHourIsFixed']=True if body['schHourIsFixed']=='True' else False
                data['schDayIsFixed']=False
                data['schMonthIsFixed']=False
                data['schMonthIsFixed']=False
                data['schMeterReadingIsFixed']=False
                data['shHasEndDate']=True if body['schHourIsFixed']=='True' else False
                form = ScheduleForm(data,instance=company)
            elif(int(data['schHowOften']==2)):
                 data['schDailyRep']=body['schDailyRep']
                 data['schDayIsFixed']=True if body['schDailyIsFixed']=='True' else False
                 #data['schDayIsFixed']=False
                 data['schMonthIsFixed']=False
                 data['schYearIsFixed']=False
                 data['schMeterReadingIsFixed']=False
                 form = ScheduleForm(data,instance=company)
            elif(int(data['schHowOften']==3)):
                 data['schHourIsFixed']=False
                 data['schDayIsFixed']=False
                 data['schMonthIsFixed']=False
                 data['schYearIsFixed']=False
                 data['schWeeklyRep']=body['schWeeklyRep']
                 data['isSaturday']=True if body['isSaturday']=='true' else False
                 data['isSunday']=True if body['isSunday']=='true' else False
                 data['isMonday']=True if body['isMonday']=='true' else False
                 data['isTuesday']=True if body['isTuesday']=='true' else False
                 data['isWednenday']=True if body['isWednenday']=='true' else False
                 data['isThursday']=True if body['isThursday']=='true' else False
                 data['isFriday']=True if body['isFriday']=='true' else False
                 print("line 324 sch ",company.schNextWo)
                 form = ScheduleForm(data,instance=company)
            elif(int(data['schHowOften']==4)):
                     data['schDayofMonthlyRep']=body['schDayofMonthlyRep']
                     data['schMonthlyRep']=body['schMonthlyRep']
                     data['schMonthIsFixed']=True if body['schMonthIsFixed']=='True' else False
                     form = ScheduleForm(data,instance=company)
            elif(int(data['schHowOften']==5)):
                     data['schHourIsFixed']=False
                     data['schDayIsFixed']=False
                     data['schMonthIsFixed']=False
                     data['schYearlyRep']=body['schYearlyRep']
                     data['schMonthOfYearRep']=body['schMonthOfYearRep']
                     data['schDayOfMonthOfYearRep']=body['schDayOfMonthOfYearRep']
                     data['schYearIsFixed']=True if body['schYearIsFixed']=='True' else False
                     form = ScheduleForm(data,instance=company)
        elif(int(data['schChoices']==1)):
                 data['schTriggerTime']=0
                 data['schCreateOnStartDate']=False
                 data['schHourIsFixed']=False
                 data['schDayIsFixed']=False
                 data['schMonthIsFixed']=False
                 data['schYearIsFixed']=False
                 data['schAsset']=body['schAsset']
                 data['shMeterReadingHasTiming']=True if body['whenreading']==0 else False
                 if(int(body['whenreading'])==0):
                     try:
                         data['shMeterReadingEvreyQnty']=body['shMeterReadingEvreyQnty']
                         data['shMeterReadingMetrics']=body['shMeterReadingMetrics']
                         data['shMeterReadingStartAt']=body['shMeterReadingStartAt']
                         data['shMeterReadingEndBy']=body['shMeterReadingEndBy']
                         data['schHasEndReading']=body['schHasEndReading']
                         data['shMeterNextVal']=int(body['shMeterReadingEvreyQnty'])+int(body['shMeterReadingStartAt'])
                         data['schMeterReadingIsFixed']=True if body['schMeterReadingIsFixed']=='True' else False
                     except Exception as e1:
                         print(e1,"line 342")
                 else:
                     data['shMeterReadingWhenMetric']=body['shMeterReadingWhenMetric']
                     data['shMetricComparison']=body['shMetricComparison']
                     data['shMeterReadingWhenQnty']=body['shMeterReadingWhenQnty']
                 # print("line 324 sch ",company.schNextWo)
                 form = ScheduleForm(data,instance=company)
        else:
            data['schTriggerTime']=0
            data['schCreateOnStartDate']=False
            print("event")
            data['schAsset']=body['schAsset']
            data['schHourIsFixed']=False
            data['schDayIsFixed']=False
            data['schMonthIsFixed']=False
            data['schYearIsFixed']=False
            data["schEvent"]=body["schEvent"]
            form = ScheduleForm(data,instance=company)
    else:
        form = ScheduleForm(instance=company)
    # print("line 338 sch ",company.schNextWo)
    return save_schedule_form(request, form, 'cmms/schedule/partialScheduleUpdate.html',company.workOrder)
