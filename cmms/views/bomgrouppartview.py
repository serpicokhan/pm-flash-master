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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import BOMGroupPartForm

###################################################################


###################################################################
def js_list_bomGroupPart(request,woId):
    data=dict()


    books=BOMGroupPart.objects.filter(BOMGroupPartBOMGroup=woId)

    data['html_bomGroupPart_list']= render_to_string('cmms/bomgroup_parts/partialBOMGroupPartList.html', {
        'bomGroupParts': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_bomGroupPart_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True


            books=BOMGroupPart.objects.filter(BOMGroupPartBOMGroup=woId)

            data['html_bomGroupPart_list'] = render_to_string('cmms/bomgroup_parts/partialBOMGroupPartList.html', {
                'bomGroupParts': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)
              data['form_is_valid'] = False

    context = {'form': form}
    data['html_bomGroupPart_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def bomGroupPart_delete(request, id):
    comp1 = get_object_or_404(BOMGroupPart, id=id)
    data = dict()
    woId=comp1.BOMGroupPartBOMGroup

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code


        books=BOMGroupPart.objects.filter(BOMGroupPartBOMGroup=woId)

        data['html_bomGroupPart_list'] = render_to_string('cmms/bomgroup_parts/partialBOMGroupPartList.html', {
            'bomGroupParts': books
        })
    else:
        context = {'bomGroupPart': comp1}
        data['html_bomGroupPart_form'] = render_to_string('cmms/bomgroup_parts/partialBOMGroupPartDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def bomGroupPart_create(request):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['BOMGroupPartBOMGroup']=body['BOMGroupPartBOMGroup']
        data['BOMGroupPartPart']=body['BOMGroupPartPart']
        data['BOMGroupPartQnty']=body['BOMGroupPartQnty']

        woId=body['BOMGroupPartBOMGroup']

        form = BOMGroupPartForm(data)

    else:
        form = BOMGroupPartForm()
    return save_bomGroupPart_form(request, form, 'cmms/bomgroup_parts/partialBOMGroupPartCreate.html',woId)
###################################################################

@csrf_exempt
def bomGroupPart_update(request, id):
    company= get_object_or_404(BOMGroupPart, id=id)
    woId=company.BOMGroupPartBOMGroup
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['BOMGroupPartBOMGroup']=body['BOMGroupPartBOMGroup']
        data['BOMGroupPartPart']=body['BOMGroupPartPart']
        data['BOMGroupPartQnty']=body['BOMGroupPartQnty']


        form = BOMGroupPartForm(data, instance=company)
    else:
        form = BOMGroupPartForm(instance=company,initial={'mypart':company.BOMGroupPartPart.partName})
    return save_bomGroupPart_form(request, form, 'cmms/bomgroup_parts/partialBOMGroupPartUpdate.html',woId.id)
