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
from cmms.models.Asset import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetFileForm
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response

###################################################################
def list_assetFile(request,id=None):
    books = AssetFile.objects.all()
    return render(request, 'cmms/asset_file/assetFileList.html', {'assetFiles': books})


###################################################################
def js_list_assetFile(request,woId):
    data=dict()
    books=AssetFile.objects.filter(assetFileAssetId=woId)

    data['html_assetFile_list']= render_to_string('cmms/asset_file/partialAssetFileList.html', {
        'assetFiles': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)




class AssetFileUploadView(View):
    def get(self, request,Id):
        try:
        # books = AssetFile.objects.all()
            return render(request, 'cmms/asset_file/assetFileList.html', {'assetFiles': 1})
        except:
            return render(request, 'cmms/asset_file/assetFileList.html', {'assetFiles': 1})


    def post(self, request,Id=None):
        from django.core.exceptions import ValidationError
        data=dict()
        fmt = getattr(settings, 'LOG_FORMAT', None)
        lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
        company= get_object_or_404(Asset, id=Id)
        logging.basicConfig(format=fmt, level=lvl)
        logging.debug( request.FILES)
        valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls','.gif']
        ext = os.path.splitext(request.FILES['assetFile'].name)[1]
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')
        else:
            save_path = os.path.join(settings.MEDIA_ROOT,'documents', request.FILES['assetFile'].name)
            path = default_storage.save(save_path, request.FILES['assetFile'])
            document = AssetFile.objects.create(assetFile=r'documents/'+request.FILES['assetFile'].name, assetFileAssetId=company)
            #data = {'is_valid': True, 'name': document.assetFile.name, 'url': document.assetFile.url,'ext':ext,'size':" MB {0:.2f}".format(document.assetFile.size/1048576)}
            books = AssetFile.objects.filter(assetFileAssetId=Id)
            data['html_assetFile_list'] = render_to_string('cmms/asset_file/partialAssetFilelist.html', {
                  'assetFiles': books})
            data['is_valid']=True

        return JsonResponse(data)
@api_view(['GET'])
def assetfile_collection(request,id):
    if request.method == 'GET':
        posts = AssetFile.objects.filter(assetFileAssetId=id)
        serializer = AssetFileSerializer(posts, many=True)

        return Response(serializer.data)
@api_view(['GET'])
def assetfile_detail_collection(request,id):
    if request.method == 'GET':
        posts = AssetFile.objects.get(id=id)
        serializer = AssetFileSerializer(posts)

        return Response(serializer.data)
