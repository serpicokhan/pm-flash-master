'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neringAmarbject.OrderId.id)
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

from cmms.models import RingAmar
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import RingAmarForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
from rest_framework import status
from cmms.business.amarutility import AmarUtility
from cmms.business.DateJob import *
@permission_required('cmms.view_ringamar')
def list_ringAmar(request,id=None):
    #
    books = RingAmar.objects.all()
    wo=AmarUtility.doPaging(request,books)

    assetMakan=Asset.objects.filter(assetTypes=1,assetIsLocatedAt__isnull=True)
    return render(request, 'cmms/ringamar/ringAmarList.html', {'ringAmar': wo,'section':'list_ringAmar','makan':assetMakan})


##########################################################

def save_ringAmar_form(request, form, template_name,id=None,cnn=None):


    data = dict()
    if (request.method == 'POST'):
        print("here!")
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = RingAmar.objects.all()
            wo=AmarUtility.doPaging(request,books)
            data['html_ringAmar_list'] = render_to_string('cmms/ringamar/partialRingAmarList.html', {
                'ringAmar': wo,
                'perms': PermWrapper(request.user)
            })
        else:
            data['form_is_valid'] = False
            print(form.errors)
            # for err in form.errors:
            #     if(err.contains("already exists")):
            #         print("error")


    else:
        print(form.errors)
    if(cnn):
        context = {'form': form,'assetName2':cnn}
    else:
        context = {'form': form}


    data['html_ringAmar_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def ringAmar_delete(request, id):
    comp1 = get_object_or_404(RingAmar, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  RingAmar.objects.all()
        #Tasks.objects.filter(ringAmarId=id).update(ringAmar=id)
        data['html_ringAmar_list'] = render_to_string('cmms/ringamar/partialRingAmarList.html', {
            'ringAmar': companies,
            'perms': PermWrapper(request.user)
        })
    else:
        context = {'ringAmar': comp1}
        data['html_ringAmar_form'] = render_to_string('cmms/ringamar/partialRingAmarDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def ringAmar_create(request):
    if (request.method == 'POST'):
        form = RingAmarForm(DateJob.clean_ringamar(request))
        # form = RingAmarForm(request.POST)
        return save_ringAmar_form(request, form, 'cmms/ringamar/partialRingAmarCreate.html')
    else:
        asset=request.GET.get("q",False)
        assetName2=Asset.objects.filter(assetIsLocatedAt__id=asset)
        # print(assetName2.count())
        form = RingAmarForm(initial={'makan':'dsds'})
        return save_ringAmar_form(request, form, 'cmms/ringamar/partialRingAmarCreate.html',cnn=assetName2)




##########################################################
def ringAmar_update(request, id):
    company= get_object_or_404(RingAmar, id=id)
    template=""
    if (request.method == 'POST'):
        form = RingAmarForm(request.POST, instance=company)
    else:
        form = RingAmarForm(instance=company)


    return save_ringAmar_form(request, form,"cmms/ringamar/partialRingAmarUpdate.html",id)
##########################################################

##########################################################
