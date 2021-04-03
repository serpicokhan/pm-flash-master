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
from cmms.models.business import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import BusinessFileForm
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

###################################################################
def list_businessFile(request,id=None):
    books = BusinessFile.objects.all()
    return render(request, 'cmms/business_file/businessFileList.html', {'businessFiles': books})


###################################################################
def js_list_businessFile(request,woId):
    data=dict()
    books=BusinessFile.objects.filter(businessFileBusinessId=woId)

    data['html_businessFile_list']= render_to_string('cmms/business_file/partialBusinessFileList.html', {
        'businessFiles': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_businessFile_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = WorkorderFile.objects.filter(businessFileBusinessId=woId)
            data['html_businessFile_list'] = render_to_string('cmms/workorder_file/partialBusinessFilelist.html', {
                'businessFiles': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_businessFile_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################


def businessFile_delete(request, id):
    comp1 = get_object_or_404(WorkorderFile, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkorderFile.objects.all()
        data['html_businessFile_list'] = render_to_string('cmms/workorder_file/partialBusinessFilelist.html', {
            'businessFile': companies
        })
    else:
        context = {'businessFile': comp1}
        data['html_businessFile_form'] = render_to_string('cmms/workorder_file/partialBusinessFileDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def businessFile_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)
    logging.debug( "dasdsadasdsa")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()

        data['businessFileBusinessId']=body['businessFileBusinessId']
        data['woNotifUser']=body['woNotifUser']
        data['woNotifOnAssignment']=True if body['woNotifOnAssignment']=='true' else False
        data['woNotifOnStatusChange']=True if body['woNotifOnStatusChange']=='true' else False
        data['woNotifOnCompletion']=True if body['woNotifOnCompletion']=='true' else False
        data['woNotifOnTaskCompleted']=True if body['woNotifOnTaskCompleted']=='true' else False
        data['woNotifOnOnlineOffline']=True if body['woNotifOnOnlineOffline']=='true' else False

        woId=body['businessFileBusinessId']

        form = BusinessFileForm(data)

    else:
        form = BusinessFileForm()
    return save_businessFile_form(request, form, 'cmms/workorder_file/partialBusinessFileCreate.html',woId)
###################################################################

@csrf_exempt
def businessFile_update(request, id):
    company= get_object_or_404(WorkorderFile, id=id)
    woId=company.businessFileBusinessId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()

        data['businessFileBusinessId']=body['businessFileBusinessId']
        data['woNotifUser']=body['woNotifUser']
        data['woNotifOnAssignment']=True if body['woNotifOnAssignment']=='true' else False
        data['woNotifOnStatusChange']=True if body['woNotifOnStatusChange']=='true' else False
        data['woNotifOnCompletion']=True if body['woNotifOnCompletion']=='true' else False
        data['woNotifOnTaskCompleted']=True if body['woNotifOnTaskCompleted']=='true' else False
        data['woNotifOnOnlineOffline']=True if body['woNotifOnOnlineOffline']=='true' else False



        form = BusinessFileForm(data, instance=company)
    else:
        form = BusinessFileForm(instance=company)
    return save_businessFile_form(request, form, 'cmms/workorder_file/partialBusinessFileUpdate.html',woId)


class BusinessFileUploadView(View):
    def get(self, request):
        books = BusinessFile.objects.all()
        return render(request, 'cmms/business_file/businessFileList.html', {'businessFiles': books})

    def post(self, request,Id=None):
        from django.core.exceptions import ValidationError
        data=dict()
        fmt = getattr(settings, 'LOG_FORMAT', None)
        lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
        company= get_object_or_404(Business, id=Id)
        logging.basicConfig(format=fmt, level=lvl)
        logging.debug( request.FILES)
        valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
        ext = os.path.splitext(request.FILES['businessFile'].name)[1]
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')
        else:
            save_path = os.path.join(settings.MEDIA_ROOT,'documents', request.FILES['businessFile'].name)
            path = default_storage.save(save_path, request.FILES['businessFile'])
            document = BusinessFile.objects.create(businessFile=r'documents/'+request.FILES['businessFile'].name, businessFileBusinessId=company)
            #data = {'is_valid': True, 'name': document.businessFile.name, 'url': document.businessFile.url,'ext':ext,'size':" MB {0:.2f}".format(document.businessFile.size/1048576)}
            books = BusinessFile.objects.filter(businessFileBusinessId=Id)
            data['html_businessFile_list'] = render_to_string('cmms/business_file/partialBusinessFilelist.html', {
                  'businessFiles': books})
            data['is_valid']=True

        return JsonResponse(data)
