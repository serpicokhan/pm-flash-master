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
from cmms.models.parts import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PartFileForm
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

###################################################################
def list_partFile(request,id=None):
    books = PartFile.objects.all()
    return render(request, 'cmms/part_file/partFileList.html', {'partFiles': books})


###################################################################
def js_list_partFile(request,woId):
    data=dict()
    books=PartFile.objects.filter(partFilePartId=woId)

    data['html_partFile_list']= render_to_string('cmms/part_file/partialPartFileList.html', {
        'partFiles': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_partFile_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = WorkorderFile.objects.filter(partFilePartId=woId)
            data['html_partFile_list'] = render_to_string('cmms/workorder_file/partialPartFilelist.html', {
                'partFiles': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_partFile_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################


def partFile_delete(request, id):
    comp1 = get_object_or_404(WorkorderFile, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkorderFile.objects.all()
        data['html_partFile_list'] = render_to_string('cmms/workorder_file/partialPartFilelist.html', {
            'partFile': companies
        })
    else:
        context = {'partFile': comp1}
        data['html_partFile_form'] = render_to_string('cmms/workorder_file/partialPartFileDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def partFile_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)
    logging.debug( "dasdsadasdsa")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()

        data['partFilePartId']=body['partFilePartId']
        data['woNotifUser']=body['woNotifUser']
        data['woNotifOnAssignment']=True if body['woNotifOnAssignment']=='true' else False
        data['woNotifOnStatusChange']=True if body['woNotifOnStatusChange']=='true' else False
        data['woNotifOnCompletion']=True if body['woNotifOnCompletion']=='true' else False
        data['woNotifOnTaskCompleted']=True if body['woNotifOnTaskCompleted']=='true' else False
        data['woNotifOnOnlineOffline']=True if body['woNotifOnOnlineOffline']=='true' else False

        woId=body['partFilePartId']

        form = PartFileForm(data)

    else:
        form = PartFileForm()
    return save_partFile_form(request, form, 'cmms/workorder_file/partialPartFileCreate.html',woId)
###################################################################

@csrf_exempt
def partFile_update(request, id):
    company= get_object_or_404(WorkorderFile, id=id)
    woId=company.partFilePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()

        data['partFilePartId']=body['partFilePartId']
        data['woNotifUser']=body['woNotifUser']
        data['woNotifOnAssignment']=True if body['woNotifOnAssignment']=='true' else False
        data['woNotifOnStatusChange']=True if body['woNotifOnStatusChange']=='true' else False
        data['woNotifOnCompletion']=True if body['woNotifOnCompletion']=='true' else False
        data['woNotifOnTaskCompleted']=True if body['woNotifOnTaskCompleted']=='true' else False
        data['woNotifOnOnlineOffline']=True if body['woNotifOnOnlineOffline']=='true' else False



        form = PartFileForm(data, instance=company)
    else:
        form = PartFileForm(instance=company)
    return save_partFile_form(request, form, 'cmms/workorder_file/partialPartFileUpdate.html',woId)


class PartFileUploadView(View):
    def get(self, request):
        books = PartFile.objects.all()
        return render(request, 'cmms/part_file/partFileList.html', {'partFiles': books})

    def post(self, request,Id=None):
        from django.core.exceptions import ValidationError
        data=dict()
        fmt = getattr(settings, 'LOG_FORMAT', None)
        lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
        company= get_object_or_404(Part, id=Id)
        logging.basicConfig(format=fmt, level=lvl)
        logging.debug( request.FILES)
        valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
        ext = os.path.splitext(request.FILES['partFile'].name)[1]
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')
        else:
            save_path = os.path.join(settings.MEDIA_ROOT,'documents', request.FILES['partFile'].name)
            path = default_storage.save(save_path, request.FILES['partFile'])
            document = PartFile.objects.create(partFile=r'documents/'+request.FILES['partFile'].name, partFilePartId=company)
            #data = {'is_valid': True, 'name': document.partFile.name, 'url': document.partFile.url,'ext':ext,'size':" MB {0:.2f}".format(document.partFile.size/1048576)}
            books = PartFile.objects.filter(partFilePartId=Id)
            data['html_partFile_list'] = render_to_string('cmms/part_file/partialPartFilelist.html', {
                  'partFiles': books})
            data['is_valid']=True

        return JsonResponse(data)
