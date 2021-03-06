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
from django.db.models import Sum
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from cmms.models.task import *
from cmms.models.workorder import *
from cmms.models.Asset import *
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator
from datetime import timedelta
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import TaskForm,TaskForm2
from cmms.business.DateJob import DateJob
from cmms.business.taskUtility import TaskUtility
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
###################################################################
def list_task(request,id=None):
    books = Tasks.objects.all()
    return render(request, 'cmms/tasks/taskList.html', {'task': books})


###################################################################
@permission_required('cmms.view_tasks')
def js_list_task(request,woId):
    data=dict()
    ####
    books = Tasks.objects.filter(workOrder=woId)
    wo_Id=WorkOrder.objects.get(id=woId)
    if(books.count()>0):
        data["is_not_empty"]=True
    else:
        data["is_not_empty"]=False

    if(wo_Id.isScheduling==True):
        # print("here")
        data['html_task_list']= render_to_string('cmms/tasks/partialTaskList.html', {
            'task': books,
            'perms': PermWrapper(request.user),
            'ispm':True
        })
    else:
        data['html_task_list']= render_to_string('cmms/tasks/partialTaskList.html', {
            'task': books,
            'perms': PermWrapper(request.user),
            'ispm':False
        })
    data["form_is_valid"]=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_task_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():

            err_code=0
            err_msg=""

            if(err_code==0):

                newTask=form.save()
                # data['wo_time']=TaskUtility.check_completion_date(newTask.workOrder)
                # print(data['wo_time'],"!!!!!!!!!!!!")

                task_create_meter_reading(newTask.id)
                data['form_is_valid'] = True
                data['id']=newTask.id
                wo=WorkOrder.objects.get(id=woId)
                #only for none pm workorder
                tasks = Tasks.objects.filter(workOrder=woId).order_by('-taskDateCompleted','-taskTimeCompleted')
                # print(tasks.count(),"couunt")
                try:
                    if(tasks.count()==1):

                        data['last_task_workinstraction']=newTask.taskDescription
                        data['last_task_assignedUser']=newTask.taskAssignedToUser.id
                        data['last_task_completedUser']=newTask.taskCompletedByUser.id
                    # if(wo.isPm==False):
                    #         data['last_task_date']=str(jdatetime.date.fromgregorian(date=tasks[0].taskDateCompleted))
                    #         data['last_task_time']=tasks[0].taskTimeCompleted
                except Exception as ex:
                    print(ex)
                books = Tasks.objects.filter(workOrder=woId)
                #books = Tasks.objects.all()
                #######
                if(wo.isScheduling==False):
                    data['html_task_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
                        'task': books,
                        'perms': PermWrapper(request.user),
                        'ispm':False
                    })
                else:
                        data['html_task_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
                            'task': books,
                            'perms': PermWrapper(request.user),
                            'ispm':True
                        })


            else:
                data['form_is_valid'] = False
                data['form_err_code'] = err_code
                data['form_err_msg'] = err_msg
                print(err_msg)
          else:
             data['form_is_valid'] = False
             print(form.errors)


    context = {'form': form}
    data['html_task_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def task_delete(request, id):
    try:
        comp1 = get_object_or_404(Tasks, id=id)
        woId=comp1.workOrder
        data = dict()
        print(request.method)

        if (request.method == 'POST'):
            comp1.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            #companies = WorkorderTask.objects.filter(workorder=woId)
            companies = Tasks.objects.filter(workOrder=woId)
            wo_Id=WorkOrder.objects.get(id=woId.id)
            if(wo_Id.isScheduling==False):
                data['html_task_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
                    'task': companies,
                    'perms': PermWrapper(request.user),
                    'ispm':False
                })
            else:
                data['html_task_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
                    'task': companies,
                    'perms': PermWrapper(request.user),
                    'ispm':True
                })

        else:
            context = {'task': comp1}
            data['html_task_form'] = render_to_string('cmms/tasks/partialTaskDelete.html',
                context,
                request=request,
            )
        return JsonResponse(data)
    except:
        data = dict()
        data['form_is_valid'] = True
        if (request.method == 'POST'):
            data['form_is_valid'] = True  # This is just to play along with the existing code
            # query="select id as id,assetPartAssetid_id,sum(assetPartQnty) as assetPartQnty from assetpart where  assetPartAssetid_id={} group by assetPartAssetid_id,AssetPartPid_id".format(woId)

            companies = Tasks.objects.filter(workOrder=woId)
            wo_Id=WorkOrder.objects.get(id=woId)
            if(wo_Id.isScheduling==False):
                data['html_task_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
                    'task': companies,
                    'perms': PermWrapper(request.user),
                    'ispm':False
                })
            else:
                data['html_task_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
                    'task': companies,
                    'perms': PermWrapper(request.user),
                    'ispm':True
                })


        return JsonResponse(data)
