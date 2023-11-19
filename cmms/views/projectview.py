'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neprojectbject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings

from cmms.models.project import *
from cmms.models.workorder import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import ProjectForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper


@permission_required('cmms.view_project')
def list_project(request,id=None):
    #
    books = Project.objects.all().order_by('-ProjectActualStartDate')
    return render(request, 'cmms/project/projectList.html', {'projects': books,'section':'list_project'})


##########################################################

def save_project_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):

        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Project.objects.all().order_by('-ProjectActualStartDate')
            data['html_project_list'] = render_to_string('cmms/project/partialProjectList.html', {
                'projects': books,
                'perms': PermWrapper(request.user)
            })
        else:
            data['form_is_valid'] = False
            print(form.errors)

    context = {'form': form,'lId':id}


    data['html_project_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def project_delete(request, id):
    comp1 = get_object_or_404(Project, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  Project.objects.all().order_by('-ProjectActualStartDate')
        #Tasks.objects.filter(projectId=id).update(project=id)
        data['html_project_list'] = render_to_string('cmms/project/partialProjectList.html', {
            'projects': companies,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'projects': comp1}
        data['html_project_form'] = render_to_string('cmms/project/partialProjectDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def project_create(request):
    if (request.method == 'POST'):
        form = ProjectForm(request.POST)
        return save_project_form(request, form, 'cmms/project/partialProjectCreate.html')
    else:
        projectInstance=Project.objects.create()
        form = ProjectForm()
        return save_project_form(request, form, 'cmms/project/partialProjectCreate.html',projectInstance.id)




##########################################################
def project_update(request, id):
    company= get_object_or_404(Project, id=id)
    template=""
    if (request.method == 'POST'):
        form = ProjectForm(request.POST, instance=company)
    else:
        form = ProjectForm(instance=company)


    return save_project_form(request, form,"cmms/project/partialProjectUpdate.html",id)
##########################################################

##########################################################
def projectSearch(request,searchStr):
    data=dict()
    searchStr=searchStr.replace('empty_','')
    searchStr=searchStr.replace('_',' ')
    books=Project.objects.filter(Q(projectName__contains=searchStr)|Q(projectDescription__contains=searchStr))
    data['html_projectLocation_list']=render_to_string('cmms/project/partialProjectList.html', {
        'projects': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)
def projectInBrief(request,id):
    data=dict()
    projectWoCount=WorkOrder.objects.filter(Project=id,isScheduling=False,isPartOf__isnull=True).count()
    projectSWoCount=WorkOrder.objects.filter(Project=id,isScheduling=True).count()
    projectHour=WorkOrder.objects.raw('select coalesce(sum(get_hour_wo(id)),0) as t1,id from workorder where project_id={0}'.format(id))[0].t1
    completedWo=WorkOrder.objects.filter(Project=id,isScheduling=False,woStatus=7).count()
    completedontime=WorkOrder.objects.raw("select coalesce(count(id),0) as id from workorder where project_id={0} and woStatus=7 and isScheduling = 0 and datecompleted<=requiredCompletionDate".format(id) )[0].id#WorkOrder.objects.filter(Project=id,isScheduling=False,woStatus=7,requiredCompletionDate__gte=self.datecompelted)
    totalCost=WorkOrder.objects.raw('''select coalesce(sum(get_workorder_part_price(id)+ get_workorder_labor_price(id)+get_workorder_misccost(id)),0) as id from workorder where project_id={0}'''.format(id))[0].id
    data['projectWoCount']=projectWoCount
    data['projectSWoCount']=projectSWoCount
    data['projectHour']=projectHour
    data['totalCost']=totalCost
    total=projectWoCount+projectSWoCount
    if(projectWoCount+projectSWoCount==0):
        data['projectWoCountoverall']=0
        data['projectWoCountontime']=0
    else:
        data['projectWoCountoverall']=completedWo*100/(projectWoCount+projectSWoCount)
        data['projectWoCountontime']=(completedontime*100/(projectWoCount+projectSWoCount))


    data['form_is_valid']=True
    return JsonResponse(data, safe=False)
def projectCancel(request,id):
    data=dict()
    tg=Project.objects.get(id=id)
    if(tg):
        if(not tg.projectName):
            tg.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            companies =  Project.objects.all().order_by('-ProjectActualStartDate')

            #Tasks.objects.filter(taskGroupId=id).update(taskGroup=id)
            data['html_project_list']=render_to_string('cmms/project/partialProjectList.html', {
                 'projects': companies
             })

    return JsonResponse(data)
