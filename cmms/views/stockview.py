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
from cmms.business.stockutility import *

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import StockForm
from django.db.models import F
###################################################################
def list_stock(request,id=None):

    books = Stock.objects.all().order_by('stockItem')
    wos=StockUtility.doPaging(request,books)
    q=Asset.objects.filter(assetIsStock=True)
    return render(request, 'cmms/stock/stockList.html', {'stocks': wos,'anbar':q})

###################################################################
def list_lowItemStock(request,id=None):
    books = Stock.objects.filter(qtyOnHand__lt=F('minQty'))
    return render(request, 'cmms/stock/dash_stockList.html', {'stocks': books})
def get_lowItemStock(request,id=None):
    data=dict()
    books = Stock.objects.filter(qtyOnHand__lt=F('minQty'))
    data['form_is_valid']=True
    print("low is low",len(books))
    data['html_lowitemstock_list'] = render_to_string('cmms/stock/partialStockList.html', {
                  'stocks': list(books),
              })
    return JsonResponse(data)


###################################################################
def js_list_stock(request,woId=None):
    data=dict()
    if(woId):
        books=Stock.objects.all()

    else:
        books=Stock.objects.filter(stockItem=woId)
    wos=StockUtility.doPaging(request,books)



    data['html_stock_list']= render_to_string('cmms/stock/partialStockList.html', {
        'stocks': wos
    })
    data['form_is_valid']=True
    return JsonResponse(data)
