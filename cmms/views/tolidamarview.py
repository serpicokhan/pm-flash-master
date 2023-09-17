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

from cmms.models import TolidAmar,TolidMoshakhase
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
from django.db.models import Max
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
# from openpyxl import Workbook
# from openpyxl.utils.dataframe import dataframe_to_rows
# import pandas as pd
@permission_required('cmms.view_ringamar')
def list_tolidAmar(request,id=None):
    #
    books = TolidAmar.objects.none()
    # wo=AmarUtility.doPaging(request,books)

    assetMakan=Asset.objects.filter(assetTypes=1,assetIsLocatedAt__isnull=True)
    return render(request, 'cmms/tolidamar/tolidAmarList.html', {'ringAmar': books,'section':'list_tolidAmar','makan':assetMakan})


# ##########################################################
#
# def save_ringAmar_form(request, form, template_name,id=None,cnn=None):
#
#
#     data = dict()
#     if (request.method == 'POST'):
#         if form.is_valid():
#             form.save(commit=False)
#             form.instance.userRegisterd=SysUser.objects.get(userId=request.user)
#             form.save()
#             data['form_is_valid'] = True
#             books = RingAmar.objects.all()
#             wo=AmarUtility.doPaging(request,books)
#             data['html_ringAmar_list'] = render_to_string('cmms/ringamar/partialRingAmarList.html', {
#                 'ringAmar': wo,
#                 'perms': PermWrapper(request.user)
#             })
#         else:
#             data['form_is_valid'] = False
#             print(form.errors)
#             # for err in form.errors:
#             #     if(err.contains("already exists")):
#             #         print("error")
#
#
#     else:
#         print(form.errors)
#     if(cnn):
#         context = {'form': form,'assetName2':cnn}
#     else:
#         context = {'form': form}
#
#
#     data['html_ringAmar_form'] = render_to_string(template_name, context, request=request)
#     return JsonResponse(data)
# ##########################################################
#
#
# def ringAmar_delete(request, id):
#     comp1 = get_object_or_404(RingAmar, id=id)
#     data = dict()
#     if (request.method == 'POST'):
#         comp1.delete()
#         data['form_is_valid'] = True  # This is just to play along with the existing code
#         companies =  RingAmar.objects.all()
#         #Tasks.objects.filter(ringAmarId=id).update(ringAmar=id)
#         data['html_ringAmar_list'] = render_to_string('cmms/ringamar/partialRingAmarList.html', {
#             'ringAmar': companies,
#             'perms': PermWrapper(request.user)
#         })
#     else:
#         context = {'ringAmar': comp1}
#         data['html_ringAmar_form'] = render_to_string('cmms/ringamar/partialRingAmarDelete.html',
#             context,
#             request=request,
#         )
#     return JsonResponse(data)
#
# ##########################################################
#
# ##########################################################
# def ringAmar_create(request):
#     if (request.method == 'POST'):
#         form = RingAmarForm(DateJob.clean_ringamar(request))
#         # form = RingAmarForm(request.POST)
#         return save_ringAmar_form(request, form, 'cmms/ringamar/partialRingAmarCreate.html')
#     else:
#         asset=request.GET.get("q",False)
#         assetName2=Asset.objects.filter(assetIsLocatedAt__id=asset)
#         # print(assetName2.count())
#         form = RingAmarForm(initial={'makan':'dsds'})
#         return save_ringAmar_form(request, form, 'cmms/ringamar/partialRingAmarCreate.html',cnn=assetName2)
#
#
#
#
# ##########################################################
# def ringAmar_update(request, id):
#     company= get_object_or_404(RingAmar, id=id)
#     template=""
#     if (request.method == 'POST'):
#         form = RingAmarForm(DateJob.clean_ringamar(request),instance=company)
#         # form = RingAmarForm(request.POST, instance=company)
#     else:
#         asset=request.GET.get("q",False)
#         assetName2=Asset.objects.filter(assetIsLocatedAt__id=asset)
#         form = RingAmarForm(instance=company)
#         return save_ringAmar_form(request, form,"cmms/ringamar/partialRingAmarUpdate.html",id,cnn=assetName2)
#
#
#     return save_ringAmar_form(request, form,"cmms/ringamar/partialRingAmarUpdate.html",id)
# ##########################################################
def getAmarTolidMoshakhase(request):
    data=dict()
    qry=request.GET.get("qry",False)
    if(qry):
        results=TolidMoshakhase.objects.filter(mogheiat=qry)
        if(results.count()>0):
            data["result"]={'mogheiat':results[0].mogheiat,'keifiat':results[0].keyfiat,'id':results[0].id,'vaziat':results[0].vaziat}
        else:
            data["result"]={}
        return JsonResponse(data, safe=False)
    return data
