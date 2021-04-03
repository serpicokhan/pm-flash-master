'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nemachineCategorybject.OrderId.id)
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

from cmms.models.machinecategory import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import MachineCategoryForm
from django.urls import reverse_lazy
from django.db import transaction



def list_machineCategory(request,id=None):
    #
    books = MachineCategory.objects.all()
    print(books)
    return render(request, 'cmms/machinecategory/machineCategoryList.html', {'machineCategory': books})


##########################################################

def save_machineCategory_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = MachineCategory.objects.all()
            data['html_machineCategory_list'] = render_to_string('cmms/machineCategory/partialMachineCategorylist.html', {
                'machineCategory': books
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}


    data['html_machineCategory_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def machineCategory_delete(request, id):
    comp1 = get_object_or_404(MachineCategory, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  MachineCategory.objects.all()
        #Tasks.objects.filter(machineCategoryId=id).update(machineCategory=id)
        data['html_machineCategory_list'] = render_to_string('cmms/machineCategory/partialMachineCategorylist.html', {
            'machineCategory': companies
        })
    else:
        context = {'machineCategory': comp1}
        data['html_machineCategory_form'] = render_to_string('cmms/machineCategory/partialMachineCategoryDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def machineCategory_create(request):
    if (request.method == 'POST'):
        form = MachineCategoryForm(request.POST)
        return save_machineCategory_form(request, form, 'cmms/machineCategory/partialMachineCategoryCreate.html')
    else:

        form = MachineCategoryForm()
        return save_machineCategory_form(request, form, 'cmms/machineCategory/partialMachineCategoryCreate.html')




##########################################################
def machineCategory_update(request, id):
    company= get_object_or_404(MachineCategory, id=id)
    template=""
    if (request.method == 'POST'):
        form = MachineCategoryForm(request.POST, instance=company)
    else:
        form = MachineCategoryForm(instance=company)


    return save_machineCategory_form(request, form,"cmms/machineCategory/partialMachineCategoryUpdate.html",id)
##########################################################

##########################################################
