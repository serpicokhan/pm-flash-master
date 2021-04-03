'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nebomgroupbject.OrderId.id)
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
from cmms.business.AssetUtility import *

from cmms.models.Asset import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import BOMGroupForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.context_processors import PermWrapper



def list_bomgroup(request,id=None):
    #
    books = BOMGroup.objects.all().order_by('BOMGroupName')
    books=AssetUtility.doPaging(request,books)
    return render(request, 'cmms/bomgroup/bomgroupList.html', {'bomgroup': books})


##########################################################

def save_bomgroup_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = BOMGroup.objects.all().order_by('BOMGroupName')
            books=AssetUtility.doPaging(request,books)
            data['html_bomgroup_list'] = render_to_string('cmms/bomgroup/partialBOMGrouplist.html', {
                'bomgroup': books,
                'perms': PermWrapper(request.user)
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form,'lId':id}


    data['html_bomgroup_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def bomgroup_delete(request, id):
    comp1 = get_object_or_404(BOMGroup, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  BOMGroup.objects.all().order_by('BOMGroupName')
        companies=AssetUtility.doPaging(request,companies)
        #Tasks.objects.filter(bomgroupId=id).update(bomgroup=id)
        data['html_bomgroup_list'] = render_to_string('cmms/bomgroup/partialBOMGrouplist.html', {
            'bomgroup': companies,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'bomgroup': comp1}
        data['html_bomgroup_form'] = render_to_string('cmms/bomgroup/partialBOMGroupDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def bomgroup_create(request):
    if (request.method == 'POST'):
        form = BOMGroupForm(request.POST)
        return save_bomgroup_form(request, form, 'cmms/bomgroup/partialBOMGroupCreate.html')
    else:
        bomgroupInstance=BOMGroup.objects.create()
        form = BOMGroupForm(instance=bomgroupInstance)
        return save_bomgroup_form(request, form, 'cmms/bomgroup/partialBOMGroupCreate.html',bomgroupInstance.id)




##########################################################
def bomgroup_update(request, id):
    company= get_object_or_404(BOMGroup, id=id)
    template=""
    if (request.method == 'POST'):
        form = BOMGroupForm(request.POST, instance=company)
    else:
        form = BOMGroupForm(instance=company)
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)
    logging.debug(id)

    return save_bomgroup_form(request, form,"cmms/bomgroup/partialBOMGroupUpdate.html",id)
##########################################################

##########################################################
def bomgroupCancel(request,id):
    data=dict()
    tg=BOMGroup.objects.get(id=id)
    if(tg):
        if(not tg.name):
            tg.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            companies =  BOMGroup.objects.all().order_by('BOMGroupName')
            companies=AssetUtility.doPaging(request,companies)
            #Tasks.objects.filter(taskGroupId=id).update(taskGroup=id)
            data['html_bomgroup_list'] = render_to_string('cmms/bomgroup/partialBOMGrouplist.html', {
                'bomgroup': companies
            })

    return JsonResponse(data)
