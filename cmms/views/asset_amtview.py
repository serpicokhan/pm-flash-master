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

from cmms.models.Asset import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import AssetMeterTemplateForm

###################################################################
def list_assetMeterTemplate(request,id=None):
    books = AssetMeterTemplate.objects.all()
    return render(request, 'cmms/asset_meter_template/assetMeterTemplateList.html', {'assetMeterTemplates': books})


###################################################################
def js_list_assetMeterTemplate(request,woId):
    data=dict()
    bg_groups=BMGAsset.objects.filter(BMGAsset__id=woId).values_list('BMGGroup',flat=True)
    tmp_=BMGTemplate.objects.filter(BMGGroup__in=bg_groups).values_list('BMGTemplate',flat=True)
    books=AssetMeterTemplate.objects.filter(id__in=).values_list('BMGTemplate')).order_by('-id')

    data['html_assetMeterTemplate_list']= render_to_string('cmms/asset_amt/partialAssetAMTList.html', {
        'assetAMTs': books
    })
    data['form_is_valid']=True
    return JsonResponse(data)
