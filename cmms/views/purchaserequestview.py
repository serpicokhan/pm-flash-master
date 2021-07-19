'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nepurchaseRequestbject.OrderId.id)
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

from cmms.models.purchaserequest import *
from cmms.models.users import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PurchaseRequestForm
from django.urls import reverse_lazy
from django.db import transaction



def list_purchaseRequest(request,id=None):
    #
    books = PurchaseRequest.objects.all()
    return render(request, 'cmms/purchase_request/purchaseRequestList.html', {'rfq': books})


##########################################################

def save_purchaseRequest_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save(commit=False)
            form.instance.PurchaseRequestRequestedUser=SysUser.objects.get(userId=request.user)
            form.save()
            data['form_is_valid'] = True
            books = PurchaseRequest.objects.all()
            data['html_purchaseRequest_list'] = render_to_string('cmms/purchase_request/partialPurchaseRequestList.html', {
                'rfq': books
            })
        else:
            data['form_is_valid'] = False
    title=None
    if(form.instance.PurchaseRequestRequestedUser):
            title=form.instance.PurchaseRequestRequestedUser.title

    context = {'form': form,'title':title}


    data['html_purchaseRequest_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def purchaseRequest_delete(request, id):
    comp1 = get_object_or_404(PurchaseRequest, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  PurchaseRequest.objects.all().order_by('name')
        #Tasks.objects.filter(purchaseRequestId=id).update(purchaseRequest=id)
        data['html_purchaseRequest_list'] = render_to_string('cmms/purchase_request/partialPurchaseRequestlist.html', {
            'purchaseRequest': companies
        })
    else:
        context = {'purchaseRequest': comp1}
        data['html_purchaseRequest_form'] = render_to_string('cmms/purchase_request/partialPurchaseRequestDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def purchaseRequest_create(request):
    if (request.method == 'POST'):
        form = PurchaseRequestForm(request.POST)
        return save_purchaseRequest_form(request, form, 'cmms/purchase_request/partialPurchaseRequestCreate.html')
    else:
        # purchaseRequestInstance=PurchaseRequest.objects.create()
        # form = PurchaseRequestForm(instance=purchaseRequestInstance)
        form = PurchaseRequestForm()
        return save_purchaseRequest_form(request, form, 'cmms/purchase_request/partialPurchaseRequestCreate.html')




##########################################################
def purchaseRequest_update(request, id):
    company= get_object_or_404(PurchaseRequest, id=id)
    template=""
    if (request.method == 'POST'):
        form = PurchaseRequestForm(request.POST, instance=company)
    else:
        form = PurchaseRequestForm(instance=company)
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)
    logging.debug(id)

    return save_purchaseRequest_form(request, form,"cmms/purchase_request/partialPurchaseRequestUpdate.html",id)
##########################################################

##########################################################
def purchaseRequestCancel(request,id):
    data=dict()
    # tg=PurchaseRequest.objects.get(id=id)
    # if(tg):
    #     if(not tg.name):
    #         tg.delete()
    #         data['form_is_valid'] = True  # This is just to play along with the existing code
    #         companies =  PurchaseRequest.objects.all().order_by('name')
    #         #Tasks.objects.filter(taskGroupId=id).update(taskGroup=id)
    #         data['html_purchaseRequest_list'] = render_to_string('cmms/purchaseRequest/partialPurchaseRequestlist.html', {
    #             'purchaseRequest': companies
    #         })

    return JsonResponse(data)
