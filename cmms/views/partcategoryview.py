'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nepartCategorybject.OrderId.id)
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

from cmms.models.parts import PartCategory
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PartCategoryForm
from django.urls import reverse_lazy
from django.db import transaction
from django.db import IntegrityError

from rest_framework.decorators import api_view
# from cmms.api.WOSerializer import PartCategorySerializer
from rest_framework.response import Response

def list_partCategory(request,id=None):
    #
    books = PartCategory.objects.all()
    return render(request, 'cmms/partcategory/partCategoryList.html', {'partCategory': books,'section':'list_partCategory'})


##########################################################

def save_partCategory_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):

        if form.is_valid():


                form.save()
                data['form_is_valid'] = True
                books = PartCategory.objects.all()
                data['html_partCategory_list'] = render_to_string('cmms/partcategory/partialPartCategoryList.html', {
                    'partCategory': books
                })

        else:
            data["error"]=form.errors
            data['form_is_valid'] = False


    context = {'form': form}


    data['html_partCategory_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def partCategory_delete(request, id):
    comp1 = get_object_or_404(PartCategory, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  PartCategory.objects.all()
        #Tasks.objects.filter(partCategoryId=id).update(partCategory=id)
        data['html_partCategory_list'] = render_to_string('cmms/partcategory/partialPartCategoryList.html', {
            'partCategory': companies
        })
    else:
        context = {'partCategory': comp1}
        data['html_partCategory_form'] = render_to_string('cmms/partcategory/partialPartCategoryDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def partCategory_create(request):
    if (request.method == 'POST'):
        form = PartCategoryForm(request.POST)
        return save_partCategory_form(request, form, 'cmms/partcategory/partialPartCategoryCreate.html')
    else:

        form = PartCategoryForm()
        return save_partCategory_form(request, form, 'cmms/partcategory/partialPartCategoryCreate.html')




##########################################################
def partCategory_update(request, id):
    company= get_object_or_404(PartCategory, id=id)
    template=""
    if (request.method == 'POST'):
        form = PartCategoryForm(request.POST, instance=company)
    else:
        form = PartCategoryForm(instance=company)


    return save_partCategory_form(request, form,"cmms/partcategory/partialPartCategoryUpdate.html",id)
##########################################################

##########################################################
@api_view(['GET'])
def partcategory_collection(request):
    if request.method == 'GET':
        posts = PartCategory.objects.all()
        serializer = PartCategorySerializer(posts, many=True)
        return Response(serializer.data)
@api_view(['GET'])
def partcategory_detail_collection(request,id):
    if request.method == 'GET':
        posts = PartCategory.objects.get(id=id)
        serializer = PartCategorySerializer(posts)
        return Response(serializer.data)
