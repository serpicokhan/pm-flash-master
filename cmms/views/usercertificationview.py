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

from cmms.models.parts import *
from cmms.models.waranty import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import UserCertificationForm
from cmms.business.DateJob import *
###################################################################
def list_userCertification(request,id=None):
    books = UserCertification.objects.all()
    return render(request, 'cmms/user_certificate/userCertList.html', {'userCertifications': books})


###################################################################
def js_list_userCertification(request,woId):
    data=dict()
    books=UserCertification.objects.filter(userCertificationUser=woId)
    #print(books[0].userCertificationUser)
    data['html_userCertification_list']= render_to_string('cmms/user_certificate/partialUserCertList.html', {
        'userCertifications': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_userCertification_form(request, form, template_name,woId=None):
        data = dict()
        if (request.method == 'POST'):
              # print(request.POST)
              # print("here is good")

              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                books = UserCertification.objects.filter(userCertificationUser=woId)
                data['html_userCertification_list'] = render_to_string('cmms/user_certificate/partialUserCertList.html', {
                    'userCertifications': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_userCertification_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################

@csrf_exempt
def userCertification_delete(request, id):
    comp1 = get_object_or_404(UserCertification, id=id)
    woId=comp1.userCertificationUser
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        print(woId.id)
        companies = UserCertification.objects.filter(userCertificationUser=woId)
        data['html_userCertification_list'] = render_to_string('cmms/user_certificate/partialUserCertList.html', {
            'userCertifications': companies
        })
    else:
        context = {'userCertification': comp1}
        data['html_userCertification_form'] = render_to_string('cmms/user_certificate/partialUserCertDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def userCertification_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['userCertificationName']=body['userCertificationName']
        data['userCertificationUser']=body['userCertificationUser']
        data['userCertificationType']=body['userCertificationType']
        data['userCertificationDesc']=body['userCertificationDesc']
        data['userCertificationStart']=DateJob.getDate(body['userCertificationStart'])
        data['userCertificationEnd']=DateJob.getDate(body['userCertificationEnd'])
        woId=body['userCertificationUser']
        form = UserCertificationForm(data)

    else:
        form = UserCertificationForm()
    return save_userCertification_form(request, form, 'cmms/user_certificate/partialUserCertCreate.html',woId)
###################################################################

@csrf_exempt
def userCertification_update(request, id):
    company= get_object_or_404(UserCertification, id=id)
    woId=company.userCertificationUser
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['userCertificationName']=body['userCertificationName']
        data['userCertificationUser']=body['userCertificationUser']
        data['userCertificationType']=body['userCertificationType']
        data['userCertificationDesc']=body['userCertificationDesc']
        data['userCertificationStart']=DateJob.getDate(body['userCertificationStart'])
        data['userCertificationEnd']=DateJob.getDate(body['userCertificationEnd'])
        form = UserCertificationForm(data, instance=company)
    else:
        form = UserCertificationForm(instance=company)
    return save_userCertification_form(request, form, 'cmms/user_certificate/partialUserCertUpdate.html',woId)
