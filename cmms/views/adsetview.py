from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings


#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import BusinessForm
from django.urls import reverse_lazy
from django.db import transaction
from cmms.models import *

###################################################################
def not_found(request):
    # data=dict()
    # books=[]
    # books=AdminSetting.objects.all()

    # data['html_adminSetting_list']= render_to_string('cmms/AdminSetting/partialAdminSettinglist.html', {
    #     'adminSettings': books
    # })
    # data['form_is_valid']=True
    # books = Business.objects.all()
    return render(request, 'cmms/404.html', {'business':123 })
    # form = AdSetForm()
    #return JsonResponse(data)
    # return render(request, 'cmms/a123/businessList.html', {'form': form})