###################################################################
@csrf_exempt
def task_create(request):
    woId=-1
    ww=request.GET.get("q","!!!!")
    try:
        if (request.method == 'POST'):
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            # print(body)
            content = body['taskTypes']
            data = request.POST.dict()

            data['taskTypes']=body['taskTypes']
            data['taskDescription']=body['taskDescription']
            data['taskAssignedToUser']=body['taskAssignedToUser']
            data['taskMetrics']=body['taskMetrics']
            data['taskStartDate']=DateJob.getTaskDate(body['taskStartDate'])
            data['taskTimeEstimate']=body['taskTimeEstimate']
            data['taskCompletedByUser']=body['taskCompletedByUser']
            data['taskTimeSpent']=body['taskTimeSpent']
            data['taskDateCompleted']=DateJob.getTaskDate(body['taskDateCompleted'])
            data['taskCompletionNote']=body['taskCompletionNote']
            data['taskStartTime']=body['taskStartTime']
            data['taskTimeCompleted']=body['taskTimeCompleted']
            data['taskResult']=body['taskResult']
            data['task_inspection']=body['task_inspection']
            ####
            data['workOrder']=body['workOrder']
            woId=body['workOrder']
            form = TaskForm(int(woId),data)

        else:
            # if(woid):
            #     wo=WorkOrder.objects.get(id=woid)
            #     form = TaskForm(initial={'taskDescription':wo.summaryofIssue,'taskCompletedByUser':wo.completedByUser,'taskAssignedToUser':wo.assignedToUser})
            form = TaskForm(workorder=int(ww))
    except Exception as ex:
        print(ex)
    # form=TaskForm()
    return save_task_form(request, form, 'cmms/tasks/partialTaskCreate.html',woId)
@csrf_exempt
def task_create2(request):
    woId=-1
    ww=request.GET.get("q","2121221")

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['taskTypes']
        data = request.POST.dict()
        data['taskTypes']=body['taskTypes']
        data['taskDescription']=body['taskDescription']
        data['taskAssignedToUser']=body['taskAssignedToUser']
        data['taskMetrics']=body['taskMetrics']
        data['taskTimeEstimate']=body['taskTimeEstimate']
        data['workOrder']=body['workOrder']
        woId=body['workOrder']
        form = TaskForm2(int(woId),data)

    else:
        form = TaskForm2(workorder=int(ww))
    return save_task_form(request, form, 'cmms/tasks/partialTaskCreate2.html',woId)
###################################################################

@csrf_exempt
def task_update(request, id):

    #company= get_object_or_404(Tasks, id=id)
    company=get_object_or_404(Tasks, id=id)

    woId=-1
    print("common")
    print(woId)
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        content = body['taskTypes']
        data = request.POST.dict()
        data['taskTypes']=body['taskTypes']
        data['taskDescription']=body['taskDescription']
        data['taskAssignedToUser']=body['taskAssignedToUser']
        data['taskMetrics']=body['taskMetrics']
        data['taskStartDate']=DateJob.getTaskDate(body['taskStartDate'])
        data['taskTimeEstimate']=body['taskTimeEstimate']
        data['taskCompletedByUser']=body['taskCompletedByUser']
        data['taskTimeSpent']=body['taskTimeSpent']
        data['taskDateCompleted']=DateJob.getTaskDate(body['taskDateCompleted'])
        # print("$$$$$$$$$$$$$$$$$$$$$",body['taskDateCompleted'])
        data['taskCompletionNote']=body['taskCompletionNote']
        data['taskStartTime']=body['taskStartTime']
        data['taskTimeCompleted']=body['taskTimeCompleted']
        data['workOrder']=body['workOrder']
        data['taskResult']=body['taskResult']
        data['task_inspection']=body['task_inspection']
        # print("taskResult",data['taskResult'])

        woId=body['workOrder']
        form = TaskForm(int(woId),data, instance=company)
    else:
        ww=request.GET.get("q","1")
        form = TaskForm(instance=company,workorder=int(ww))
    return save_task_form(request, form, 'cmms/tasks/partialTaskUpdate.html',woId)
@csrf_exempt
def task_update2(request, id):

    #company= get_object_or_404(Tasks, id=id)
    company=get_object_or_404(Tasks, id=id)

    woId=-1
    print("this is a")
    print(woId)
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['taskTypes']
        data = request.POST.dict()
        data['taskTypes']=body['taskTypes']
        data['taskDescription']=body['taskDescription']
        data['taskAssignedToUser']=body['taskAssignedToUser']
        data['taskMetrics']=body['taskMetrics']
        data['taskTimeEstimate']=body['taskTimeEstimate']
        data['workOrder']=body['workOrder']
        woId=body['workOrder']
        form = TaskForm2(int(woId),data, instance=company)
    else:
        ww=request.GET.get("q","1")
        form = TaskForm2(instance=company,workorder=int(ww))
    return save_task_form(request, form, 'cmms/tasks/partialTaskUpdate2.html',woId)


