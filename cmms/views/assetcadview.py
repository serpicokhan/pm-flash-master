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


#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetCadForm
from django.urls import reverse_lazy
from django.db import transaction
from cmms.models import *
from django.contrib.auth.decorators import permission_required

@permission_required('cmms.view_asset')
def assetcad_view(request):
    # objs=AssetCadCoordination.objects.all()
    # return render(request,'cmms/asset/dashboard/assetcad.html',{'assets':objs})
    assets=Asset.objects.filter(assetIsLocatedAt__isnull=True,assetTypes=1)
    return render(request,'cmms/asset/dashboard/assetcad.html',{'test':assets})
@permission_required('cmms.view_asset')
def assetcadmain_view(request):
    # objs=AssetCadCoordination.objects.all()
    # test
    assets=Asset.objects.filter(assetIsLocatedAt_isnull=True,assetTypes=1)
    return render(request,'cmms/asset/dashboard/assetcad.html',{'assets':objs})

def save_assetCad_form(request, form, template_name,id=None,loc=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            # books = MaintenanceType.objects.all()
            # data['html_assetCad_list'] = render_to_string('cmms/maintenancetype/partialMaintenanceTypeList.html', {
            #     'maintenanceType': books,
            #     'perms': PermWrapper(request.user)
            # })
        else:
            data['form_is_valid'] = False
            print(form.errors)

    context = {'form': form,'location':loc}


    data['html_asset_cad_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
@permission_required('cmms.view_asset')
def assetcad_create(request):
        if (request.method == 'POST'):
            form = AssetCadForm(int (request.POST.get("location",'')),request.POST)
            return save_assetCad_form(request, form, 'cmms/asset/dashboard/partialAssetCadCreate.html')

        else:
            location=request.GET.get("q","")
            if(location):
                form = AssetCadForm(loc=int(location))
                return save_assetCad_form(request, form, 'cmms/asset/dashboard/partialAssetCadCreate.html',loc=location)
        return JsonResponse(dict())
def get_assetFile(request):
    asset_id=request.GET.get('q','')
    asset_width=request.GET.get('ratiow','')
    asset_height=request.GET.get('ratioh','')
    data=dict()
    if(asset_id):
        try:
            file=AssetCadFile.objects.get(assetCadFileAssetId__id=asset_id)
            data['img']= settings.MEDIA_URL+file.assetCadFile.name
            # print(file.assetCadFileAssetId.id)
            data['id']=file.assetCadFileAssetId.id
            points=list(AssetCadCoordination.objects.filter(assetCoord__assetIsLocatedAt__id=asset_id))
            # points={}
            # for i in pts:
            print(points)

            updated_querypoints = []
            for point in points:
                print(asset_width)
                adjustmentRatioX = float(asset_width) / float(point.z);

                # print(asset_height,point.z2)
                adjustmentRatioY = float(asset_height) / float(point.z2);
                # Update the x and y values
                point.x = point.x*adjustmentRatioX
                point.y = point.y*adjustmentRatioY

                # Append the updated object to the new list
                updated_querypoints.append(point)


            data['points']=render_to_string('cmms/asset/dashboard/points.html', {
                'points': updated_querypoints


            })
        except AssetCadFile.DoesNotExist:
            pass

    return JsonResponse(data)
def get_points(request):
    id=request.GET.get("id","")
