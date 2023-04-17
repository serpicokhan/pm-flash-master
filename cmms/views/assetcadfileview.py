'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neassetCadFilebject.OrderId.id)
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

from cmms.models.workorder import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetCadFileForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
from rest_framework import status

@permission_required('cmms.view_assetcadfile')
def list_assetCadFile(request,id=None):
    #
    books = AssetCadFile.objects.all()
    return render(request, 'cmms/assetcadfile/assetCadFileList.html', {'assetCadFile': books,'section':'list_assetCadFile'})


##########################################################

def save_assetCadFile_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):

        if form.is_valid():            
            form.save()
        else:
            print(form.errors)
        books = AssetCadFile.objects.all()
        data['html_assetCadFile_list'] = render_to_string('cmms/assetcadfile/partialAssetCadFileList.html', {
                'assetCadFile': books,
                'perms': PermWrapper(request.user)
            })



    context = {'form': form}


    data['html_assetCadFile_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def assetCadFile_delete(request, id):
    comp1 = get_object_or_404(AssetCadFile, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  AssetCadFile.objects.all()
        #Tasks.objects.filter(assetCadFileId=id).update(assetCadFile=id)
        data['html_assetCadFile_list'] = render_to_string('cmms/assetcadfile/partialAssetCadFileList.html', {
            'assetCadFile': companies,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'assetCadFile': comp1}
        data['html_assetCadFile_form'] = render_to_string('cmms/assetcadfile/partialAssetCadFileDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def assetCadFile_create(request):
    if (request.method == 'POST'):
        form = AssetCadFileForm(request.POST,request.FILES)
        return save_assetCadFile_form(request, form, 'cmms/assetcadfile/partialAssetCadFileCreate.html')
    else:

        form = AssetCadFileForm()
        return save_assetCadFile_form(request, form, 'cmms/assetcadfile/partialAssetCadFileCreate.html')




##########################################################
def assetCadFile_update(request, id):
    company= get_object_or_404(AssetCadFile, id=id)
    template=""
    if (request.method == 'POST'):
        form = AssetCadFileForm(request.POST, instance=company)
    else:
        form = AssetCadFileForm(instance=company)


    return save_assetCadFile_form(request, form,"cmms/assetcadfile/partialAssetCadFileUpdate.html",id)
##########################################################

##########################################################
