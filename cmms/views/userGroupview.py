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

from cmms.models.users import *

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import UserGroupForm

###################################################################
def list_userGroup(request,id=None):
    books = UserGroup.objects.all()
    return render(request, 'cmms/usergroup/userGroupList.html', {'userGroups': books})


###################################################################
def js_list_userGroup2(request):
    data=dict()
    books=UserGroup.objects.filter()

    data['html_userGroup_list']= render_to_string('cmms/settingpages/usergroup/partialUserGrouplist.html', {
        'userGroups': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_userGroup_form(request, form, template_name):
        data = dict()
        if (request.method == 'POST'):
              if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                fmt = getattr(settings, 'LOG_FORMAT', None)
                lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                logging.basicConfig(format=fmt, level=lvl)
                # logging.debug( woId)
                books = UserGroup.objects.all()
                data['html_userGroup_list'] = render_to_string('cmms/settingpages/usergroup/partialUserGrouplist.html', {
                    'userGroups': books
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)

        context = {'form': form}
        data['html_userGroup_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################


def userGroup_delete(request, id):
    comp1 = get_object_or_404(UserGroup, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = UserGroup.objects.all()
        data['html_userGroup_list'] = render_to_string('cmms/settingpages/usergroup/partialUserGrouplist.html', {
            'userGroup': companies
        })
    else:
        context = {'userGroup': comp1}
        data['html_userGroup_form'] = render_to_string('cmms/settingpages/userGroup/partialUserGroupDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def userGroup_create(request):
    woId=-1
    print("enter:")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['userGroupCode']=body['userGroupCode']
        data['userGroupName']=body['userGroupName']
        data['userGroupIsPartOF']=body['userGroupIsPartOF']
        data['userUserLocation']=body['userUserLocation']
        data['userGroupZarib']=body['userGroupZarib']

        form = UserGroupForm(data)
    else:
        form = UserGroupForm()

    return save_userGroup_form(request, form, 'cmms/settingpages/usergroup/partialUserGroupCreate.html')
###################################################################

@csrf_exempt
def userGroup_update(request, id):
    company= get_object_or_404(UserGroup, id=id)
    # woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['userGroupCode']=body['userGroupCode']
        data['userGroupName']=body['userGroupName']
        data['userGroupIsPartOF']=body['userGroupIsPartOF']
        data['userUserLocation']=body['userUserLocation']
        data['userGroupZarib']=body['userGroupZarib']
        data['userGroupZaribTamir']=body['userGroupZaribTamir']
        data['userGroupZaribService']=body['userGroupZaribService']
        data['userGroupZaribProject']=body['userGroupZaribProject']
        form = UserGroupForm(data, instance=company)

    else:
        form = UserGroupForm(instance=company)
    return save_userGroup_form(request, form, 'cmms/settingpages/usergroup/partialUserGroupUpdate.html')
