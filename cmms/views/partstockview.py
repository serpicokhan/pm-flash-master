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
from cmms.models.stock import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import PartStockForm

###################################################################
def list_partStock(request,id=None):
    books = Stock.objects.all()
    return render(request, 'cmms/part_stock/partStockList.html', {'partStocks': books})


###################################################################
def js_list_partStock(request,woId):
    data=dict()
    books=Stock.objects.filter(stockItem=woId)

    data['html_partStock_list']= render_to_string('cmms/part_stock/partialPartStockList.html', {
        'partStocks': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_partStock_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = Stock.objects.filter(stockItem=woId)
            data['html_partStock_list'] = render_to_string('cmms/part_stock/partialPartStockList.html', {
                'partStocks': books
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_partStock_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def partStock_delete(request, id):
    comp1 = get_object_or_404(Stock, id=id)
    data = dict()
    woId=comp1.stockItem

    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = Stock.objects.filter(stockItem=woId)
        data['html_partStock_list'] = render_to_string('cmms/part_stock/partialPartStockList.html', {
            'partStocks': companies
        })
    else:
        context = {'partStock': comp1}
        data['html_partStock_form'] = render_to_string('cmms/part_stock/partialPartStockDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def partStock_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)
    logging.debug( "dasdsadasdsa")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        data['stockItem']=body['stockItem']
        data['location']=body['location']
        data['qtyOnHand']=body['qtyOnHand']
        data['minQty']=body['minQty']
        data['aisle']=body['aisle']
        data['row']=body['row']
        data['bin']=body['bin']

        woId=body['stockItem']

        form = PartStockForm(data)

    else:
        form = PartStockForm()
    return save_partStock_form(request, form, 'cmms/part_stock/partialPartStockCreate.html',woId)
###################################################################

@csrf_exempt
def partStock_update(request, id):
    company= get_object_or_404(Stock, id=id)
    woId=company.stockItem
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['stockItem']=body['stockItem']
        data['location']=body['location']
        data['qtyOnHand']=body['qtyOnHand']
        data['minQty']=body['minQty']
        data['aisle']=body['aisle']
        data['row']=body['row']
        data['bin']=body['bin']
        form = PartStockForm(data, instance=company)
    else:
        form = PartStockForm(instance=company)
    return save_partStock_form(request, form, 'cmms/part_stock/partialPartStockUpdate.html',woId)