# ##########################################################
# def get_max_kilometer(request):
#     data=dict()
#     # max_value = MyModel.objects.aggregate(max_value=Max('my_field'))['max_value']
#     # max=Ama
#     asset=request.GET.get("asset_id",0)
#     print(asset)
#     shift=request.GET.get("shift",0)
#     date=request.GET.get("date",0)
#     date=DateJob.getTaskDate(date)
#     # data["x"]=RingAmar.objects.filter(assetName=asset).aggregate(max_value=Max('assetEndKilometer'))['max_value']
#     id=[]
#     id.append(RingAmar.objects.filter(assetName=asset).aggregate(max_value=Max('id'))['max_value'])
#     flag=True
#     data["x"]=0
#     while(data["x"]==0):
#         id1=RingAmar.objects.exclude(assetName=asset,id__in=id).filter(assetName=asset).aggregate(second_max=Max('id'))['second_max']
#
#         data["x"]=RingAmar.objects.get(id=id1).assetEndKilometer
#         # RingAmar.objects.filter(assetName=asset, id=RingAmar.objects.filter(assetName=asset).aggregate(Max('id'))['id__max']).first().assetEndKilometer
#         # print(data,asset,id)
#         id.append(id1)
#     return JsonResponse(data)
# def get_max_time(request):
#     data=dict()
#     # max_value = MyModel.objects.aggregate(max_value=Max('my_field'))['max_value']
#     # max=Ama
#     asset=request.GET.get("asset_id",0)
#     print(asset)
#     shift=request.GET.get("shift",0)
#     date=request.GET.get("date",0)
#     date=DateJob.getTaskDate(date)
#     data["x"]=RingAmar.objects.filter(assetName=asset).aggregate(max_value=Max('assetEndTime'))['max_value']
#     return JsonResponse(data)
#
#
def loadAmarTolidTableInfo(request):
    makan=request.GET.get("makan",False)
    dt=request.GET.get("dt",False)
    date1=DateJob.getTaskDate(dt)
    data=dict()
    x1=''
    y1=''
    if(makan):
        amar=TolidAmar.objects.filter(location=makan,registered_date=date1).order_by('registered_date')
        location=Asset.objects.get(id=makan)

        if(amar.count()==0):
            amar=[]


            j=TolidAmar.objects.create(location=location,registered_date=date1,tedad=0,meghdar=0)
            amar.append(j)
                # data['amar']= render_to_string('cmms/tolidamar/partialRingAmarList2.html', {
                # 'dt':dt,
                # 'date':date1,
                # 'makan':makan,
                # 'makan_id':location.id,
                # 'perms': PermWrapper(request.user)})

            data['amar']= render_to_string('cmms/tolidamar/partialRingAmarList2.html', {
            'tolidAmar': amar,
            'perms': PermWrapper(request.user),

        })
        data['amar']= render_to_string('cmms/tolidamar/partialRingAmarList2.html', {
        'tolidAmar': amar,
        'perms': PermWrapper(request.user)
        })

        data['form_is_valid']=True

    return JsonResponse(data)
@csrf_exempt
def saveAmarTolidTableInfo(request):
    # print(request.body)
    # print(request.POST)
    data = json.loads(request.body)
    dt={}
    print("********")
    for i in data:
        # print("********")


        if('id' in i):

            moshakhase=0
            if(int(i['id'])!=-1):
                print(i['radif'],i['tolidmoshakhase'])
                if(int(i['tolidmoshakhase'])==0):
                        print("here!",i['vaziat_text'])
                        nakh_obj=TolidMoshakhase.objects.create(mogheiat=i['vaziat_text'],keyfiat=i['keyfiat'],vaziat=i['mogheiat'])
                        moshakhase=nakh_obj.id
                        print(nakh_obj)
                else:
                    moshakhase=i['tolidmoshakhase']


            # -2 show new row and -1 represent header row which is not contain ant information
            if(i['id']!='-2'):

                if(int(i['id'])!=-1):
                    print(i['isheatset'])
                    amar=TolidAmar.objects.get(id=i['id'])
                    amar.tolidmoshakhase=TolidMoshakhase.objects.get(id=moshakhase)
                    amar.registered_date=i["registered_date"].replace('/','-')
                    amar.tedad=float(i["tedad"])
                    amar.meghdar=float(i["meghdar"])
                    amar.location=Asset.objects.get(id=i["location"])
                    amar.isheatset=i['isheatset']
                    amar.save()

            #-2 show new row
            if(i['id']=='-2'):
                print(moshakhase)
                isheatset=i['isheatset']
                newRow=TolidAmar.objects.create(tolidmoshakhase=TolidMoshakhase.objects.get(id=moshakhase),registered_date=i["registered_date"].replace('/','-'),tedad=int(i["tedad"]),meghdar=float(i["meghdar"]),location=Asset.objects.get(id=i["location"]),isheatset=isheatset)
                dt[i['radif']]=newRow.id
    return JsonResponse(dt)
# def export_to_excel(request):
#     pass
# #     amar=RingAmar.objects.all()
# #     data = {
# #     'Name': ['John', 'Jane', 'Mike'],
# #     'Age': [25, 30, 28],
# #     'Country': ['USA', 'Canada', 'UK']
# #     }
# #
# # # Create a workbook and select the active sheet
# #     wb = Workbook()
# #     ws = wb.active
# #
# #     # Create a DataFrame
# #     df = pd.DataFrame.from_records(amar.values())
# #
# #     # Insert the data into the worksheet
# #     for row in dataframe_to_rows(df, index=False, header=True):
# #         ws.append(row)
# #
# #     # Add a table to the worksheet
# #     # table_range = f'A1:C{len(df) + 1}'  # Adjust the range based on the size of your data
# #     # table = ws.tables.add(table_range)
# #
# #     # Save the workbook
# #     # wb.save('table_example.xlsx')
# #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
# #     response['Content-Disposition'] = 'attachment; filename=table_example.xlsx'
# #
# #     # Save the workbook to the response object
# #     wb.save(response)
# #
# #     return response
