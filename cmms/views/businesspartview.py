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

from cmms.models.Asset import *
from cmms.models.waranty import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import BusinessPartForm

###################################################################
def list_businessPart(request,id=None):
    books = BusinessPart.objects.all()
    return render(request, 'cmms/business_part/businessPartList.html', {'businessPart': books})


###################################################################
def js_list_businessPart(request,woId):
    data=dict()
    books=BusinessPart.objects.filter(businessPartBusiness=woId)

    data['html_businessPart_list']= render_to_string('cmms/business_part/partialBusinessPartList.html', {
        'businessParts': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_businessPart_form(request, form, template_name,woId=None):
        data = dict()


        if (request.method == 'POST'):
              print(request.POST)
              print("here is good")

              if form.is_valid():

                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                logging.debug( woId)
                books = BusinessPart.objects.filter(businessPartBusiness=woId)
                data['html_businessPart_list'] = render_to_string('cmms/business_part/partialBusinessPartList.html', {
                    'businessParts': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_businessPart_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def businessPart_delete(request, id):
    comp1 = get_object_or_404(BusinessPart, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = BusinessPart.objects.all()
        data['html_businessPart_list'] = render_to_string('cmms/business_part/partialBusinessPartList.html', {
            'businessPart': companies
        })
    else:
        context = {'businessPart': comp1}
        data['html_businessPart_form'] = render_to_string('cmms/business_part/partialBusinessPartDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def businessPart_create(request,pid=None):
    woId=-1





    #print(parts.BusinessPartPart)


    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['BusinessPartPart']=body['BusinessPartPart']
        data['businessPartBusiness']=body['businessPartBusiness']
        data['businessPartBusinessType']=body['businessPartBusinessType']

        data['businessPartSupplierPartNumber']=body['businessPartSupplierPartNumber']
        data['businessPartCatalog']=body['businessPartCatalog']
        data['businessPartisDefault']=True if body['businessPartisDefault']=='true' else False





        woId=body['businessPartBusiness']



        form = BusinessPartForm(data)



    else:
        form = BusinessPartForm()

    return save_businessPart_form(request, form, 'cmms/business_part/partialBusinessPartCreate.html',woId)
###################################################################

@csrf_exempt
def businessPart_update(request, id):
    company= get_object_or_404(BusinessPart, id=id)
    woId=company.businessPartBusiness
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['BusinessPartPart']=body['BusinessPartPart']
        data['businessPartBusiness']=body['businessPartBusiness']
        data['businessPartBusinessType']=body['businessPartBusinessType']

        data['businessPartSupplierPartNumber']=body['businessPartSupplierPartNumber']
        data['businessPartCatalog']=body['businessPartCatalog']
        data['businessPartisDefault']=True if body['businessPartisDefault']=='true' else False



        form = BusinessPartForm(data, instance=company)
    else:
        form = BusinessPartForm(instance=company)
    return save_businessPart_form(request, form, 'cmms/business_part/partialBusinessPartUpdate.html',woId)
