'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nemaintenanceTypebject.OrderId.id)
 '''
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

from cmms.models.workorder import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import MaintenanceTypeForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper

@permission_required('cmms.view_maintenancetype')
def list_maintenanceType(request,id=None):
    #
    books = MaintenanceType.objects.all()
    return render(request, 'cmms/maintenancetype/maintenanceTypeList.html', {'maintenanceType': books})


##########################################################

def save_maintenanceType_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = MaintenanceType.objects.all()
            data['html_maintenanceType_list'] = render_to_string('cmms/maintenancetype/partialMaintenanceTypelist.html', {
                'maintenanceType': books,
                'perms': PermWrapper(request.user)
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}


    data['html_maintenanceType_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def maintenanceType_delete(request, id):
    comp1 = get_object_or_404(MaintenanceType, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  MaintenanceType.objects.all()
        #Tasks.objects.filter(maintenanceTypeId=id).update(maintenanceType=id)
        data['html_maintenanceType_list'] = render_to_string('cmms/maintenancetype/partialMaintenanceTypelist.html', {
            'maintenanceType': companies,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'maintenanceType': comp1}
        data['html_maintenanceType_form'] = render_to_string('cmms/maintenancetype/partialMaintenanceTypeDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def maintenanceType_create(request):
    if (request.method == 'POST'):
        form = MaintenanceTypeForm(request.POST)
        return save_maintenanceType_form(request, form, 'cmms/maintenancetype/partialMaintenanceTypeCreate.html')
    else:

        form = MaintenanceTypeForm()
        return save_maintenanceType_form(request, form, 'cmms/maintenancetype/partialMaintenanceTypeCreate.html')




##########################################################
def maintenanceType_update(request, id):
    company= get_object_or_404(MaintenanceType, id=id)
    template=""
    if (request.method == 'POST'):
        form = MaintenanceTypeForm(request.POST, instance=company)
    else:
        form = MaintenanceTypeForm(instance=company)


    return save_maintenanceType_form(request, form,"cmms/maintenancetype/partialMaintenanceTypeUpdate.html",id)
##########################################################

##########################################################
