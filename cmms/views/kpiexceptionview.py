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

from cmms.models.reportsetting import *

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import KpiExceptionForm

###################################################################
def list_kpiException(request,id=None):
    books = KpiException.objects.all()
    return render(request, 'cmms/part_purchase/kpiExceptionList.html', {'kpiExceptions': books})


###################################################################
def js_list_kpiException(request):
    data=dict()
    books=KpiException.objects.filter()

    data['html_kpiException_list']= render_to_string('cmms/settingpages/kpi_exception/partialKpiExceptionList.html', {
        'kpiExceptions': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_kpiException_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = KpiException.objects.all()
                data['html_kpiException_list'] = render_to_string('cmms/settingpages/kpi_exception/partialKpiExceptionList.html', {
                    'kpiExceptions': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_kpiException_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def kpiException_delete(request, id):
    comp1 = get_object_or_404(KpiException, id=id)
    data = dict()

    comp1.delete()
    data['form_is_valid'] = True  # This is just to play along with the existing code
    companies = KpiException.objects.all()
    data['html_kpiException_list'] = render_to_string('cmms/settingpages/kpi_exception/partialKpiExceptionList.html', {
        'kpiExceptions': companies
    })
    return JsonResponse(data)
###################################################################
@csrf_exempt
def kpiException_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['stopcode']=body['stopcode']

        form = KpiExceptionForm(data)
    else:
        form = KpiExceptionForm()

    return save_kpiException_form(request, form, 'cmms/settingpages/kpi_exception/partialKpiExceptionCreate.html')
###################################################################

@csrf_exempt
def kpiException_update(request, id):
    company= get_object_or_404(KpiException, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['stopcode']=body['stopcode']



        form = KpiExceptionForm(data, instance=company)
    else:
        form = KpiExceptionForm(instance=company)
    return save_kpiException_form(request, form, 'cmms/settingpages/kpi_exception/partialKpiExceptionUpdate.html')
