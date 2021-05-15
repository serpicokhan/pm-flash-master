'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neassetCategorybject.OrderId.id)
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

from cmms.models.assetcategory import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetCategoryForm
from django.urls import reverse_lazy
from django.db import transaction



def list_assetCategory(request,id=None):
    #
    books = AssetCategory.objects.all()
    return render(request, 'cmms/assetcategory/assetCategoryList.html', {'assetCategory': books})


##########################################################

def save_assetCategory_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = AssetCategory.objects.all()
            data['html_assetCategory_list'] = render_to_string('cmms/assetcategory/partialAssetCategoryList.html', {
                'assetCategory': books
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}


    data['html_assetCategory_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def assetCategory_delete(request, id):
    comp1 = get_object_or_404(AssetCategory, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  AssetCategory.objects.all()
        #Tasks.objects.filter(assetCategoryId=id).update(assetCategory=id)
        data['html_assetCategory_list'] = render_to_string('cmms/assetcategory/partialAssetCategoryList.html', {
            'assetCategory': companies
        })
    else:
        context = {'assetCategory': comp1}
        data['html_assetCategory_form'] = render_to_string('cmms/assetcategory/partialAssetCategoryDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def assetCategory_create(request):
    if (request.method == 'POST'):
        form = AssetCategoryForm(request.POST)
        return save_assetCategory_form(request, form, 'cmms/assetcategory/partialAssetCategoryCreate.html')
    else:

        form = AssetCategoryForm()
        return save_assetCategory_form(request, form, 'cmms/assetcategory/partialAssetCategoryCreate.html')




##########################################################
def assetCategory_update(request, id):
    company= get_object_or_404(AssetCategory, id=id)
    template=""
    if (request.method == 'POST'):
        form = AssetCategoryForm(request.POST, instance=company)
    else:
        form = AssetCategoryForm(instance=company)


    return save_assetCategory_form(request, form,"cmms/assetcategory/partialAssetCategoryUpdate.html",id)
##########################################################

##########################################################
