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
from cmms.models.parts import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PartUserForm

###################################################################
def list_partUser(request,id=None):
    books = PartUser.objects.all()
    return render(request, 'cmms/part_user/PartUserList.html', {'partUsers': books})


###################################################################
def js_list_partUser(request,woId):
    data=dict()

    books=PartUser.objects.filter(PartUserPartId=woId)

    data['html_partUser_list']= render_to_string('cmms/part_user/partialPartUserList.html', {
        'partUsers': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_partUser_form(request, form, template_name,woId=None):
    data = dict()
    print(woId)
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = PartUser.objects.filter(PartUserPartId=woId)
            data['html_partUser_list'] = render_to_string('cmms/part_user/partialPartUserList.html', {
                'partUsers': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_partUser_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def partUser_delete(request, id):
    comp1 = get_object_or_404(PartUser, id=id)
    data = dict()
    woId=comp1.PartUserPartId

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = PartUser.objects.filter(PartUserPartId=woId)
        data['html_partUser_list'] = render_to_string('cmms/part_user/partialPartUserList.html', {
            'partUsers': companies
        })
    else:
        context = {'partUser': comp1}
        data['html_partUser_form'] = render_to_string('cmms/part_user/partialPartUserDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def partUser_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['PartUserPartId']=body['PartUserPartId']
        data['PartUserUserId']=body['PartUserUserId']


        woId=body['PartUserPartId']

        form = PartUserForm(data)

    else:
        form = PartUserForm()
    return save_partUser_form(request, form, 'cmms/part_user/partialPartUserCreate.html',woId)
###################################################################

@csrf_exempt
def partUser_update(request, id):
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)

    company= get_object_or_404(PartUser, id=id)
    woId=company.PartUserPartId
    logging.debug(woId)
    print(woId)
    print("update")
    if (request.method == 'POST'):
        print("update")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['PartUserPartId']=body['PartUserPartId']
        data['PartUserUserId']=body['PartUserUserId']



        form = PartUserForm(data, instance=company)
    else:
        form = PartUserForm(instance=company)
    return save_partUser_form(request, form, 'cmms/part_user/partialPartUserUpdate.html',woId)
