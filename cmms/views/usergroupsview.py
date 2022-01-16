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
from cmms.forms import UserGroup

###################################################################
def list_userGroup(request,id=None):
    books = UserGroup.objects.all()
    return render(request, 'cmms/user_group/userGroupList.html', {'userGroups': books})


###################################################################
def js_list_userGroup(request,woId):
    data=dict()


    books=UserGroups.objects.filter(userUserGroups=woId)

    book=UserGroup.objects.exclude(id__in=[o.groupUserGroups_id for o in books ])

    data['html_userGroup_list']= render_to_string('cmms/user_group/partialUserGroupList.html', {
        'userGroups': books,
        'userGroup':book
    })
    data['form_is_valid']=True

    return JsonResponse(data)


###################################################################    ###################################################################
def update_usergroup(request,userId,groupId):
    company=UserGroups.objects.filter(userUserGroups=userId,groupUserGroups=groupId)

    if(company):

        company.delete()
        print("deleted")
    else:
        UserGroups.objects.create(userUserGroups_id=userId,groupUserGroups_id=groupId)
        print("created")
    data=dict()
    return JsonResponse(data)
