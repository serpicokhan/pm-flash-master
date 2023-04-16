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
    objs=AssetCadCoordination.objects.all()
    return render(request,'cmms/asset/dashboard/assetcad.html',{'assets':objs})

def save_assetCad_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            print("here")
            data['form_is_valid'] = True
            # books = MaintenanceType.objects.all()
            # data['html_assetCad_list'] = render_to_string('cmms/maintenancetype/partialMaintenanceTypeList.html', {
            #     'maintenanceType': books,
            #     'perms': PermWrapper(request.user)
            # })
        else:
            data['form_is_valid'] = False
            print(form.errors)

    context = {'form': form}


    data['html_asset_cad_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
@permission_required('cmms.view_asset')
def assetcad_create(request):
        if (request.method == 'POST'):
            form = AssetCadForm(request.POST)
            return save_assetCad_form(request, form, 'cmms/asset/dashboard/partialAssetCadCreate.html')

        else:

            form = AssetCadForm()
            return save_assetCad_form(request, form, 'cmms/asset/dashboard/partialAssetCadCreate.html')
