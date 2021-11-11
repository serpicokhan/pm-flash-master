'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nebusinessbject.OrderId.id)
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

from cmms.models.business import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import BusinessForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.context_processors import PermWrapper
from cmms.business.BusiUtil import *



def list_business(request,id=None):
    #
    books = Business.objects.all().order_by('name')
    wos=BusinessUtility.doPaging(request,books)

    return render(request, 'cmms/business/businessList.html', {'business': wos,'section':'list_business'})


##########################################################

def save_business_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Business.objects.all().order_by('name')
            data['html_business_list'] = render_to_string('cmms/business/partialBusinesslist.html', {
                'business': books
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form,'lId':id}


    data['html_business_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def business_delete(request, id):
    comp1 = get_object_or_404(Business, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  Business.objects.all().order_by('name')
        #Tasks.objects.filter(businessId=id).update(business=id)
        data['html_business_list'] = render_to_string('cmms/business/partialBusinesslist.html', {
            'business': companies
        })
    else:
        context = {'business': comp1}
        data['html_business_form'] = render_to_string('cmms/business/partialBusinessDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def business_create(request):
    if (request.method == 'POST'):
        form = BusinessForm(request.POST)
        return save_business_form(request, form, 'cmms/business/partialBusinessCreate.html')
    else:
        businessInstance=Business.objects.create()
        form = BusinessForm(instance=businessInstance)
        return save_business_form(request, form, 'cmms/business/partialBusinessCreate.html',businessInstance.id)




##########################################################
def business_update(request, id):
    company= get_object_or_404(Business, id=id)
    template=""
    if (request.method == 'POST'):
        form = BusinessForm(request.POST, instance=company)
    else:
        form = BusinessForm(instance=company)
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)
    logging.debug(id)

    return save_business_form(request, form,"cmms/business/partialBusinessUpdate.html",id)
##########################################################

##########################################################
def businessCancel(request,id):
    data=dict()
    # tg=Business.objects.get(id=id)
    # if(tg):
    #     if(not tg.name):
    #         tg.delete()
    #         data['form_is_valid'] = True  # This is just to play along with the existing code
    #         companies =  Business.objects.all().order_by('name')
    #         #Tasks.objects.filter(taskGroupId=id).update(taskGroup=id)
    #         data['html_business_list'] = render_to_string('cmms/business/partialBusinesslist.html', {
    #             'business': companies
    #         })

    return JsonResponse(data)
#####################
def business_search(request,searchStr):
    data=dict()
    searchStr=searchStr.replace('_',' ')
    books=BusinessUtility.seachBusiness(searchStr).order_by('name')
    wos=BusinessUtility.doPaging(request,list(books))
    data['html_business_search_tag_list'] = render_to_string('cmms/business/partialBusinessList.html', {               'business': wos  ,'perms': PermWrapper(request.user)                       })
    # data['html_business_paginator'] = render_to_string('cmms/business/partialBusinessPagination.html', {
    #       'business': wos,'pageType':'business_search','ptr':searchStr})
    data['form_is_valid'] = True
    return JsonResponse(data)
