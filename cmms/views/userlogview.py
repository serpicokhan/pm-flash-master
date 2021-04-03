
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string


from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf

import logging
from django.conf import settings
from cmms.models.users import *
from cmms.models.task import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict


###################################################################



###################################################################
def js_list_userLog(request,woId):
    data=dict()
    books=WorkOrder.objects.filter(assignedToUser=woId).order_by('-id')[:10]

    data['html_userLog_list']= render_to_string('cmms/user_log/partialUserLogList.html', {
        'userLogs': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
