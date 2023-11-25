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
from django.core.paginator import *
from cmms.business.UserUtility import *
from cmms.utils import *





def filter_user(request):
    if(request.user.username=="admin"):
        return PurchaseRequest.objects.all().order_by('-id')
    else:
        return PurchaseRequest.objects.filter(PurchaseRequestRequestedUser__userId=request.user).order_by('-id')
##########################################################
def list_purchaseRequest(request,id=None):
    #
    books1 = filter_user(request)
    books=doPaging(request,books1)

    return render(request, 'cmms/purchase_request/purchaseRequestList.html', {'rfq': books,'status':Status})
def list_purchaseRequest_v2(request,id=None):
    #
    books1 = filter_user(request)
    books=doPaging(request,books1)

    return render(request, 'cmms/purchase_main/purchaseList.html', {'rfq': books,'status':Status})

def save_purchaseRequest_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save(commit=False)
            if(not form.instance.PurchaseRequestStatus):
                form.instance.PurchaseRequestStatus=1;

            # form.instance.PurchaseRequestRequestedUser=SysUser.objects.get(userId=request.user)
            form.save()
            # print(form.instance.PurchaseRequestDateTo,"tarikh")
            data['form_is_valid'] = True

            books1 =filter_user(request)
            books=doPaging(request,books1)
            data['html_purchaseRequest_list'] = render_to_string('cmms/purchase_request/partialPurchaseRequestList.html', {
                'rfq': books
            })
        else:
            data['form_is_valid'] = False
    title=None
    if(form.instance.PurchaseRequestRequestedUser):
            title=form.instance.PurchaseRequestRequestedUser

    context = {'form': form,'title':title,'is_manager':UserUtility.is_manager(request.user)}


    data['html_purchaseRequest_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def purchaseRequest_delete(request, id):
    comp1 = get_object_or_404(PurchaseRequest, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        # companies =  PurchaseRequest.objects.all().order_by('-id')
        books1 =filter_user(request)
        books=doPaging(request,books1)
        #Tasks.objects.filter(purchaseRequestId=id).update(purchaseRequest=id)
        data['html_purchaseRequest_list'] = render_to_string('cmms/purchase_request/partialPurchaseRequestList.html', {
            'rfq': books
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
        form = PurchaseRequestForm(request.user,request.POST)
        return save_purchaseRequest_form(request, form, 'cmms/purchase_request/partialPurchaseRequestCreate.html')
    else:
        form = PurchaseRequestForm(userid=request.user)
        return save_purchaseRequest_form(request, form, 'cmms/purchase_request/partialPurchaseRequestCreate.html')




##########################################################
def purchaseRequest_update(request, id):
    company= get_object_or_404(PurchaseRequest, id=id)
    template=""
    if (request.method == 'POST'):
        form = PurchaseRequestForm(request.user,request.POST, instance=company)
    else:
        form = PurchaseRequestForm(instance=company,userid=request.user,initial={'mypart':company.PurchaseRequestPartName.partName})


    return save_purchaseRequest_form(request, form,"cmms/purchase_request/partialPurchaseRequestUpdate.html",id)
##########################################################

##########################################################
def purchaseRequestCancel(request,id):
    data=dict()

    return JsonResponse(data)

def doPaging(request,books):
    page=request.GET.get('page',1)
    paginator = Paginator(books, 10)
    wos=None
    try:
        wos=paginator.page(page)
    except PageNotAnInteger:
        wos = paginator.page(1)
    except EmptyPage:
        wos = paginator.page(paginator.num_pages)
    return wos
def purchaseRequest_filter(request):
    q=request.GET.get("q",None)
    if(q):
        books1 = filter_user(request)
        books1=books1.filter(PurchaseRequestStatus=int(q))
        books=doPaging(request,books1)
        return render(request, 'cmms/purchase_request/purchaseRequestList.html', {'rfq': books,'status':Status,'selected':int(q)})
