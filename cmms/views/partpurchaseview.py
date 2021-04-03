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
from cmms.business.DateJob import *
from cmms.models.parts import *
from cmms.models.stock import *
from cmms.models.purchase import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PartPurchaseForm

###################################################################
def list_partPurchase(request,id=None):
    books = PartPurchase.objects.all().order_by(-id)
    return render(request, 'cmms/part_purchase/partPurchaseList.html', {'partPurchases': books})


###################################################################
def js_list_partPurchase(request,woId):
    data=dict()
    books=PartPurchase.objects.filter(purchasePartId=woId).order_by('-purchaseDateOrdered')

    data['html_partPurchase_list']= render_to_string('cmms/part_purchase/partialPartPurchaseList.html', {
        'partPurchases': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_partPurchase_form(request, form, template_name,woId=None):
        data = dict()


        if (request.method == 'POST'):


              if form.is_valid():

                form.save()
                # stock=Stock.objects.filter(stockItem=form.instance.purchasePartId,location=form.instance.purchaseStock)[0]
                # wo=[]
                # if(not stock):
                #     wo=Stock.objects.create(stockItem=form.instance.purchasePartId,location=form.instance.purchaseStock,qtyOnHand=form.instance.purchaseQuantityReceived,minQty=0)
                # else:
                #     stock.qtyOnHand=stock.qtyOnHand+form.instance.purchaseQuantityReceived
                #     stock.save()
                #######update part price
                wp=Part.objects.get(pk=form.instance.purchasePartId.id)
                print(wp,"###########")
                wp.partLastPrice=1000
                print(wp.partLastPrice,"###################")
                wp.save()
                ########################

                data['form_is_valid'] = True

                books = PartPurchase.objects.filter(purchasePartId=woId).order_by('-purchaseDateOrdered')
                stks=Stock.objects.filter(stockItem=form.instance.purchasePartId,location=form.instance.purchaseStock)
                data['html_partPurchase_list'] = render_to_string('cmms/part_purchase/partialPartPurchaseList.html', {
                    'partPurchases': books,

                })
                data['html_partStock_list'] = render_to_string('cmms/part_stock/partialPartStocklist.html', {
                    'partStocks': stks
                })
              else:
                  fmt = getattr(settings, 'LOG_FORMAT', None)
                  lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
                  logging.basicConfig(format=fmt, level=lvl)
                  logging.debug(form.errors)
                  print("#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        context = {'form': form}
        data['html_partPurchase_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

###################################################################

@csrf_exempt
def partPurchase_delete(request, id):
    comp1 = get_object_or_404(PartPurchase, id=id)
    data = dict()
    stck=Stock.objects.none()
    woId=comp1.purchasePartId

    if (request.method == 'POST'):
        try:
            stck=Stock.objects.get(stockItem=comp1.purchasePartId,location=comp1.purchaseStock)
            stck.qtyOnHand=stck.qtyOnHand-comp1.purchaseQuantityReceived
            stck.save()
        except Stock.DoesNotExist:
            stock.create(stockItem=comp1.purchasePartId,location=comp1.purchaseStock,qtyOnHand=0)
        comp1.delete()

        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = PartPurchase.objects.filter(purchasePartId=woId).order_by('-purchaseDateOrdered')
        data['html_partPurchase_list'] = render_to_string('cmms/part_purchase/partialPartPurchaseList.html', {
            'partPurchases': companies
        })
    else:
        context = {'partPurchase': comp1}
        data['html_partPurchase_form'] = render_to_string('cmms/part_purchase/partialPartPurchaseDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def partPurchase_create(request):
    woId=-1

    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['purchasePartId']=body['purchasePartId']
        data['purchaseDateOrdered']=DateJob.getDate2(body['purchaseDateOrdered'])
        data['purchasePriceTotla']=body['purchasePriceTotla']

        data['purchaseCurrency']=body['purchaseCurrency']
        data['purchaseDateRecieved']=DateJob.getDate2(body['purchaseDateRecieved'])
        data['purchaseDateofExpire']=DateJob.getDate2(body['purchaseDateofExpire'])
        data['purchasedFrom']=body['purchasedFrom']
        data['purchaseUser']=body['purchaseUser']
        data['purchasePricePerUnit']=body['purchasePricePerUnit']
        data['purchaseStock']=body['purchaseStock']
        data['purchaseQuantityReceived']=body['purchaseQuantityReceived']
        # data['prevQNTY']=0





        woId=body['purchasePartId']



        form = PartPurchaseForm(data)



    else:
        form = PartPurchaseForm()

    return save_partPurchase_form(request, form, 'cmms/part_purchase/partialPartPurchaseCreate.html',woId)
###################################################################

@csrf_exempt
def partPurchase_update(request, id):
    company= get_object_or_404(PartPurchase, id=id)
    woId=company.purchasePartId
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['purchasePartId']=body['purchasePartId']
        data['purchaseDateOrdered']=DateJob.getDate2(body['purchaseDateOrdered'])
        data['purchasePriceTotla']=body['purchasePriceTotla']

        data['purchaseCurrency']=body['purchaseCurrency']
        data['purchaseDateRecieved']=DateJob.getDate2(body['purchaseDateRecieved'])
        data['purchaseDateofExpire']=DateJob.getDate2(body['purchaseDateofExpire'])
        data['purchasedFrom']=body['purchasedFrom']
        data['purchaseUser']=body['purchaseUser']
        data['purchasePricePerUnit']=body['purchasePricePerUnit']
        data['purchaseStock']=body['purchaseStock']
        data['purchaseQuantityReceived']=body['purchaseQuantityReceived']
        # data['prevQNTY']=body['prevQNTY']

        form = PartPurchaseForm(data, instance=company.purchaseQuantityReceived)
    else:
        # form = PartPurchaseForm(instance=company,initial={'prevQNTY':company.})
        form = PartPurchaseForm(instance=company)
    return save_partPurchase_form(request, form, 'cmms/part_purchase/partialPartPurchaseUpdate.html',woId)