def set_task_result(request,id):
    task=Tasks.objects.get(id=id)
    task.taskResult=float(request.GET.get('q','0'))
    dt_start=datetime.datetime.combine(task.taskStartDate,task.taskStartTime)
    dt_end=dt_start+timedelta(hours=task.taskTimeEstimate)
    task.taskDateCompleted=dt_end.date()
    task.taskTimeCompleted=dt_end.time()

    task.save()
    data=dict()
    data['form_is_valid']=True
    data["result"]=task.taskResult
    data["time"]=task.get_total_work_time()
    task_create_meter_reading(task.id)
    return JsonResponse(data)
def task_create_meter_reading(t):
    task=Tasks.objects.get(id=t)
    wo=task.workOrder
    wo_Asset=wo.woAsset
    asset_meter=AssetMeterReading.objects.filter(assetWorkorderMeterReading=wo,assetMeterMeterReadingUnit=task.taskMetrics)
    if(task.taskResult):
        if(asset_meter.count()>0):
            asset_meter1=asset_meter[0]
            asset_meter1.assetMeterMeterReading=task.taskResult
            asset_meter1.save()
        else:
            AssetMeterReading.objects.create(assetWorkorderMeterReading=wo,assetMeterMeterReadingUnit=task.taskMetrics,assetMeterLocation=wo_Asset,assetMeterMeterReading=task.taskResult)

    else:
        if(asset_meter.count()>0):
            asset_meter1=asset_meter[0]
            asset_meter1.delete()



def getTotalUserActivityEstimatedTimeBySWO(request,wo,uid):
    swo=Schedule.objects.get(workOrder=wo)
    time_=swo.schnextTime

    total_time=TaskUtility.GetTotalEstimatedUserTime(uid,time_)
    data=dict()
    data["form_is_valid"]=True
    data["result"]=total_time
    return JsonResponse(data)

def get_auto_completion_time(request,id):
    task=Tasks.objects.get(id=id)
    dt_start=datetime.datetime.combine(task.taskStartDate,task.taskStartTime)
    dt_end=dt_start+timedelta(hours=task.taskTimeEstimate)
    data=dict()
    data["date"]=str(jdatetime.date.fromgregorian(date=dt_end.date()))
    data["time"]=dt_end.time()

    data["form_is_valid"]=True
    return JsonResponse(data)
def set_All_task_completion_date(request,id):
    data=dict()
    tasks=Tasks.objects.filter(workOrder__id=id)
    try:
        for x in tasks:


            dt_start=datetime.datetime.combine(x.taskStartDate,x.taskStartTime)
            dt_end=dt_start+timedelta(hours=x.taskTimeEstimate)
            x.taskDateCompleted=dt_end.date()
            x.taskTimeCompleted=dt_end.time()
            x.save()
        data["form_is_valid"]=True
    except:
        data["error"]="?????????? ???? ????????"
        data["form_is_valid"]=False

    wo_Id=WorkOrder.objects.get(id=id)
    if(wo_Id.isScheduling==False):
        data['html_task_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
            'task': tasks,
            'perms': PermWrapper(request.user),
            'ispm':False
        })
    else:
        data['html_task_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
            'task': companies,
            'perms': PermWrapper(request.user),
            'ispm':True
        })



    # data["date"]=str(jdatetime.date.fromgregorian(date=dt_end.date()))
    # data["time"]=dt_end.time()


    return JsonResponse(data)


def getTaskTypeSelector(request):

    ww=request.GET.get("q",1)
    task_type=request.GET.get("t",1)
    task_id=request.GET.get("id","0")
    data=dict()
    form=None
    if(int(task_id)>0):
        form=TaskForm(instance=Tasks.objects.get(id=task_id),workorder=int(ww))
    else:
        form=TaskForm(workorder=int(ww))

    data['html']=render_to_string('cmms/tasks/tasktypeselector.html', {
        'form':form,
        'c':task_type,
    })
    return JsonResponse(data)
def getTaskWoHour(request,startHijri,endHijri,t1,t2):
    start1,end1=DateJob.convert2Date(startHijri,endHijri)
    start=DateJob.combine(start1,t1)
    end=DateJob.combine(end1,t2)
    data=dict()
    data['task_hour_result']=TaskUtility.getTaskHour(start,end)
    return JsonResponse(data)
@api_view(['GET'])
def task_collection(request,id):
    if request.method == 'GET':
        print("reached task")
        posts = Tasks.objects.filter(workOrder=id)
        serializer = TaskSerializer(posts, many=True)

        return Response(serializer.data)
@api_view(['GET'])
def task_detail_collection(request,id):
    if request.method == 'GET':
        # print("!23")
        posts = Tasks.objects.get(id=id)
        serializer = TaskSerializer(posts)

        return Response(serializer.data)
