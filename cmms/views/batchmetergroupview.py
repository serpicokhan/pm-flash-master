'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nebatchMeterGroupbject.OrderId.id)
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
from cmms.business.AssetUtility import *

from cmms.models.Asset import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import BatchMeterGroupForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.context_processors import PermWrapper
from django.db import IntegrityError
from django.core.paginator import *



def list_batchMeterGroup(request,id=None):
    #
    books = BatchMeterGroup.objects.all().order_by('BatchMeterGroupName')
    books=AssetUtility.doPaging(request,books)
    return render(request, 'cmms/batch_meter_group/batchMeterGroupList.html', {'batchMeterGroup': books,'section':'list_batchMeterGroup'})


##########################################################

def save_batchMeterGroup_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        try:
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                books1 = BatchMeterGroup.objects.all().order_by('BatchMeterGroupName')
                books=AssetUtility.doPaging(request,books1)
                data['html_batchMeterGroup_list'] = render_to_string('cmms/batch_meter_group/partialBatchMeterGroupList.html', {
                    'batchMeterGroup': books,
                    'perms': PermWrapper(request.user)
                })


            else:
                data['form_is_valid'] = False
        except IntegrityError as exc:
            print(exc)
            data['form_is_valid'] = False
            data['bom_error']="نام گروه تکراری"
        except Exeption as c:
            print("!2321")

    context = {'form': form,'lId':id}


    data['html_batchMeterGroup_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def batchMeterGroup_delete(request, id):
    comp1 = get_object_or_404(BatchMeterGroup, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies1 =  BatchMeterGroup.objects.all().order_by('BatchMeterGroupName')
        companies=AssetUtility.doPaging(request,companies1)
        #Tasks.objects.filter(batchMeterGroupId=id).update(batchMeterGroup=id)
        data['html_batchMeterGroup_list'] = render_to_string('cmms/batch_meter_group/partialBatchMeterGroupList.html', {
            'batchMeterGroup': companies,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'batchMeterGroup': comp1}
        data['html_batchMeterGroup_form'] = render_to_string('cmms/batch_meter_group/partialBatchMeterGroupDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def batchMeterGroup_create(request):
    if (request.method == 'POST'):
        form = BatchMeterGroupForm(request.POST)
        return save_batchMeterGroup_form(request, form, 'cmms/batch_meter_group/partialBatchMeterGroupCreate.html')
    else:
        batchMeterGroupInstance=BatchMeterGroup.objects.create()
        form = BatchMeterGroupForm(instance=batchMeterGroupInstance)
        return save_batchMeterGroup_form(request, form, 'cmms/batch_meter_group/partialBatchMeterGroupCreate.html',batchMeterGroupInstance.id)




##########################################################
def batchMeterGroup_update(request, id):
    company= get_object_or_404(BatchMeterGroup, id=id)
    template=""
    if (request.method == 'POST'):
        form = BatchMeterGroupForm(request.POST, instance=company)
    else:
        form = BatchMeterGroupForm(instance=company)
    return save_batchMeterGroup_form(request, form,"cmms/batch_meter_group/partialBatchMeterGroupUpdate.html",id)
##########################################################

##########################################################
def batchMeterGroupCancel(request,id):
    data=dict()
    tg=BatchMeterGroup.objects.get(id=id)
    if(tg):
        if(not tg.BatchMeterGroupName):
            tg.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            companies1 =  BatchMeterGroup.objects.all().order_by('BatchMeterGroupName')
            companies=AssetUtility.doPaging(request,companies1)
            #Tasks.objects.filter(taskGroupId=id).update(taskGroup=id)
            data['html_batchMeterGroup_list'] = render_to_string('cmms/batch_meter_group/partialBatchMeterGroupList.html', {
                'batchMeterGroup': companies
            })

    return JsonResponse(data)
##############
#####################
def batchMeterGroup_search(request,searchStr):
    data=dict()
    searchStr=searchStr.replace('_',' ')
    books=TaskUtility.seachBOM(searchStr).order_by('name')
    wos=AssetUtility.doPaging(request,list(books))
    data['html_html_batchMeterGroup_list_search_tag_list'] = render_to_string('cmms/business/partialBusinessList.html', {               'business': wos  ,'perms': PermWrapper(request.user)                       })
    # data['html_business_paginator'] = render_to_string('cmms/business/partialBusinessPagination.html', {
    #       'business': wos,'pageType':'business_search','ptr':searchStr})
    data['form_is_valid'] = True
    return JsonResponse(data)
