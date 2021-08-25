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
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import TaskTemplateForm
from cmms.business.DateJob import DateJob

###################################################################
def list_taskTemplate(request,id=None):
    books = TaskTemplate.objects.all()
    return render(request, 'cmms/tasktemplate/taskTemplateList.html', {'taskTemplate': books})


###################################################################
def js_list_taskTemplate(request,woId):
    data=dict()


    ####
    books = TaskTemplate.objects.filter(taskTemplateTaskGroup=woId)
    data['html_taskTemplate_list']= render_to_string('cmms/tasktemplate/partialtaskTemplatelist.html', {
        'taskTemplate': books
    })
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_taskTemplate_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():

            # err_code=0



            newTaskTemplate=form.save()
            data['form_is_valid'] = True
            books = TaskTemplate.objects.filter(taskTemplateTaskGroup=woId)
            #books = TaskTemplate.objects.all()
            #######
            data['html_taskTemplate_list'] = render_to_string('cmms/tasktemplate/partialTaskTemplatelist.html', {
                'taskTemplate': books
            })

          else:
             print(form.errors)
    context = {'form': form}
    data['html_taskTemplate_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def taskTemplate_delete(request, id):
    comp1 = get_object_or_404(TaskTemplate, id=id)
    woId=comp1.taskTemplateTaskGroup
    data = dict()
    print(request.method)

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        #companies = WorkorderTaskTemplate.objects.filter(workorder=woId)
        companies = TaskTemplate.objects.filter(taskTemplateTaskGroup=woId)
        data['html_taskTemplate_list'] = render_to_string('cmms/tasktemplate/partialTaskTemplatelist.html', {
            'taskTemplate': companies
        })
    else:
        context = {'taskTemplate': comp1}
        data['html_taskTemplate_form'] = render_to_string('cmms/tasktemplate/partialTaskTemplateDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def taskTemplate_create(request):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['taskTemplateTypes']
        data = request.POST.dict()

        data['taskTemplateTypes']=body['taskTemplateTypes']
        data['taskTemplateDescription']=body['taskTemplateDescription']
        # data['taskTemplateAssignedToUser']=body['taskTemplateAssignedToUser']
        data['taskTemplateMetrics']=body['taskTemplateMetrics']
        # data['taskTemplateStartDate']=body['taskTemplateStartDate']
        data['taskTemplateTimeEstimate']=body['taskTemplateTimeEstimate']

        ####
        data['taskTemplateTaskGroup']=body['taskTemplateTaskGroup']
        woId=body['taskTemplateTaskGroup']
        form = TaskTemplateForm(data)

    else:
        form = TaskTemplateForm()
    return save_taskTemplate_form(request, form, 'cmms/tasktemplate/partialTaskTemplateCreate.html',woId)
###################################################################

@csrf_exempt
def taskTemplate_update(request, id):

    #company= get_object_or_404(Tasktemplate, id=id)
    company=get_object_or_404(TaskTemplate, id=id)

    woId=company.taskTemplateTaskGroup
    print(woId)
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['taskTemplateTypes']
        data = request.POST.dict()
        data['taskTemplateTypes']=body['taskTemplateTypes']
        data['taskTemplateDescription']=body['taskTemplateDescription']
        # data['taskTemplateAssignedToUser']=body['taskTemplateAssignedToUser']
        data['taskTemplateMetrics']=body['taskTemplateMetrics']
        # data['taskTemplateStartDate']=body['taskTemplateStartDate']
        data['taskTemplateTimeEstimate']=body['taskTemplateTimeEstimate']
    
        data['taskTemplateTaskGroup']=body['taskTemplateTaskGroup']

        woId=body['taskTemplateTaskGroup']
        form = TaskTemplateForm(data, instance=company)
    else:
        form = TaskTemplateForm(instance=company)
    return save_taskTemplate_form(request, form, 'cmms/tasktemplate/partialTaskTemplateUpdate.html',woId)
