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
from cmms.models.workorder import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import WoFileForm
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response

###################################################################
def list_woFile(request,id=None):
    books = WorkorderFile.objects.all()
    return render(request, 'cmms/workorder_file/woFileList.html', {'woFiles': books})


###################################################################
@permission_required('cmms.view_workorderfile')
def js_list_woFile(request,woId):
    data=dict()
    books=WorkorderFile.objects.filter(woFileworkorder=woId)

    data['html_woFile_list']= render_to_string('cmms/workorder_file/partialWoFileList.html', {
        'woFiles': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################

class WorkOrderUploadView(View):
    def get(self, request):
        books = WorkorderFile.objects.all()
        return render(request, 'cmms/workorder_file/woFileList.html', {'woFiles': books})

    def post(self, request,Id=None):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        from django.core.exceptions import ValidationError
        data=dict()
        # fmt = getattr(settings, 'LOG_FORMAT', None)
        # lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
        company= get_object_or_404(WorkOrder, id=Id)
        # logging.basicConfig(format=fmt, level=lvl)
        # logging.debug( request.FILES)
        valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls','.gif','.aac']
        ext = os.path.splitext(request.FILES['woFile'].name)[1]
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')
        else:
            save_path = os.path.join(settings.MEDIA_ROOT,'documents', request.FILES['woFile'].name)
            path = default_storage.save(save_path, request.FILES['woFile'])
            document = WorkorderFile.objects.create(woFile='documents/'+request.FILES['woFile'].name, woFileworkorder=company)
            #data = {'is_valid': True, 'name': document.woFile.name, 'url': document.woFile.url,'ext':ext,'size':" MB {0:.2f}".format(document.woFile.size/1048576)}
            books = WorkorderFile.objects.filter(woFileworkorder=Id)
            data['html_woFile_list'] = render_to_string('cmms/workorder_file/partialWoFileList.html', {
                  'woFiles': books})
            data['is_valid']=True

        return JsonResponse(data)






@api_view(['GET'])
def wofile_collection(request,id):
    if request.method == 'GET':
        print("reached task")
        posts = WorkorderFile.objects.filter(woFileworkorder=id)
        serializer = WorkorderFileSerializer(posts, many=True)

        return Response(serializer.data)
@api_view(['GET'])
def wofile_detail_collection(request,id):
    if request.method == 'GET':
        # print("!23")
        posts = WorkorderFile.objects.get(id=id)
        serializer = WorkorderFileSerializer(posts)

        return Response(serializer.data)

@api_view(['POST'])
def woFile_post(request,Id=None):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        from django.core.exceptions import ValidationError
        data=dict()
        print(request.FILES['woFile'],'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        # fmt = getattr(settings, 'LOG_FORMAT', None)
        # lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
        company= get_object_or_404(WorkOrder, id=Id)
        # logging.basicConfig(format=fmt, level=lvl)

        # valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls','.gif']
        # ext = os.path.splitext(request.FILES['woFile'].name)[1]
        # if not ext.lower() in valid_extensions:
        #     raise ValidationError(u'Unsupported file extension.')
        # else:
        save_path = os.path.join(settings.MEDIA_ROOT,'documents', request.FILES['woFile'].name)
        path = default_storage.save(save_path, request.FILES['woFile'])
        document = WorkorderFile.objects.create(woFile='documents/'+request.FILES['woFile'].name, woFileworkorder=company)
        #data = {'is_valid': True, 'name': document.woFile.name, 'url': document.woFile.url,'ext':ext,'size':" MB {0:.2f}".format(document.woFile.size/1048576)}
        books = WorkorderFile.objects.filter(woFileworkorder=Id)
        data['html_woFile_list'] = render_to_string('cmms/workorder_file/partialWoFileList.html', {
              'woFiles': books})
        data['is_valid']=True

        print("Ok!!!!!!!!!!!!!!")

        return JsonResponse(data)
