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

from cmms.models.workorder import *

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import ProblemCodeForm

###################################################################
def list_woProblem(request,id=None):
    books = ProblemCode.objects.all()
    return render(request, 'cmms/part_purchase/woProblemList.html', {'woProblems': books})


###################################################################
def js_list_woProblem(request):
    data=dict()
    books=ProblemCode.objects.filter()

    data['html_woProblem_list']= render_to_string('cmms/settingpages/wo_problem_code/partialWoProblemlist.html', {
        'woProblems': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_woProblem_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = ProblemCode.objects.all()
                data['html_woProblem_list'] = render_to_string('cmms/settingpages/wo_problem_code/partialWoProblemlist.html', {
                    'woProblems': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_woProblem_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def woProblem_delete(request, id):
    comp1 = get_object_or_404(ProblemCode, id=id)
    data = dict()


    comp1.delete()
    data['form_is_valid'] = True  # This is just to play along with the existing code
    companies = ProblemCode.objects.all()
    data['html_woProblem_list'] = render_to_string('cmms/settingpages/wo_problem_code/partialWoProblemlist.html', {
        'woProblems': companies
    })
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woProblem_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['problemCode']=body['problemCode']
        data['problemDescription']=body['problemDescription']
        data['problemIsActive']=True if body['problemDescription'] is 'true' else False
        form = ProblemCodeForm(data)
    else:
        form = ProblemCodeForm()

    return save_woProblem_form(request, form, 'cmms/settingpages/wo_problem_code/partialWoProblemCreate.html')
###################################################################

@csrf_exempt
def woProblem_update(request, id):
    company= get_object_or_404(ProblemCode, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['problemCode']=body['problemCode']
        data['problemDescription']=body['problemDescription']


        form = ProblemCodeForm(data, instance=company)
    else:
        form = ProblemCodeForm(instance=company)
    return save_woProblem_form(request, form, 'cmms/settingpages/wo_problem_code/partialWoProblemUpdate.html')
