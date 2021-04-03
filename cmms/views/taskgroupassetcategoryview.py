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

import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings

from cmms.models.task import *
from cmms.models.waranty import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import TaskGroupAssetCategoryForm

###################################################################
def list_taskGroupAssetCategory(request,id=None):
    books = TaskGroupAssetCategory.objects.all()
    return render(request, 'cmms/taskgroup_assetcategory/taskGroupAssetCategoryList.html', {'taskGroupAssetCategorys': books})


###################################################################
def js_list_taskGroupAssetCategory(request,woId):
    data=dict()
    books=TaskGroupAssetCategory.objects.filter(TaskGroup=woId)

    data['html_taskGroupAssetCategory_list']= render_to_string('cmms/taskgroup_assetcategory/partialTaskGroupAssetCategorylist.html', {
        'taskGroupAssetCategorys': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_taskGroupAssetCategory_form(request, form, template_name,woId=None):
        data = dict()


        if (request.method == 'POST'):
              # print(request.POST)
              # print("here is good")

              if form.is_valid():

                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                logging.debug( woId)
                books = TaskGroupAssetCategory.objects.filter(TaskGroup=woId)
                data['html_taskGroupAssetCategory_list'] = render_to_string('cmms/taskgroup_assetcategory/partialTaskGroupAssetCategorylist.html', {
                    'taskGroupAssetCategorys': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_taskGroupAssetCategory_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################

@csrf_exempt
def taskGroupAssetCategory_delete(request, id):
    comp1 = get_object_or_404(TaskGroupAssetCategory, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = TaskGroupAssetCategory.objects.filter(TaskGroup=comp1.TaskGroup)
        data['html_taskGroupAssetCategory_list'] = render_to_string('cmms/taskgroup_assetcategory/partialTaskGroupAssetCategorylist.html', {
            'taskGroupAssetCategorys': companies
        })
    else:
        context = {'taskGroupAssetCategory': comp1}
        data['html_taskGroupAssetCategory_form'] = render_to_string('cmms/taskgroup_assetcategory/partialTaskGroupAssetCategoryDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def taskGroupAssetCategory_create(request):
    woId=-1
    # print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['TaskGroup']=body['TaskGroup']
        data['assetCategory']=body['assetCategory']

        data['includeSubCategory']=True if body['includeSubCategory']==True else False





        woId=body['TaskGroup']



        form = TaskGroupAssetCategoryForm(data)



    else:
        form = TaskGroupAssetCategoryForm()
    # print(form)
    return save_taskGroupAssetCategory_form(request, form, 'cmms/taskgroup_assetcategory/partialTaskGroupAssetCategoryCreate.html',woId)
###################################################################

@csrf_exempt
def taskGroupAssetCategory_update(request, id):
    company= get_object_or_404(TaskGroupAssetCategory, id=id)
    woId=company.TaskGroup
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data = request.POST.dict()
        data['TaskGroup']=body['TaskGroup']
        data['assetCategory']=body['assetCategory']
        print(body['includeSubCategory'],"$$$$$$$$$$$$$$$$$")

        data['includeSubCategory']=True if body['includeSubCategory']==True else False


        form = TaskGroupAssetCategoryForm(data, instance=company)
    else:
        form = TaskGroupAssetCategoryForm(instance=company)
    return save_taskGroupAssetCategory_form(request, form, 'cmms/taskgroup_assetcategory/partialTaskGroupAssetCategoryUpdate.html',woId)
