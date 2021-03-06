''' = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(netaskGroupbject.OrderId.id)
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
from cmms.models.Asset import *

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import TaskGroupForm
from django.urls import reverse_lazy
from django.db import transaction
from cmms.business.taskUtility import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from cmms.business.taskUtility import TaskUtility

@permission_required('cmms.view_taskgroup')
def list_taskGroup(request,id=None):
    #
    books = TaskGroup.objects.all().order_by('-id')
    wos=TaskUtility.doPaging(request,books)
    return render(request, 'cmms/taskgroup/taskGroupList.html', {'taskGroup': wos,'section':'list_taskGroup'})


##########################################################
def list_taskGroup_js(request,assetId=None):
    # print("here1212")
    data=dict()
    assetCat=0
    books=0
    assetCat=Asset.objects.get(id=assetId)
    books=TaskGroup.objects.filter(id__in=TaskGroupAssetCategory.objects.
                                   filter(assetCategory=assetCat.assetCategory).values_list('TaskGroup',flat=True))
    if(len(books)>0):
        pass
    else:
        books=TaskGroup.objects.all().order_by('-id')

    bookp=TaskUtility.doPaging(request,books)






    ####


    data['html_taskGroup_list']= render_to_string('cmms/taskgroup/partialTaskGroupList2.html', {
        'taskGroup': bookp
    })

    return JsonResponse(data)

def save_taskGroup_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = TaskGroup.objects.all().order_by('-id')
            wos=TaskUtility.doPaging(request,books)
            data['html_taskGroup_list'] = render_to_string('cmms/taskgroup/partialTaskGroupList.html', {
                'taskGroup': wos,
                'perms': PermWrapper(request.user)
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form,'lId':id}


    data['html_taskGroup_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def taskGroup_delete(request, id):
    comp1 = get_object_or_404(TaskGroup, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  TaskGroup.objects.all().order_by('-id')
        wos=TaskUtility.doPaging(request,companies)
        #Tasks.objects.filter(taskGroupId=id).update(taskGroup=id)
        data['html_taskGroup_list'] = render_to_string('cmms/taskgroup/partialTaskGroupList.html', {
            'taskGroup': wos,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'taskGroup': comp1,'perms': PermWrapper(request.user)}
        data['html_taskGroup_form'] = render_to_string('cmms/taskgroup/partialTaskGroupDelete.html',
            context,
            request=request,

        )
    return JsonResponse(data)

##########################################################

##########################################################
def taskGroup_create(request):
    if (request.method == 'POST'):
        form = TaskGroupForm(request.POST)
        return save_taskGroup_form(request, form, 'cmms/taskgroup/partialTaskGroupCreate.html')
    else:
        taskGroupInstance=TaskGroup.objects.create()
        print("somthing")
        form = TaskGroupForm(instance=taskGroupInstance)
        return save_taskGroup_form(request, form, 'cmms/taskgroup/partialTaskGroupCreate.html',taskGroupInstance.id)




##########################################################
def taskGroup_update(request, id):
    company= get_object_or_404(TaskGroup, id=id)
    template=""
    if (request.method == 'POST'):
        form = TaskGroupForm(request.POST, instance=company)
    else:
        form = TaskGroupForm(instance=company)
    # fmt = getattr(settings, 'LOG_FORMAT', None)
    # lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    #
    # logging.basicConfig(format=fmt, level=lvl)
    # logging.debug(id)

    return save_taskGroup_form(request, form,"cmms/taskgroup/partialTaskGroupUpdate.html",id)
##########################################################

##########################################################
def registerTaskGroup(request,tid,woid):
    print("triggerd")
    data=dict()
    TaskUtility.register(tid,woid)
    books = Tasks.objects.filter(workOrder=woid)
    wos_=WorkOrder.objects.get(id=woid)
    if(wos_.isScheduling):
        data['html_taskgroup_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
            'task': books,
            'perms': PermWrapper(request.user),
            'ispm':True

        })
    else:
        data['html_taskgroup_list'] = render_to_string('cmms/tasks/partialTaskList.html', {
            'task': books,
            'perms': PermWrapper(request.user),
            'ispm':False

        })
    return JsonResponse(data)

# ***********************
@csrf_exempt
def taskGroupCancel(request,id):
    data=dict()
    if(request.method=='POST'):

        tg=TaskGroup.objects.get(id=id)
        if(tg):

                tg.delete()
                data['form_is_valid'] = True  # This is just to play along with the existing code
                companies =  TaskGroup.objects.all().order_by('taskGroupName')
                wos=TaskUtility.doPaging(request,companies)
                #Tasks.objects.filter(taskGroupId=id).update(taskGroup=id)
                data['html_taskGroup_list'] = render_to_string('cmms/taskgroup/partialTaskGroupList.html', {
                    'taskGroup': wos
                })
        else:
            data['form_is_valid'] = True
            print("else")

    return JsonResponse(data)
# ***********************
@csrf_exempt
def task_check_task_num(request,id):
    data=dict()

    tg=TaskTemplate.objects.filter(taskTemplateTaskGroup=id)
    data['form_is_valid']=True
    data['result']=tg.count()




    return JsonResponse(data)
def taskGroupSearch(request,str):

    data=dict()
    str=str.replace('_',' ')
    str=str.replace('empty','')
    wos=[]
    if(str):
        wos= TaskGroup.objects.filter(taskGroupName__contains=str).order_by('-id')
    else:
        wos=TaskGroup.objects.all().order_by('-id')

    data["form_is_valid"]=True
    data['html_taskGroup_list']=render_to_string('cmms/taskgroup/partialTaskGroupListSearch.html', {
        'taskGroup': wos,
        'perms': PermWrapper(request.user)

    })
    return JsonResponse(data)
