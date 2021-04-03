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
import os
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
from django.views import View
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import ProjectFileForm
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

###################################################################
def list_projectFile(request,id=None):
    books = ProjectFile.objects.all()
    return render(request, 'cmms/project_file/projectFileList.html', {'projectFiles': books})


###################################################################
def js_list_projectFile(request,woId):
    data=dict()
    books=ProjectFile.objects.filter(projectFileProjectId=woId)

    data['html_projectFile_list']= render_to_string('cmms/project_file/partialProjectFilelist.html', {
        'projectFiles': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_projectFile_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = WorkorderFile.objects.filter(projectFileProjectId=woId)
            data['html_projectFile_list'] = render_to_string('cmms/workorder_file/partialProjectFilelist.html', {
                'projectFiles': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_projectFile_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################


def projectFile_delete(request, id):
    comp1 = get_object_or_404(WorkorderFile, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkorderFile.objects.all()
        data['html_projectFile_list'] = render_to_string('cmms/workorder_file/partialProjectFilelist.html', {
            'projectFile': companies
        })
    else:
        context = {'projectFile': comp1}
        data['html_projectFile_form'] = render_to_string('cmms/workorder_file/partialProjectFileDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def projectFile_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)
    logging.debug( "dasdsadasdsa")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()

        data['projectFileProjectId']=body['projectFileProjectId']
        data['woNotifUser']=body['woNotifUser']
        data['woNotifOnAssignment']=True if body['woNotifOnAssignment']=='true' else False
        data['woNotifOnStatusChange']=True if body['woNotifOnStatusChange']=='true' else False
        data['woNotifOnCompletion']=True if body['woNotifOnCompletion']=='true' else False
        data['woNotifOnTaskCompleted']=True if body['woNotifOnTaskCompleted']=='true' else False
        data['woNotifOnOnlineOffline']=True if body['woNotifOnOnlineOffline']=='true' else False

        woId=body['projectFileProjectId']

        form = ProjectFileForm(data)

    else:
        form = ProjectFileForm()
    return save_projectFile_form(request, form, 'cmms/workorder_file/partialProjectFileCreate.html',woId)
###################################################################

@csrf_exempt
def projectFile_update(request, id):
    company= get_object_or_404(WorkorderFile, id=id)
    woId=company.projectFileProjectId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()

        data['projectFileProjectId']=body['projectFileProjectId']
        data['woNotifUser']=body['woNotifUser']
        data['woNotifOnAssignment']=True if body['woNotifOnAssignment']=='true' else False
        data['woNotifOnStatusChange']=True if body['woNotifOnStatusChange']=='true' else False
        data['woNotifOnCompletion']=True if body['woNotifOnCompletion']=='true' else False
        data['woNotifOnTaskCompleted']=True if body['woNotifOnTaskCompleted']=='true' else False
        data['woNotifOnOnlineOffline']=True if body['woNotifOnOnlineOffline']=='true' else False



        form = ProjectFileForm(data, instance=company)
    else:
        form = ProjectFileForm(instance=company)
    return save_projectFile_form(request, form, 'cmms/workorder_file/partialProjectFileUpdate.html',woId)


class ProjectFileUploadView(View):
    def get(self, request):
        books = ProjectFile.objects.all()
        return render(request, 'cmms/project_file/projectFileList.html', {'projectFiles': books})

    def post(self, request,Id=None):
        from django.core.exceptions import ValidationError
        data=dict()
        fmt = getattr(settings, 'LOG_FORMAT', None)
        lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
        company= get_object_or_404(Project, id=Id)
        logging.basicConfig(format=fmt, level=lvl)
        logging.debug( request.FILES)
        valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
        ext = os.path.splitext(request.FILES['projectFile'].name)[1]
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')
        else:
            save_path = os.path.join(settings.MEDIA_ROOT,'documents', request.FILES['projectFile'].name)
            path = default_storage.save(save_path, request.FILES['projectFile'])
            document = ProjectFile.objects.create(projectFile=r'documents/'+request.FILES['projectFile'].name, projectFileProjectId=company)
            #data = {'is_valid': True, 'name': document.projectFile.name, 'url': document.projectFile.url,'ext':ext,'size':" MB {0:.2f}".format(document.projectFile.size/1048576)}
            books = ProjectFile.objects.filter(projectFileProjectId=Id)
            data['html_projectFile_list'] = render_to_string('cmms/project_file/partialProjectFilelist.html', {
                  'projectFiles': books})
            data['is_valid']=True

        return JsonResponse(data)
