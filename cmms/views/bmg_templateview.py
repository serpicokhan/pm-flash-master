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
from cmms.forms import BMGTemplateForm

###################################################################


###################################################################
def js_list_bmgTemplate(request,woId):
    data=dict()


    books=BMGTemplate.objects.filter(BMGGroup=woId)

    data['html_bmgTemplate_list']= render_to_string('cmms/bmgroup_meter_template/partialBMGTemplateList.html', {
        'bmgTemplates': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_bmgTemplate_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True


            books=BMGTemplate.objects.filter(BMGGroup=woId)

            data['html_bmgTemplate_list'] = render_to_string('cmms/bmgroup_meter_template/partialBMGTemplateList.html', {
                'bmgTemplates': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)
              data['form_is_valid'] = False

    context = {'form': form}
    data['html_bmgTemplate_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def bmgTemplate_delete(request, id):
    comp1 = get_object_or_404(BMGTemplate, id=id)
    data = dict()
    woId=comp1.BMGGroup

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code


        books=BMGTemplate.objects.filter(BMGGroup=woId)

        data['html_bmgTemplate_list'] = render_to_string('cmms/bmgroup_meter_template/partialBMGTemplateList.html', {
            'bmgTemplates': books
        })
    else:
        context = {'bmgTemplate': comp1}
        data['html_bmgTemplate_form'] = render_to_string('cmms/bmgroup_meter_template/partialBMGTemplateDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def bmgTemplate_create(request):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['BMGGroup']=body['BMGGroup']
        data['BMGTemplate']=body['BMGTemplate']
        woId=body['BMGGroup']

        form = BMGTemplateForm(data)

    else:
        form = BMGTemplateForm()
    return save_bmgTemplate_form(request, form, 'cmms/bmgroup_meter_template/partialBMGTemplateCreate.html',woId)
###################################################################

@csrf_exempt
def bmgTemplate_update(request, id):
    company= get_object_or_404(BMGTemplate, id=id)
    woId=company.BMGGroup
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['BMGGroup']=body['BMGGroup']
        data['BMGTemplate']=body['BMGTemplate']


        form = BMGTemplateForm(data, instance=company)
    else:
        form = BMGTemplateForm(instance=company,initial={'mypart':company.BMGTemplate.assetMeterTemplateDesc})
    return save_bmgTemplate_form(request, form, 'cmms/bmgroup_meter_template/partialBMGTemplateUpdate.html',woId.id)