def js_list_modal_stock(request):
    data=dict()

    books=Stock.objects.all()






    data['html_stock_list']= render_to_string('cmms/stock/partialModalStockList.html', {
        'stocks': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)


def js_list_all_stock(request):
    data=dict()

    books=Stock.objects.all().order_by('stockItem')


    wos=StockUtility.doPaging(request,books)



    data['html_stock_list']= render_to_string('cmms/stock/partialStockList.html', {
        'stocks': wos
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
#test var is used for diffrentiate betwwen part stock call and stock call (both use same view)
def save_stock_form(request, form, template_name,woId=None,test=None,isupdating=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            if(not StockUtility.have_Prev_val(form.instance) or isupdating):
                form.save()
                data['form_is_valid'] = True
                data['html_success']="موجودی با موفقیت تغییر یافت"


                if(not test):
                    print("here!!!!!!!!")
                    books=Stock.objects.all().order_by('stockItem')
                else:
                    books=Stock.objects.filter(stockItem=woId)
                wos=StockUtility.doPaging(request,books)
                data['html_stock_list'] = render_to_string('cmms/stock/partialStockList.html', {
                    'stocks': wos
                })
            else:
                print("something is wrong here!")
                data['form_is_valid'] = False
                data['stock_has_err']=1
                data['stock_err_msg']="ورودی های خود را کنترل نمایید"

          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_stock_form'] = render_to_string(template_name, context, request=request)
    # print("here!")
    return JsonResponse(data)
###################################################################
@csrf_exempt
#test var is used for diffrentiate betwwen part stock call and stock call (both use same view)
def save2_stock_form(request, form, template_name,woId=None,test=None,isupdating=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            if(not StockUtility.have_Prev_val(form.instance) or isupdating):
                form.save()
                data['form_is_valid'] = True
                data['html_success']="موجودی با موفقیت تغییر یافت"


                if(not test):
                    print("here!!!!!!!!")
                    books=Stock.objects.all().order_by('stockItem')
                else:
                    books=Stock.objects.filter(stockItem=woId)
                # wos=StockUtility.doPaging(request,books)
                data['html_stock_list'] = render_to_string('cmms/stock/partialStockListModal.html', {
                    'stocks': books
                })
            else:
                print("something is wrong here!")
                data['form_is_valid'] = False
                data['stock_has_err']=1
                data['stock_err_msg']="ورودی های خود را کنترل نمایید"

          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_stock_form'] = render_to_string(template_name, context, request=request)
    # print("here!")
    return JsonResponse(data)
###################################################################


def stock_delete(request, id):
    comp1 = get_object_or_404(Stock, id=id)
    data = dict()

    if (request.method == 'POST'):
        comp1.delete()
        print("good")
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = Stock.objects.all().order_by('stockItem')
        wos=StockUtility.doPaging(request,companies)
        data['html_stock_list'] = render_to_string('cmms/stock/partialStockList.html', {
            'stocks': wos
        })
        data['html_success']="موجودی با موفقیت حذف شد"
    else:


        context = {'stock': comp1}
        data['html_stock_form'] = render_to_string('cmms/stock/partialStockDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def stock_create(request):
    woId=-1
    test=0

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
        if('test' in body):
            test=True
        else:
            test=False

        woId=body['stockItem']

        form = StockForm(data)

    else:
        form = StockForm()
    return save_stock_form(request, form, 'cmms/stock/partialStockCreate.html',woId,test,False)
@csrf_exempt
def stock_create2(request):
    woId=-1
    test=0

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
        if('test' in body):
            test=True
        else:
            test=False

        woId=body['stockItem']

        form = StockForm(data)

    else:
        form = StockForm()
    return save2_stock_form(request, form, 'cmms/stock/partialStockCreate2.html',woId,test,False)
###################################################################

@csrf_exempt
def stock_update(request, id):
    test=0
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
        if('test' in body):
            test=True
        else:
            test=False
        form = StockForm(data, instance=company)
    else:
        form = StockForm(instance=company,initial={'mypart':company.stockItem.partName})
    return save_stock_form(request, form, 'cmms/stock/partialStockUpdate.html',woId,test,True)

def groupByStockLocation(request,locationId):
    data=dict()

    q=""
    if(locationId==-1):
        data['form_is_valid']=False
    q=Stock.objects.filter(location=locationId)

    wos=StockUtility.doPaging(request,q)
    data['form_is_valid']=True
    data['html_stock_list'] = render_to_string('cmms/stock/partialStockList.html', {       'stocks': q      })
    # data['html_stock_page']=render_to_string('cmms/stock/partialStockList.html', {       '': q      })
    data['html_stock_paginator'] = render_to_string('cmms/stock/partialStockPagination.html', {               'wo': wos,'pageType':'group_by_stock_location'  ,'pageArgs':  locationId                   })
    return JsonResponse(data)
############################################
### get stock consume item in wo in stockslistdetail.html
def getConsumedItem(request,stockId,num):
    data=dict()
    wos=StockUtility.getConsumeInfo(stockId,num)
    data['form_is_valid']=True
    # data['html_stock_page']=render_to_string('cmms/stock/partialStockList.html', {       '': q      })
    data['html_stock_list'] =render_to_string('cmms/stock/consumedstockresult.html', {
        'wos': wos
    })
    return JsonResponse(data)
### get stock purchased history item in wo in stockslistdetail.html
def getPurchasedItem(request,stockId,num):
    data=dict()
    wos=StockUtility.getPurchasedInfo(stockId,num)
    data['form_is_valid']=True
    # data['html_stock_page']=render_to_string('cmms/stock/partialStockList.html', {       '': q      })
    data['html_stock_list'] =render_to_string('cmms/stock/purchasestockresult.html', {
        'wos': wos
    })
    return JsonResponse(data)
def stockSearch(request,searchStr):
    data=dict()
    searchStr=searchStr.replace('empty_','')
    searchStr=searchStr.replace('_',' ')
    books=list(StockUtility.seachStock(searchStr))
    if(not searchStr):
        searchStr='empty_'
    # print(searchStr)
    wos=StockUtility.doPaging(request,books)
    data['html_stock_list'] = render_to_string('cmms/stock/partialStockList.html', {               'stocks': wos                       })

    data['html_stock_paginator'] = render_to_string('cmms/stock/partialStockPagination.html', {'wo': wos,'pageType':'stockSearch','pageArgs':searchStr})
    data['form_is_valid'] = True
    return JsonResponse(data)
def stockSearch2(request,searchStr):
    data=dict()
    searchStr=searchStr.replace('empty_','')
    searchStr=searchStr.replace('_',' ')
    books=list(StockUtility.seachStock(searchStr))
    if(not searchStr):
        searchStr='empty_'
    # print(searchStr)
    # wos=StockUtility.doPaging(request,books)
    data['html_stock_list'] = render_to_string('cmms/stock/partialStockListModal.html', {               'stocks': books                       })

    # data['html_stock_paginator'] = render_to_string('cmms/stock/partialStockPagination.html', {'wo': wos,'pageType':'stockSearch','pageArgs':searchStr})
    data['form_is_valid'] = True
    return JsonResponse(data)
