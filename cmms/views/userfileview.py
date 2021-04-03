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
from cmms.models.users import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import UserFileForm
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

###################################################################
def list_userFile(request,id=None):
    books = UserFile.objects.filter(userFileUser=id)
    return render(request, 'cmms/user_file/userFileList.html', {'userFiles': books,'lId':id})


###################################################################
def js_list_userFile(request,id):
    data=dict()
    books=UserFile.objects.filter(userFileUser=id)

    data['html_userFile_list']= render_to_string('cmms/user_file/partialUserFilelist.html', {
        'userFiles': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################

class UserFileUploadView(View):
    def get(self, request):
        books = UserFile.objects.all()
        return render(request, 'cmms/user_file/userFileList.html', {'userFiles': books})

    def post(self, request,Id=None):
        from django.core.exceptions import ValidationError
        data=dict()
        fmt = getattr(settings, 'LOG_FORMAT', None)
        lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
        company= get_object_or_404(SysUser, id=Id)
        logging.basicConfig(format=fmt, level=lvl)
        logging.debug( request.FILES)
        valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
        ext = os.path.splitext(request.FILES['userFile'].name)[1]
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')
        else:
            save_path = os.path.join(settings.MEDIA_ROOT,'documents', request.FILES['userFile'].name)
            path = default_storage.save(save_path, request.FILES['userFile'])
            document = UserFile.objects.create(userFile=r'documents/'+request.FILES['userFile'].name, userFileUser=company)
            #data = {'is_valid': True, 'name': document.userFile.name, 'url': document.userFile.url,'ext':ext,'size':" MB {0:.2f}".format(document.userFile.size/1048576)}
            books = UserFile.objects.filter(userFileUser=Id)
            data['html_userFile_list'] = render_to_string('cmms/user_file/partialUserFilelist.html', {
                  'userFiles': books})
            data['is_valid']=True

        return JsonResponse(data)
