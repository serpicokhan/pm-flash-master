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
from cmms.models.workorder import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import WoPartForm
from cmms.models.parts import *
from cmms.business.stockutility import *
from cmms.utils import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from rest_framework.decorators import api_view
from cmms.api.WOSerializer import *
from rest_framework.response import Response
from django.db import IntegrityError
from cmms.models.Asset import *

###################################################################
def list_woPart(request,id=None):
    books = WorkorderPart.objects.all()
    return render(request, 'cmms/workorder_parts/woPartList.html', {'woParts': books})
###################################################################
@permission_required('cmms.view_workorderpart')
def js_list_woPart(request,woId):
    data=dict()
    query="select id as id,woPartWorkorder_id,sum(woPartActulaQnty) as woPartActulaQnty,sum(woPartPlannedQnty) as woPartPlannedQnty from workorderpart where  woPartWorkorder_id={} group by woPartWorkorder_id,woPartPart_id".format(woId)
    books=WorkorderPart.objects.filter(woPartWorkorder=woId)

    data['html_woPart_list']= render_to_string('cmms/workorder_parts/partialWoPartList.html', {
        'woParts': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)
###################################################################    ###################################################################
@csrf_exempt
def save_woPart_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            # stockMsg=StockUtility.remove(form.instance)
            ########################Message handling for part available in stock#################
            # if(stockMsg==WOPartMsg.Success):
            #   data['html_woPart_list_success']=str(stockMsg.value)
            # elif(stockMsg==WOPartMsg.NotEnouphPart):
            #     # form.instance.woPartActulaQnty=0
            #     #form.save()
            #     data['html_woPart_list_error']=str(stockMsg.value)
            #     data['html_woPart_wo_status']=woStatus['waitingforparts']
            # else:
            #     pass


            form.save()
            data['form_is_valid'] = True
            data['html_woPart_list_success']='با موفقیت قطعه درخواست شد'
           
            # query="select id as id,woPartWorkorder_id,sum(woPartActulaQnty) as woPartActulaQnty,sum(woPartPlannedQnty) as woPartPlannedQnty from workorderpart where  woPartWorkorder_id={} group by woPartWorkorder_id,woPartPart_id".format(woId)
            # print(query)
            books = WorkorderPart.objects.filter(woPartWorkorder=woId)
            data['html_woPart_list'] = render_to_string('cmms/workorder_parts/partialWoPartList.html', {
                'woParts': books,
                'perms': PermWrapper(request.user)
            })
            ########################################################
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)
              if("not unique" in form.errors):
                      data["html_woPart_list_error"]="قطعه تکراری"

    context = {'form': form}
    data['html_woPart_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def woPart_delete(request, id):
    comp1 = get_object_or_404(WorkorderPart, id=id)
    data = dict()
    woId=comp1.woPartWorkorder

    if (request.method == 'POST'):
        StockUtility.add(comp1.woPartStock,comp1.woPartActulaQnty)
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = WorkorderPart.objects.filter(woPartWorkorder=woId)
        data['html_woPart_list'] = render_to_string('cmms/workorder_parts/partialWoPartList.html', {
            'woParts': companies,
            'perms':PermWrapper(request.user)
        })
    else:
        context = {'woPart': comp1}
        data['html_woPart_form'] = render_to_string('cmms/workorder_parts/partialWoPartDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woPart_create(request,id=None):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)
    logging.debug( "dasdsadasdsa")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['woPartWorkorder']=body['woPartWorkorder']
        # data['woPartPart']=body['woPartPart']
        data['woPartPlannedQnty']=body['woPartPlannedQnty']
        data['woPartActulaQnty']=body['woPartActulaQnty']
        data['woPartStock']=body['woPartStock']
        woId=body['woPartWorkorder']
        form = WoPartForm(data=data)
    else:
        form = WoPartForm()
    return save_woPart_form(request, form, 'cmms/workorder_parts/partialWoPartCreate.html',woId)
###################################################################

@csrf_exempt
def woPart_update(request, id):

    company= get_object_or_404(WorkorderPart, id=id)

    woId=company.woPartWorkorder
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()
        data['woPartWorkorder']=body['woPartWorkorder']
        # data['woPartPart']=body['woPartPart']
        data['woPartPlannedQnty']=body['woPartPlannedQnty']
        data['woPartActulaQnty']=body['woPartActulaQnty']
        data['woPartStock']=body['woPartStock']
        form = WoPartForm(data=data, instance=company)
    else:
        form = WoPartForm(instance=company,initial={'mypart':company.woPartStock.stockItem})
    return save_woPart_form(request, form, 'cmms/workorder_parts/partialWoPartUpdate.html',woId.id)
@csrf_exempt
def woPart_Seach(request,name):
    result=Part.objects.filter(partName__contains=name);
    data=dict()

    data['woPartSearchResult'] = render_to_string('cmms/workorder_parts/partialWoSearchResult.html', {
        'woParts': result
    })
    
    return JsonResponse(data)
#############################
def wo_getParts(request):
    # print(request.GET['q'])
    searchStr= request.GET['qry'] if request.GET['qry'] else ''
    x=list(PartUtility.getParts(searchStr))
    # if(len(x)==0):
    #     print("dasdsa")
    #     x=[{'id':-1,'partName':'قطعه یافت نشد'}]


    # response_data = {}
    # response_data['result'] = '[dsadas,dasdasdas]'
    return JsonResponse(x, safe=False)
def wo_getStockParts(request):
    # print(request.GET['q'])
    searchStr= request.GET['qry'] if request.GET['qry'] else ''
    x=list(StockUtility.getStockParts(searchStr))
    # response_data = {}
    # response_data['result'] = '[dsadas,dasdasdas]'
    return JsonResponse(x, safe=False)
##############################
###used in wopart.js and
### fro finding coresponding stock to part
def wP_getPartStock(request,id):
    # print(request.GET['q'])
    x=dict()
    # x['result']=render_to_string('cmms/workorder_parts/partialWoSearchResult.html', {
    #     'woParts': result
    # })
    x['result']={'result':PartUtility.getPartStock(id)}
    # response_data = {}
    # response_data['result'] = '[dsadas,dasdasdas]'
    return JsonResponse(x)
def WoPart_search_form_set(request):
    q=request.GET.get("q",'')
    data=dict()
    if(len(q)>1):
        res=Stock.objects.filter(stockItem__partName__icontains=q)
        data['result']=render_to_string('cmms/workorder_parts/partialWoPartSearchResult.html', {
            'woParts': res
        })

    return JsonResponse(data)


def wo_AssetPartList(request,id):
    #id is wo id
    if(request.method=='GET'):
        # woPart=WorkOrderPart.objects.filter(woPartWorkorder=id)
        data=dict()
        woId=WorkOrder.objects.get(id=id).woAsset
        # print(woId)
        # print("here!!!!!!!!!!!!!")
        #books=AssetPart.objects.filter(assetPartAssetid=woId)
        # query="select id as id,assetPartAssetid_id,sum(assetPartQnty) as assetPartQnty from assetpart where  assetPartAssetid_id={} group by assetPartAssetid_id,AssetPartPid_id".format(woId)
        # query="select * from assetpart where assetPartAssetid_id={0}".format(woId)
        books2=BOMGroupPart.objects.filter(BOMGroupPartBOMGroup__in=
        BOMGroupAsset.objects.filter(BOMGroupAssetAsset=woId).values_list('BOMGroupAssetBOMGroup',flat=True)).order_by('BOMGroupPartPart__partName')

        books=AssetPart.objects.filter(assetPartAssetid=woId).order_by('assetPartPid__partName')
        all_books=[]
        #type =0 bom and type =1 assetpart
        for i in books2:
            all_books.append({'type':0,'bom':i})
        for i in books:
            all_books.append({'type':1,'bom':i})

        data['html_part_form']= render_to_string('cmms/workorder_parts/assetPartList.html', {
            'assetParts': all_books,
            
            'wo':id
        })
        data['form_is_valid']=True
        return JsonResponse(data)

def create_by_wo_part(request,wo,pid):
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data = request.POST.dict()
        data['woPartWorkorder']=body['woPartWorkorder']
        # data['woPartPart']=body['woPartPart']
        data['woPartPlannedQnty']=body['woPartPlannedQnty']
        data['woPartActulaQnty']=body['woPartActulaQnty']
        data['woPartStock']=body['woPartStock']
        woId=body['woPartWorkorder']
        form = WoPartForm(data=data)
    else:
        form = WoPartForm(initial={'mypart':'100'})
    return save_woPart_form(request, form, 'cmms/workorder_parts/partialWoPartCreate.html',wo)

def create_wo_part_from_bom(request,wo,pid,kid):
    #find stockitem from pid
    data=dict()
    try:
        stock_item=Stock.objects.filter(stockItem__id=pid,qtyOnHand__gt=0)[0]
    except:
        data['error']="در انبار یافت نشد"
        
    if(stock_item):
        x=WorkorderPart.objects.create(
            woPartWorkorder=WorkOrder.objects.get(id=wo),woPartPlannedQnty=1,woPartActulaQnty=1,woPartStock=stock_item
        )
        qty=stock_item.qtyOnHand - 1
        stock_item.qtyOnHand=qty
        stock_item.save()
        data["id"]=x.id
        data['form_is_valid'] = True
        data['html_woPart_list_success']='با موفقیت قطعه درخواست شد'
           
        # query="select id as id,woPartWorkorder_id,sum(woPartActulaQnty) as woPartActulaQnty,sum(woPartPlannedQnty) as woPartPlannedQnty from workorderpart where  woPartWorkorder_id={} group by woPartWorkorder_id,woPartPart_id".format(woId)
        # print(query)
        books = WorkorderPart.objects.filter(woPartWorkorder__id=wo)
        data['html_woPart_list'] = render_to_string('cmms/workorder_parts/partialWoPartList.html', {
                'woParts': books,
                'perms': PermWrapper(request.user)
            })

    else:
        data["error"]="not enoght quantity in hand"


    #create new wopart
    return JsonResponse(data)

@api_view(['GET'])
def wopart_collection(request,id):
    if request.method == 'GET':
        print("wopart reached")
        posts = WorkorderPart.objects.filter(woPartWorkorder=id)
        serializer = woPartSerializer(posts, many=True)

        return Response(serializer.data)
@api_view(['GET'])
def wopart_detail_collection(request,id):
    if request.method == 'GET':
        # print("!23")
        posts = WorkorderPart.objects.get(id=id)
        serializer = woPartSerializer(posts)

        return Response(serializer.data)
