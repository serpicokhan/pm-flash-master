'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(netaskGroupFilebject.OrderId.id)
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
from cmms.models.task import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import TaskGroupFileForm
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

###################################################################
def list_taskGroupFile(request,id=None):
    books = TaskGroupFileFile.objects.all()
    return render(request, 'cmms/taskgroup_file/taskGroupFileList.html', {'taskGroupFiles': books})


###################################################################
def js_list_taskGroupFile(request,taskGroupFileId):
    data=dict()
    books=TaskGroupFile.objects.filter(taskGroupFileTaskGroup=taskGroupFileId)

    data['html_taskGroupFile_list']= render_to_string('cmms/taskgroup_file/partialTaskGroupFilelist.html', {
        'taskGroupFiles': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)




class TaskGroupBasicUploadView(View):
    def get(self, request):
        books = TaskGroupFile.objects.all()
        return render(request, 'cmms/taskgroup_file/taskGroupFileList.html', {'taskGroupFiles': books})

    def post(self, request,Id=None):
        from django.core.exceptions import ValidationError
        data=dict()

        valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
        ext = os.path.splitext(request.FILES['taskGroupFile'].name)[1]
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')
        else:
            save_path = os.path.join(settings.MEDIA_ROOT,'documents', request.FILES['taskGroupFile'].name)
            path = default_storage.save(save_path, request.FILES['taskGroupFile'])
            document = TaskGroupFile.objects.create(taskGroupFile='documents/'+request.FILES['taskGroupFile'].name, taskGroupFileTaskGroup=Id)
            #data = {'is_valid': True, 'name': document.taskGroupFile.name, 'url': document.taskGroupFile.url,'ext':ext,'size':" MB {0:.2f}".format(document.taskGroupFile.size/1048576)}
            books = TaskGroupFile.objects.filter(taskGroupFileTaskGroup=Id)
            data['html_taskGroupFile_list'] = render_to_string('cmms/taskgroup_file/partialTaskGroupFilelist.html', {
                  'taskGroupFiles': books})
            data['is_valid']=True

        return JsonResponse(data)
