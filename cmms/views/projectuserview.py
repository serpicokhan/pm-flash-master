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

import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings

from cmms.models.project import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import ProjectUserForm

###################################################################
def list_projectUser(request,id=None):
    books = ProjectUser.objects.all()
    return render(request, 'cmms/project_user/projectUserList.html', {'projectUsers': books})


###################################################################
def js_list_projectUser(request,woId):
    data=dict()
    books=ProjectUser.objects.filter(ProjectUserId=woId)

    data['html_projectUser_list']= render_to_string('cmms/project_user/partialProjectUserList.html', {
        'projectUsers': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_projectUser_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = ProjectUser.objects.filter(ProjectUserId=woId)
            data['html_projectUser_list'] = render_to_string('cmms/project_user/partialProjectUserList.html', {
                'projectUsers': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_projectUser_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def projectUser_delete(request, id):
    comp1 = get_object_or_404(ProjectUser, id=id)
    data = dict()
    projid=comp1.ProjectUserId

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = ProjectUser.objects.filter(ProjectUserId=projid)
        data['html_projectUser_list'] = render_to_string('cmms/project_user/partialProjectUserList.html', {
            'projectUsers': companies
        })
    else:
        context = {'projectUser': comp1}
        data['html_projectUser_form'] = render_to_string('cmms/project_user/partialProjectUserDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def projectUser_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['ProjectUserId']=body['ProjectUserId']
        data['ProjectUserUserId']=body['ProjectUserUserId']


        woId=body['ProjectUserId']

        form = ProjectUserForm(data)

    else:
        form = ProjectUserForm()
    return save_projectUser_form(request, form, 'cmms/project_user/partialProjectUserCreate.html',woId)
###################################################################

@csrf_exempt
def projectUser_update(request, id):
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)

    company= get_object_or_404(ProjectUser, id=id)
    woId=company.ProjectUserId
    logging.debug(woId)
    print(woId)
    print("update")
    if (request.method == 'POST'):
        print("update")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['ProjectUserId']=body['ProjectUserId']
        data['ProjectUserUserId']=body['ProjectUserUserId']



        form = ProjectUserForm(data, instance=company)
    else:
        form = ProjectUserForm(instance=company)
    return save_projectUser_form(request, form, 'cmms/project_user/partialProjectUserUpdate.html',woId)
